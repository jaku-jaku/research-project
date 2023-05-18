#%%
import yaml
import os
import numpy as np
from icecream import ic

from dataclasses import dataclass
from typing import List, Dict, Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D

# from spatialmath import SE3
from utils.uwarl_util import read_yaml

@dataclass
class MultiSensor_Camera_Node:
    """ To parse yaml repesentation of a camera configuration with multiple sensors. (VINS)
    """
    # required:
    _config_file: str
    # hidden:
    _load_subconfigs: bool = False
    _verbose: bool = True
    _node_name: str = None
    _cam_config: Dict = None
    _cam_subconfigs: List = None
    _if_imu: int = 0
    _n_cams: int = 0
    # optional:
    _KEY_PARAM: str = "estimate_extrinsic"
    _CAM_ID = "cam{0}_calib"
    _N_CAMS = "num_of_cam"
    _IF_IMU = "imu"
    
    def __post_init__(self):
        _config_file = self._config_file
        _name = os.path.basename(_config_file)
        _dir = os.path.dirname(_config_file)
        # store:
        self._node_name = _name
        self._cam_config = self.read_camera_config(path=_config_file)
        # extract sub-configs:
        self._n_cams = self._cam_config[self._N_CAMS]
        if self._load_subconfigs:
            self._cam_subconfigs = list()
            for i in range(self._n_cams):
                _cam_config_name = os.path.join(_dir, self._cam_config[self._CAM_ID.format(i)])
                self._cam_subconfigs.append(self.read_camera_config(path=_cam_config_name))
        self._if_imu = self._cam_config[self._IF_IMU]

    @staticmethod
    def read_camera_config(path):
        ic(path)
        yaml.add_constructor(u'tag:yaml.org,2002:opencv-matrix', MultiSensor_Camera_Node.meta_constructor)
        _config = read_yaml(path)
        return _config
    
    @staticmethod
    def meta_constructor(loader, node):
        value = loader.construct_mapping(node)
        return value
    
    @staticmethod
    def create_3d_figure( 
        proj_type='ortho', graph_size=[-0.2,0.2], show_grid=True, view_angles=(20,45),
    ):
        fig = plt.figure(figsize=(18, 7))
        ax = fig.add_subplot(1,1,1, projection='3d')
        ax.view_init(*view_angles)
        ax.set_aspect("equal")#("auto")
        ax.set_xlim(graph_size)
        ax.set_ylim(graph_size)
        ax.set_zlim(graph_size)
        ax.grid(show_grid)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        return fig, ax

    def get_cam_extrinsic(self, index):
        return np.array(self._cam_config[f"body_T_cam{index}"]["data"]).reshape((4,4))
    
    def get_cam_aspect_ratio(self, index):
        if self._cam_subconfigs:
            return self._cam_subconfigs[index]["image_height"] / self._cam_subconfigs[index]["image_width"]
        else:
            return self._cam_config["image_height"] / self._cam_config["image_width"]

    def get_cam_topic(self, index):
        key = f"cam{index}_topic"
        if key in self._cam_config:
            return self._cam_config[key]
        else:
            return f"cam_{index}"
        
    def plot_camera(self, 
            ax, RBT_SE3=np.eye(4), 
            show_body_origin=True, show_axis=True, auto_adjust_frame=True,
            axis_length=0.15,
            alpha=0.35, linewidths=0.3,
            facecolors='g', edgecolors='r',
            verbose=True,
        ):
        """
        :params:
        @RBT_SE3 Rigid Body Transformation Matrix in \SE(3)
        """
        for i in range(self._n_cams): 
            extrinsic = self.get_cam_extrinsic(index=i)
            aspect_ratio = self.get_cam_aspect_ratio(index=i)
            self.plot_wireframe_camera(ax, extrinsic, RBT_SE3=RBT_SE3, aspect_ratio=aspect_ratio, f_length=axis_length,
                show_axis=show_axis, facecolors=facecolors, linewidths=linewidths, edgecolors=edgecolors, alpha=alpha, 
                auto_adjust_frame=auto_adjust_frame, cam_name=self.get_cam_topic(i), verbose=verbose)
            ic(extrinsic)

        if (self._if_imu and show_axis) or show_body_origin:
            self.plot_axis(ax, RBT_SE3=RBT_SE3, q_length=axis_length, node_label="imu", verbose=verbose)
        
    def plot_wireframe_camera(self, 
            ax, extrinsic, RBT_SE3=np.eye(4,4), 
            f_length=0.15, aspect_ratio=0.1,
            show_axis=True, auto_adjust_frame=False,
            alpha=0.35, linewidths=0.3,
            facecolors='g', edgecolors='r', 
            cam_name=None,
            verbose=True,
        ):
        vertex_std = [  [ 0, 0,0,1],
                        [ 1,-1,1,1],
                        [ 1, 1,1,1],
                        [-1, 1,1,1],
                        [-1,-1,1,1],]
        # scaling:
        vertex_std = vertex_std * np.array([f_length * aspect_ratio, f_length * aspect_ratio, f_length, 1]).T
        vertex_std = vertex_std.T
        # extrinsic transformation:
        vertex_transformed = extrinsic @ vertex_std
        # rigid body transformation:
        vertex_transformed = RBT_SE3 @ vertex_transformed
        vertex_transformed = vertex_transformed.T
        # mesh construction:
        meshes = [[vertex_transformed[0, :-1], vertex_transformed[1][:-1], vertex_transformed[2, :-1]],
                  [vertex_transformed[0, :-1], vertex_transformed[2, :-1], vertex_transformed[3, :-1]],
                  [vertex_transformed[0, :-1], vertex_transformed[3, :-1], vertex_transformed[4, :-1]],
                  [vertex_transformed[0, :-1], vertex_transformed[4, :-1], vertex_transformed[1, :-1]],
                  [vertex_transformed[1, :-1], vertex_transformed[2, :-1], vertex_transformed[3, :-1], vertex_transformed[4, :-1]]]
        # collection plot:
        ax.add_collection3d(
            Poly3DCollection(meshes, facecolors=facecolors, linewidths=linewidths, edgecolors=edgecolors, alpha=alpha))
        
        # auto adjust bounds
        if auto_adjust_frame:
            graph_size = np.max(np.max(np.abs(vertex_transformed[:,:-1])))
            if graph_size > np.max(ax.get_ylim()):
                graph_size = [-graph_size, graph_size]
                ax.set_xlim(graph_size)
                ax.set_ylim(graph_size)
                ax.set_zlim(graph_size)
                print(" [WARN] the extrinsic is out-of scope, readjusting wire-frame.")
        
        # axis plot:
        if show_axis:
            pose = RBT_SE3 @ extrinsic
            self.plot_axis(ax, RBT_SE3=pose, q_length=f_length/3, node_label=cam_name, verbose=verbose)

    def plot_axis(self, 
            ax, RBT_SE3=np.eye(4), 
            q_length=0.1, 
            node_label=None, 
            verbose=True,
        ):
        """
        :params:
        @RBT_SE3 Rigid Body Transformation Matrix in \SE(3)
        """
        ic(RBT_SE3)
        R = RBT_SE3[:3,:3]
        T = RBT_SE3[:3,3]
        x,y,z = T
        # R * np.eye(3).reshape(3,1,3)
        u,v,w = R * [1,0,0]
        ax.quiver(x,y,z, u,v,w, length=q_length, normalize=True, color="red")
        u,v,w = R * [0,1,0]
        ax.quiver(x,y,z, u,v,w, length=q_length, normalize=True, color="green")
        u,v,w = R * [0,0,1]
        ax.quiver(x,y,z, u,v,w, length=q_length, normalize=True, color="blue")
        if node_label and self._verbose and verbose:
            ax.text(x,y,z, f" {node_label}", color="black")