# %%
import yaml
import os
import numpy as np
from pathlib import Path
from datetime import datetime


from dataclasses import dataclass
from typing import List, Dict, Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D

from icecream import ic

# from spatialmath import SE3
from utils.uwarl_util import read_yaml
from vins_replay_utils.uwarl_camera import MultiSensor_Camera_Node
from vins_replay_utils.uwarl_analysis_plot import AnalysisManager

# %%
FIG_OUT_DIR = f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/research-project/output/vins_analysis"
CONFIG_DIR = f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config"
FEATURE_AUTO_SAVE                   = True
FEATURE_AUTO_CLOSE_FIGS             = True

AM = AnalysisManager(
    bag_dict=None,
    output_dir=FIG_OUT_DIR,
    run_name="run_{}".format(datetime.now().strftime("%Y-%m-%d")), 
    test_set_name="MANUAL_TEST",
    prefix="camera",
    auto_save=FEATURE_AUTO_SAVE,
    auto_close=FEATURE_AUTO_CLOSE_FIGS,
    bag_directory=None,
)

# 
CONFIGS = {
    "l515-mono-imu": f"{CONFIG_DIR}/uwarl_l515/mono_imu_config_EE.yaml",
    "d455-mono-imu-color": f"{CONFIG_DIR}/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    "d455-stereo-imu": f"{CONFIG_DIR}/uwarl_d455/stereo_imu_config_EE.yaml",
    "d435i-stereo-imu": f"{CONFIG_DIR}/uwarl_d435i/stereo_imu_config_EE.yaml",
    "vins-euroc-stereo-imu": f"{CONFIG_DIR}/euroc/euroc_stereo_config.yaml",
    "vins-simulation": f"{CONFIG_DIR}/simulation/simulation_config.yaml",
    "vins-d435i-stereo-imu": f"{CONFIG_DIR}/realsense_d435i/realsense_stereo_imu_config.yaml",
    "vins-mynteye-mono-imu":   f"{CONFIG_DIR}/mynteye/mynteye_mono_imu_config.yaml",
    "vins-mynteye-stereo-imu": f"{CONFIG_DIR}/mynteye/mynteye_stereo_imu_config.yaml",
}

for cam_name, cam_config_path in CONFIGS.items():
    cam_d455 = MultiSensor_Camera_Node(_config_file=cam_config_path)
    fig, ax = cam_d455.create_3d_figure()
    # a = SE3.EulerVec([-np.pi/4,0,0]).A
    cam_d455.plot_camera(ax=ax)#, RBT_SE3=a)
    AM.save_fig(fig, tag=cam_name)

# %%
