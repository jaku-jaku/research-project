from typing import Dict, List, Tuple, Union, Callable, Optional

import yaml
import numpy as np
import matplotlib.pyplot as plt

from utils.uwarl_plot import Color_Wheel, COLOR_TABLE_1, CMAP_Selector, HandlerColormap, get_color_table
from utils.uwarl_bag_parser import TYPES_VAR
from vins_replay_utils.uwarl_replay_decoder import ProcessedData

from utils.uwarl_util import create_all_folders
from typing import Dict, List, Tuple, Union, Callable, Optional

from icecream import ic


DEFAULT_FIGSIZE = (5, 5)

class AnalysisManager:
    """ Analysis Manager 
        - handle global settings and keep consistency
        - manage output folder
    """
    _auto_save  :bool 
    _auto_close :bool 
    _output_dir :str 
    _bag_dict   :Dict[str, str]
    _prefix     :str 
    _bag_directory:str
    
    def __init__(self, 
            bag_dict, 
            output_dir: str="", 
            run_name: str="vins_analysis", 
            test_set_name: str="default",
            prefix: str="",
            auto_save: bool=True,
            auto_close: bool=False,
            bag_directory: str="",
        ):
        self._bag_directory = bag_directory
        self._auto_close = auto_close
        self._auto_save = auto_save
        self._prefix = prefix
        # create output folder
        self._create_dir(output_dir, run_name, test_set_name)
        # save info
        self._bag_dict = bag_dict
        if not bag_dict: # only if exists
            print(" [WARNING] Empty bag_dict!")
    
    def _create_dir(self, output_dir: str, run_name: str, test_set_name):
        self._output_dir = f"{output_dir}/{run_name}/{test_set_name}"#/{self._prefix}"
        create_all_folders(self._output_dir)

    def save_fig(self, fig, tag, title=None, dpi=600):
        if title:
            plt.title(title)
        if self._auto_save:
            output_path=self.output_path()
            file_name=f"{output_path}plot_{tag.replace(' ', '_')}.png"
            fig.savefig(file_name, bbox_inches = 'tight', dpi=dpi)
            print(f"Saved figure to {file_name}")
        if self._auto_close:
            plt.show(block=False)
            plt.close(fig)
        else:
            plt.show(block=True)
    
    def save_dict(self, data, file_name):
        if self._auto_save:
            output_path=self.output_path()
            with open(f"{output_path}{file_name}.yaml", "w") as f:
                yaml.dump(data, f)

    def output_path(self):
        return f"{self._output_dir}/{self._prefix}_"
    
# -------------------------------- Multi-Bag Plotter -------------------------------- %% #
class MultiBagsDataManager:
    # list of data placeholder:
    list_of_bags : List
    list_of_note : List
    list_of_dT_s : List
    list_of_bag_labels : List
    N_bags : int 
    
    def __init__(self, bags: Dict[str, ProcessedData]): 
        """ Re-organize data from multiple bag files into a single object.
        """
        self.clear_cache()
        for label, data in bags.items():
            if label not in self.list_of_bag_labels: # unique only
                self.N_bags += 1
                self.list_of_bags.append(data)
                self.list_of_bag_labels.append(label)
                self.list_of_note.append(data.description)
                self.list_of_dT_s.append(data.dT)
            
    def clear_cache(self):
        self.N_bags = 0
        self.list_of_bags = []
        self.list_of_bag_labels = []
        self.list_of_note = []
        self.list_of_dT_s = []
        
    def extract_data(self, 
            bag_topic, dict_var_type:Dict[TYPES_VAR, str], 
            pre_process_funcs=None, zeroing:bool=False
        )-> Dict[str, np.ndarray]:
        """ Extract data from multiple bag files and concatenate them into a single array.
        
            # data.bag_data["/uwarl/robotnik_base_hw/voltage"][TYPES_VAR.VOLTAGE]
            # np.linalg.norm(data.bag_data["/wam/joint_states"][TYPES_VAR.JOINT_EFFORT], axis=1)       
        """
        _payload = {}
        _payload['t'] = []
        _payload['t0'] = []
        for i in range(self.N_bags):
            _len = []
            dT_s = self.list_of_dT_s[i]
            
            if bag_topic in self.list_of_bags[i].bag_data:
                topic_msg = self.list_of_bags[i].bag_data[bag_topic]
            
                # append time stamps:
                if(TYPES_VAR.TIME_STAMP_SEC in topic_msg):
                    # grab time stamps from the bag file:
                    _time = topic_msg[TYPES_VAR.TIME_STAMP_SEC] 
                    _payload['t0'].append(_time[0]) # record time zero
                    _time = np.subtract(_time, _time[0]) # reset to zero start time
                else:
                    _payload["t0"].append(-1) # record time invalid
                
                # append variables:
                _data = None
                for var_type, symbol in dict_var_type.items():
                    if symbol not in _payload:
                        _payload[symbol] = [] # initialize
                        
                    if var_type in topic_msg:
                        if pre_process_funcs is not None and var_type in pre_process_funcs:
                            _data = pre_process_funcs[var_type](topic_msg[var_type])
                        else:
                            _data = (topic_msg[var_type])
                    ## exception handles:
                    else:
                        raise ValueError(f"Unknown variable type: {var_type}")

                    if zeroing:
                        _data = np.subtract(_data, _data[0]) # reset to zero origin
                    
                    _len.append(len(_data))
                    _payload[symbol].append(_data)
                    
                if(TYPES_VAR.TIME_STAMP_SEC not in topic_msg) and _data is not None:
                    # generate time stamps uniformly, if there is no timestamp in the bag file:
                    _time = np.arange(0, dT_s, dT_s/len(_data))[0:len(_data)]
                    _payload['t0'].append(0)
                
                assert np.min(_len) == np.max(_len), f"Data variable lengths are expected to be same size in topic {_len}"
                # append time stamps:
                _payload['t'].append(_time)
            
            else: # if does not exist in the bag file:
                for var_type, symbol in dict_var_type.items():
                    if symbol not in _payload:
                        _payload[symbol] = [] # initialize
                    _payload[symbol].append([])
                _payload['t'].append([])

        return _payload
    
# %% 
# -------------------------------- 2D Plot Functions -------------------------------- %% #
## Generic Handy Multi-Segments Multi-Topical Plotting Functions:
CWheel = Color_Wheel(get_color_table("tab10", 10))

def plot_data_sets_along_xaxis(data_sets_xy, xlabel="", PAD_WIDTH=0.1, figsize=(10,5)):
    fig, ax = plt.subplots(figsize=figsize)
    
    N_size = len(data_sets_xy)
    axes = [ax if i==0 else ax.twinx() for i in range(N_size)] # twin x-axis 
    fig.subplots_adjust(right=(1-N_size*PAD_WIDTH)) 
    
    for i in range(1,N_size):
        axes[i].spines["right"].set_position(("axes", 1+(i-1)*PAD_WIDTH))
    
    if N_size > 1:
        axes[-1].set_frame_on(True)
        axes[-1].patch.set_visible(False)

    # plotting:
    for i, (label, data) in enumerate(data_sets_xy.items()):
        axes[i].plot(data["x"], data["y"], color=CWheel[i], label=label)
        axes[i].set_ylabel(label, color=CWheel[i])
        # axes[i].set_ylim(bottom=np.min(data["y"]), top=np.max(data["y"]))
        axes[i].tick_params(axis='y', labelcolor=CWheel[i], colors=CWheel[i])
    
    axes[0].set_xlabel(xlabel)
    return fig, ax

def plot_data_sets_subplots(data_sets_xys, xlabel="", figsize=(5, 5)):
    """ Plot multiple data sets on subplots, with different bag files on the same subplot.
    """
    N_sets = len(data_sets_xys)
    fig = plt.figure(figsize=(figsize[0], figsize[1]*N_sets))
    gs = fig.add_gridspec(N_sets, hspace=0.0)
    axs = gs.subplots(sharex=True)
    
    axs[-1].set_xlabel(xlabel)
    for j, (label, data) in enumerate(data_sets_xys.items()):
        for i, (_x,_y,_label)  in enumerate(zip(data["x"], data["y"], data["label"])):
            axs[j].set_ylabel(label)
            axs[j].plot(_x, _y, label=_label, color=CWheel[i])
        axs[j].legend()
    return fig, axs

# %% 
# -------------------------------- Plot Time Functions -------------------------------- %% #

def plot_time_series(
    bag_plot:MultiBagsDataManager, data_sets_y, title=None, if_label_bags=True, figsize=DEFAULT_FIGSIZE):
    """
    data_sets_y = {
        "Voltage (V)"       : battery_v,
        "Joint Effort (N.m)": joint_eff,
    }
    """
    N_bags = bag_plot.N_bags
    if title is None:
        title = " and ".join(data_sets_y.keys())
    
    # concatenate all the data:
    dT_s = np.sum(bag_plot.list_of_dT_s)
    data_sets_xy = dict()
    for label, data in data_sets_y.items():
        data_sets_xy[label] = dict()
        try:
            data_sets_xy[label]["y"] = np.concatenate(data['y'])
        except:
            print(data)
            exit(1)
        ### cumulative time:
        prev_t0 = 0
        data_sets_xy[label]["x"] = [data['t'][0]]
        for i in range(1, N_bags):
            prev_t0 += data['t'][i-1][-1]
            data_sets_xy[label]["x"].append(np.add(prev_t0, data['t'][i]))
        data_sets_xy[label]["x"] = np.concatenate(data_sets_xy[label]["x"])
                
    # figure:
    _fig_size =(figsize[0]*N_bags, figsize[1])
    fig, ax = plot_data_sets_along_xaxis(data_sets_xy, xlabel="Time (s)", figsize=_fig_size)
    # plot labels:
    plt.title(f"{title} ({N_bags} bags)")
    
    # (Auto-label) Segment bag files:
    if if_label_bags:
        t_end = 0
        y_range = plt.ylim()
        # if N_bags > 1:
        plt.axvline(x=0, color = 'r', ls='--', alpha=0.5)
        for i in range(N_bags):
            # segment bag_files
            t_end += bag_plot.list_of_dT_s[i]
            label = bag_plot.list_of_bag_labels[i]
            plt.axvline(x=t_end, color = 'r', ls='--', alpha=0.5)
            plt.text(t_end, y_range[1], f" [{label}]", color='r', verticalalignment='top', horizontalalignment='right')
        
    return fig, ax, f"{title}_time_series"

def plot_time_parallel(bag_plot:MultiBagsDataManager, data_sets_y, title=None, figsize=DEFAULT_FIGSIZE):
    """
    data_sets_y = {
        "Voltage (V)"       : battery_v,
        "Joint Effort (N.m)": joint_eff,
    }
    """
    if title is None:
        title = " and ".join(data_sets_y.keys())
    
    # prepare data:
    data_sets_xys = dict()
    for label, data in data_sets_y.items():
        data_sets_xys[label] = dict()
        data_sets_xys[label]["y"] = data['y']
        data_sets_xys[label]["x"] = data['t']
        data_sets_xys[label]["label"] = bag_plot.list_of_bag_labels
        
    fig, ax = plot_data_sets_subplots(data_sets_xys, xlabel="Time (s)", figsize=figsize)
    ax[0].set_title(f"{title} ({bag_plot.N_bags} bags)")

    return fig, ax, f"{title}_time_parallel"
    
# %% 
# -------------------------------- Plot: 3D trajectories -------------------------------- %% #
# 4. Plot:
from scipy.spatial.transform import Rotation as R
def plot_spatial(bag_plot:MultiBagsDataManager, 
        data_sets_3d, title=None, 
        figsize=DEFAULT_FIGSIZE, projection='3d', proj_type='ortho',
        N_sample=1, show_grid=True, view_angles=[(30,10),(70,45),(10,10)],
        show_orientations=False, N_orientations_sample=20, zero_orienting=False,
        scatter_or_line="line", bag_subset=None, cameras=None, zero_position=True,
        fixed_view=False,
):
    """ Plot is 3D Spatial Coordinates per data bag
        - muxing data from multiple topics
    """
    
    N_bags = bag_plot.N_bags
    N_views = len(view_angles)
    fig = plt.figure(figsize=(figsize[0]*N_bags, figsize[1]*N_views))
    fig.subplots_adjust(wspace=0, hspace=0)
    axs = [fig.add_subplot(N_views,N_bags,i+1, projection=projection, proj_type=proj_type) for i in range(N_bags*N_views)]
    
    CMAP = CMAP_Selector("Seq2")
    cmap_handles, handler_map = CMAP.get_cmap_handles(N_color=len(data_sets_3d.keys()))  
    if_scatter = scatter_or_line == "scatter"
    for j in range(N_bags):
        label_list = []
        for i, (label, data) in enumerate(data_sets_3d.items()):
            # copy data:
            is_data_valid = len(data['t'][j]) > 1
                
            if is_data_valid:
                N_sample_ = N_sample
                if "Vicon" in label: # reduce vicon sampling rate
                    N_sample_ = int(N_sample*10)
                t_ = np.array(data['t'][j][::N_sample_].copy())
                x_ = np.array(data['y'][j][::N_sample_].copy())
                u_ = np.array(data['r'][j][::N_sample_].copy())
                label_list.append(label)
            

            if "Vicon" in label and is_data_valid and (zero_orienting is True or True):
                # ic(label, j, u_[1:5])
                # rr_ = R.from_quat(u_[1:5])
                # ic(rr_.as_euler('zyx', degrees=True))
                # r2_ = R.from_quat(np.mean(uu_,axis=0)) # pick means orientation
                ic(label, u_[0:10])
                r2_ = R.from_quat(u_[0]) # pick means orientation
                r2_deg = r2_.as_euler('zyx', degrees=True)
                ic(label, r2_deg)
                r2_ = R.from_euler('z', -r2_deg[2], degrees=True)
                ic(label, r2_.as_euler('zyx', degrees=True))
                x_=r2_.apply(x_)
                label_list[-1] += " (re-oriented)"
                # TODO: reorient vicon with first index
                
            if zero_position is True:
                x_ = np.subtract(x_, x_[0])
                print(x_[0])
       
            if is_data_valid:
                # orientation correction:
                N_sample_rate = max(int(len(x_) / N_orientations_sample), 1)
                xu_ = x_[::N_sample_rate]
                uu_ = u_[::N_sample_rate]
                if show_orientations:
                    uu_[0] = uu_[1] # u_ may be 0 quaternion
                    ic(np.shape(uu_), np.shape(xu_), uu_[0])
                    r_ = R.from_quat(uu_)

            for k in range(N_views):
                view_idx = j+k*N_bags
                axs[view_idx].view_init(*view_angles[k])
                axs[view_idx].set_aspect('equal')
                axs[view_idx].grid(show_grid)
                axs[view_idx].set_xlabel("x")
                axs[view_idx].set_ylabel("y")
                axs[view_idx].set_zlabel("z")
                # plot points:
                if is_data_valid:
                    if if_scatter:
                        axs[view_idx].scatter3D(x_[:,0], x_[:,1], x_[:,2], c=t_, cmap=CMAP[i], depthshade=True, label=label_list[-1], alpha=0.2, marker=".")
                    else:
                        axs[view_idx].plot3D(x_[:,0], x_[:,1], x_[:,2], color=CWheel[i], label=label_list[-1])
                        axs[view_idx].legend(bbox_to_anchor=(0.3, 0.9), fontsize=10)
                    if show_orientations:
                        if cameras and "VINS" in label:
                            for r, x in zip(r_.as_dcm(), xu_):
                                T_rbt = np.eye(4)
                                T_rbt[0:3,0:3] = r # 3x3
                                T_rbt[0:3, 3] = x
                                # ic(r, x, T_rbt)
                                cam_id = 0 if "base" in label else 1
                                cameras[cam_id].plot_camera(ax=axs[view_idx], RBT_SE3=T_rbt, verbose=False)
                        else:
                            ex_ = r_.apply([1,0,0])
                            ey_ = r_.apply([0,1,0])
                            ez_ = r_.apply([0,0,1])
                            axs[view_idx].quiver(xu_[:,0], xu_[:,1], xu_[:,2], ex_[:,0], ex_[:,1], ex_[:,2], length=0.1, normalize=True, color="red")
                            axs[view_idx].quiver(xu_[:,0], xu_[:,1], xu_[:,2], ey_[:,0], ey_[:,1], ey_[:,2], length=0.1, normalize=True, color="green")
                            axs[view_idx].quiver(xu_[:,0], xu_[:,1], xu_[:,2], ez_[:,0], ez_[:,1], ez_[:,2], length=0.1, normalize=True, color="blue")
                    
                    if fixed_view:
                        a_ = np.max(np.abs([np.max(x_, axis=0), np.min(x_, axis=0)]))*2
                        axs[view_idx].set_xlim3d(-a_, a_)
                        axs[view_idx].set_ylim3d(-a_, a_)
                        axs[view_idx].set_zlim3d(-a_, a_)
                
        axs[j].set_title(f"{bag_plot.list_of_bag_labels[j]}")
        for k in range(N_views): 
            if if_scatter:
                axs[j+k*N_bags].legend(
                    handles=cmap_handles, labels=label_list, handler_map=handler_map, 
                    bbox_to_anchor=(0.3, 0.9), fontsize=10)
    
    # save file:
    if title is None:
        title = " and ".join(data_sets_3d.keys())
    
    attr=f"{scatter_or_line}"
    attr+= "_oriented" if zero_orienting else ""
    attr+= "_pose" if show_orientations else ""
    title = f"{title}_spatial_{attr}"

    return fig, axs, title
