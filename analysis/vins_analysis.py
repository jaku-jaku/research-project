# %% -------------------------------- Import Lib -------------------------------- %% #
# built-in
import os
from datetime import datetime

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Callable, Optional
from enum import Enum


# 3rd party lib
import pandas as pd
import numpy as np
import yaml

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

# ros:
import rosbag

# 3rd party util
from icecream import ic

# %% 
# -------------------------------- Import Our Lib -------------------------------- %% #
# ours:
from utils.uwarl_util import create_all_folders
from utils.uwarl_bag_parser import BagParser, TYPES_VAR
from utils.uwarl_plot import Color_Wheel, COLOR_TABLE_1, CMAP_Selector, HandlerColormap, get_color_table

from configs.uwarl_common import PARSER_CALLBACKS
from configs.uwarl_test_set import TEST_SET_STEREO_IMU, TEST_SET_MONO_IMU, TEST_SET_STEREO, TEST_SET_SINGLE

# %% [markdown]
# # 1. Pre-Config
FIG_OUT_DIR = "/home/jx/UWARL_catkin_ws/src/vins-research-pkg/research-project/output/vins_analysis"

BAG_TEST_SET        = TEST_SET_SINGLE
BAG_FILES_SELECTED  = BAG_TEST_SET.Base_i9
BAG_DRECTORY        = BAG_TEST_SET.DIRECTORY

FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS  = True
FEATURE_OUTPUT_BAG_META             = True
FEATURE_AUTO_SAVE                   = True
FEATURE_AUTO_CLOSE_FIGS             = False

print(f"BAG_FILES_SELECTED: {BAG_FILES_SELECTED}")
print(f"BAG_DRECTORY: {BAG_DRECTORY}")

# %% 
# -------------------------------- Files Automation -------------------------------- %% #
def decode_replayed_vins_bag_file_name(_bag_path:str):
    prefix = _bag_path.split("_recording_")[0]
    ic(prefix)
    unique_id, t_window, run_id, _, demo_id = prefix.split("_")
    tag, session_id, run_id = unique_id.split("-")
    description = {
        "cam-session-run": unique_id,
        "tag": tag,
        "session_id": session_id,
        "dt": t_window,
        "demo": demo_id,
        "run_id": run_id,
    }
    return description

def auto_generate_labels_from_bag_file_name(list_of_bag_path:List[str]):
    # auto generate labels based on demo id
    id_list = ["NULL"]
    for konfig_base in ["FIX", "SPI", "FWD", "RVR", "CIR", "88"]:
        for kongig_arm in ["Home", "Pt-F", "Pt-U", "Pt-D", "Pt-LR", "Pt-UD"]:
            id_list.append(f"{konfig_base}-{kongig_arm}")
        
    _bag_dict = dict()
    for path in list_of_bag_path:
        description = decode_replayed_vins_bag_file_name(path)
        demo = id_list[int(description["demo"])]
        tag = description["tag"]
        session_id = description["session_id"]
        run_id = description["run_id"]
        bag_label = f"{tag}-{demo}-s{session_id}-i{run_id}"
        _bag_dict[bag_label] = path
    return _bag_dict

AUTO_BAG_DICT = auto_generate_labels_from_bag_file_name(BAG_FILES_SELECTED.value)
ic(AUTO_BAG_DICT);
        
# %% 
# -------------------------------- Manager & Configs -------------------------------- %% #
BAG_DICT = AUTO_BAG_DICT

# NOTE: to override the auto-gen bag_dict:
# BAG_DICT = {
#     # Copy the `AUTO_BAG_DICT` or `info.yaml` here to select the bag files manually:
#     'EE-88-Pt-F-s3-i5': 'EE-3-5_S5-E30_5_DEMO_32_recording_2023-04-06-16-26-52_2023-04-11-11-33-31.bag',
# }

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
        self._save_info(bag_dict=bag_dict)
    
    def _create_dir(self, output_dir: str, run_name: str, test_set_name):
        self._output_dir = f"{output_dir}/{run_name}/{test_set_name}/{self._prefix}"
        create_all_folders(self._output_dir)

    def _save_info(self, bag_dict: Dict[str, str]):
        self._bag_dict = bag_dict
        self.save_dict(bag_dict, "info")
            
    def save_fig(self, fig, tag):
        if self._auto_save:
            file_name=f"{self._output_dir}/plot_{tag.replace(' ', '_')}.png"
            fig.savefig(file_name, bbox_inches = 'tight')
            print(f"Saved figure to {file_name}")
        if self._auto_close:
            plt.close(fig)
    
    def save_dict(self, data, file_name):
        if self._auto_save:
            with open(f"{self._output_dir}/{file_name}.yaml", "w") as f:
                yaml.dump(data, f)

BP = BagParser(PARSER_CALLBACKS)
AM = AnalysisManager(
    bag_dict=AUTO_BAG_DICT,
    output_dir=FIG_OUT_DIR,
    run_name="run_{}".format(datetime.now().strftime("%Y-%m-%d")), 
    test_set_name=BAG_TEST_SET.__name__,
    prefix=BAG_FILES_SELECTED.name,
    auto_save=FEATURE_AUTO_SAVE,
    auto_close=FEATURE_AUTO_CLOSE_FIGS,
    bag_directory=BAG_DRECTORY.value,
)

# %% [markdown]
# # 2. Data Pre-Processing

# %% 
# -------------------------------- Processing -------------------------------- %% #
# Processed Data Object Placeholder
class ProcessedData:
    """ Placeholder for processed data
        - bag files will be loaded with BagParser and processed in batch
        - processed data will be cached in this class
    """
    _bag_path: str=""
    bag_info: Dict[str, Union[str, float]] = {}
    bag_topics: Dict[str, List[str]] = {}
    bag_data: Dict[str, Union[str, float]] = {}
    bag_samples: Dict[str, Union[str, float]] = {}
    T0: float = 0.0
    T1: float = 0.0
    dT: float = 0.0
    description: Dict[str, Union[str, float]] = {}

    def __init__(self, directory, bag_path):
        self._bag_path = bag_path
        # load bag file:
        BP.bind_bagfile(bagfile=f"{directory}/{bag_path}")
        BP.load_bag_topics()
        self.bag_info = BP.get_bag_info_safe()
        self.bag_topics = BP.get_bag_topics_lut_safe()
        BP.process_all_bag_msgs()
        self.bag_data = BP.get_processed_bag_safe()
        self.bag_samples = BP.get_bag_samples_safe()
        # self._bag = BP._bag_data # DEBUG: debug purpose
        # unbind toolchain
        BP.unbind_bagfile()
        self._init_process()
    
    def _init_process(self):
        self.T0=datetime.fromtimestamp(self.bag_info["start"])
        self.T1=datetime.fromtimestamp(self.bag_info["end"])
        self.dT = (self.T1 - self.T0).total_seconds()
        self.description = decode_replayed_vins_bag_file_name(self._bag_path)
        ic(self.description)

# 1. Process and Aggregate data from multiple bags:
pData={}
for label, path in AM._bag_dict.items():
    pData[label] = ProcessedData(AM._bag_directory, path)
        

# %% 
# -------------------------------- DEBUG -------------------------------- %% #
# DEBUG: save a sample here:
if FEATURE_OUTPUT_BAG_META:
    for label, data in pData.items():
        AM.save_dict(data.bag_samples, "bag_samples")
        AM.save_dict(data.bag_topics, "bag_topics")
        AM.save_dict(data.bag_info, "bag_info")
        break

# %% [markdown]
# # 3. Plotting Multiple datasets from multiple bagfiles

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
    N_sets = len(data_sets_y)
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
# -------------------------------- Multi-Bag Plotter -------------------------------- %% #
class Bags_Data_Plot:
    DEFAULT_FIGSIZE = (5, 5)
    # list of data placeholder:
    list_of_bags = []
    list_of_note = []
    list_of_dT_s = []
    list_of_bag_labels = []
    # list_of_battery_v = []
    # list_of_joint_eff = []
    N_bags = 0
    NAME: str = None
    
    def __init__(self, bags: Dict[str, ProcessedData]): 
        """ Re-organize data from multiple bag files into a single object.
        """
        for label, data in bags.items():
            if label not in self.list_of_bag_labels: # unique only
                self.N_bags += 1
                self.list_of_bags.append(data)
                self.list_of_bag_labels.append(label)
                self.list_of_note.append(data.description)
                self.list_of_dT_s.append(data.dT)
            
    
    def extract_data(self, 
            bag_topic, dict_var_type:Dict[TYPES_VAR, str], 
            pre_process_func=lambda x: x, zeroing:bool=False
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

                
                # append variables:
                _data = None
                for var_type, symbol in dict_var_type.items():
                    if symbol not in _payload:
                        _payload[symbol] = [] # initialize
                        
                    if var_type in topic_msg:
                        _data = pre_process_func(topic_msg[var_type])
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
    
# 2. Load into data plotter:
BagPlot = Bags_Data_Plot(pData)
# %% 
# -------------------------------- Plot Functions -------------------------------- %% #

def plot_time_series(bag_plot, data_sets_y, title=None, if_label_bags=True, figsize=Bags_Data_Plot.DEFAULT_FIGSIZE):
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
        data_sets_xy[label]["y"] = np.concatenate(data['y'])
        ### cumulative time:
        prev_t0 = 0
        data_sets_xy[label]["x"] = [data['t'][0]]
        for i in range(1, N_bags):
            prev_t0 += data['t'][i-1][-1]
            data_sets_xy[label]["x"].append(np.add(prev_t0, data['t'][i]))
        data_sets_xy[label]["x"] = np.concatenate(data_sets_xy[label]["x"])
                
    # figure:
    _fig_size =(figsize[0]*N_bags, figsize[1])
    fig, _ = plot_data_sets_along_xaxis(data_sets_xy, xlabel="Time (s)", figsize=_fig_size)
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
    
    AM.save_fig(fig, f"{title}_time_series")

def plot_time_parallel(bag_plot, data_sets_y, title=None, figsize=Bags_Data_Plot.DEFAULT_FIGSIZE):
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
    AM.save_fig(fig, f"{title}_time_parallel")



# %% 
# -------------------------------- Plot: Voltage & Joint Efforts -------------------------------- #
from scipy.ndimage import gaussian_filter1d
if FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS:
    # 3. assemble data sets:
    data_sets_y = {
        "Voltage (V)"       : BagPlot.extract_data(
            bag_topic="/uwarl/robotnik_base_hw/voltage", 
            dict_var_type={TYPES_VAR.VOLTAGE: 'y'},
        ),
        "Joint Effort (Filtered) (N.m)": BagPlot.extract_data(
            bag_topic="/wam/joint_states", 
            dict_var_type={TYPES_VAR.JOINT_EFFORT: 'y'},
            pre_process_func=lambda x: gaussian_filter1d(np.linalg.norm(x, axis=1), 3),
        ),
    }

    # 4. Plot:
    plot_time_series(BagPlot, data_sets_y)
    plot_time_parallel(BagPlot, data_sets_y, figsize=(15,4))

# %%
# -------------------------------- Plot Data Prep: 3D trajectories -------------------------------- %% #
# 3. assemble data sets:
POSE_VARS = {
    TYPES_VAR.POSITION_XYZ: 'y',
    TYPES_VAR.ORIENTATION_XYZW: 'r',
}
data_sets_3d = dict()
if AM._prefix in [BAG_TEST_SET.Base_i8.name, BAG_TEST_SET.Base_i9.name]:
    data_sets_3d["Summit Base"] = BagPlot.extract_data(
        bag_topic="/vicon/summit_base/summit_base", zeroing=True, dict_var_type=POSE_VARS,
    )
else:
    data_sets_3d["WAM EE"]= BagPlot.extract_data(
        bag_topic="/vicon/wam_EE/wam_EE", zeroing=True, dict_var_type=POSE_VARS,
    )
    # data_sets_3d["WAM base"]= BagPlot.extract_data(
    #     bag_topic="/vicon/base_EE/base_base", zeroing=True, dict_var_type=POSE_VARS,
    # ),
data_sets_3d.update({
    "VINS est"       : BagPlot.extract_data(
        bag_topic="/vins_estimator/path", zeroing=True, dict_var_type=POSE_VARS,
    ),
    "VINS loop"       : BagPlot.extract_data(
        bag_topic="/loop_fusion/pose_graph_path", zeroing=True, dict_var_type=POSE_VARS,
    ),
})

for label,data in data_sets_3d.items():
    print(f"> [{label}] t0:{data['t0']}")
    
# %% 
# -------------------------------- Plot: 3D trajectories -------------------------------- %% #
# 4. Plot:
from scipy.spatial.transform import Rotation as R
def plot_spatial(bag_plot, 
        data_sets_3d, title=None, 
        figsize=Bags_Data_Plot.DEFAULT_FIGSIZE, projection='3d', proj_type='ortho',
        N_sample=1, show_grid=True, view_angles=[(30,10),(70,45),(10,10)],
        show_orientations=False, N_orientations_sample=10,zero_orienting=False,
        scatter_or_line="line",
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
        for i, (label, data) in enumerate(data_sets_3d.items()):
            # copy data:
            is_data_valid = len(data['t'][j]) > 1
                
            if is_data_valid:
                t_ = np.array(data['t'][j][::N_sample].copy())
                x_ = np.array(data['y'][j][::N_sample].copy())
            
            if is_data_valid:
                # orientation correction:
                xu_ = x_[::N_orientations_sample]
                u_ = np.array(data['r'][j][::N_sample].copy())
                uu_ = np.array(data['r'][j][::N_orientations_sample].copy())
                if show_orientations:
                    uu_[0] = uu_[1] # u_ may be 0 quaternion
                    ic(np.shape(uu_), np.shape(xu_), uu_[0])
                    r_ = R.from_quat(uu_)

            if label in ["VINS est", "VINS loop"] and is_data_valid and zero_orienting is True:
                # ic(label, j, u_[1:5])
                # rr_ = R.from_quat(u_[1:5])
                # ic(rr_.as_euler('zyx', degrees=True))
                # r2_ = R.from_quat(np.mean(uu_,axis=0)) # pick means orientation
                r2_ = R.from_quat(np.mean(u_[5:20],axis=0)) # pick means orientation
                r2_deg = r2_.as_euler('zyx', degrees=True)
                r2_ = R.from_euler('z', r2_deg[0], degrees=True)
                ic(r2_deg)
                x_=r2_.apply(x_)
            
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
                        axs[view_idx].scatter3D(x_[:,0], x_[:,1], x_[:,2], c=t_, cmap=CMAP[i], depthshade=True)
                    else:
                        axs[view_idx].plot3D(x_[:,0], x_[:,1], x_[:,2], color=CWheel[i], label=label)
                        axs[view_idx].legend(bbox_to_anchor=(0.3, 0.9), fontsize=10)
                    if show_orientations:
                        ex_ = r_.apply([1,0,0])
                        ey_ = r_.apply([0,1,0])
                        ez_ = r_.apply([0,0,1])
                        axs[view_idx].quiver(xu_[:,0], xu_[:,1], xu_[:,2], ex_[:,0], ex_[:,1], ex_[:,2], length=0.1, normalize=True, color="red")
                        axs[view_idx].quiver(xu_[:,0], xu_[:,1], xu_[:,2], ey_[:,0], ey_[:,1], ey_[:,2], length=0.1, normalize=True, color="green")
                        axs[view_idx].quiver(xu_[:,0], xu_[:,1], xu_[:,2], ez_[:,0], ez_[:,1], ez_[:,2], length=0.1, normalize=True, color="blue")
                    
                    a_ = np.max(np.abs([np.max(x_, axis=0), np.min(x_, axis=0)]))
                    axs[view_idx].set_xlim3d(a_, -a_)
                    axs[view_idx].set_ylim3d(a_, -a_)
                    axs[view_idx].set_zlim3d(0, a_)
                
        axs[j].set_title(f"{bag_plot.list_of_bag_labels[j]}")
        for k in range(N_views): # FIXME: all legens will show even there is no data plot, need sth else?? (no need for now)
            if if_scatter:
                axs[j+k*N_bags].legend(
                    handles=cmap_handles, labels=data_sets_3d.keys(), handler_map=handler_map, 
                    bbox_to_anchor=(0.3, 0.9), fontsize=10)
    
    # save file:
    if title is None:
        title = " and ".join(data_sets_3d.keys())
    AM.save_fig(fig, f"{title}_spatial_{scatter_or_line}")
        
    return fig, axs

# # 4. Plot:
### pip install ipympl
# fig, axs = plot_spatial(BagPlot, data_sets_3d, figsize=(10,8), view_angles=[(30,45)], show_orientations=False)
fig, axs = plot_spatial(BagPlot, data_sets_3d, figsize=(10,8), zero_orienting=False, scatter_or_line='scatter') # default 3 views
plt.show()
fig, axs = plot_spatial(BagPlot, data_sets_3d, figsize=(10,8), zero_orienting=False, scatter_or_line='line') # default 3 views
plt.show()

# fig.canvas.toolbar_visible = True
# fig.canvas.header_visible = True
# fig.canvas.resizable = True

# %%
