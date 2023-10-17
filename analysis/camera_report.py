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
# from utils.uwarl_util import read_yaml
from vins_replay_utils.uwarl_camera import MultiSensor_Camera_Node
from vins_replay_utils.uwarl_analysis_plot import AnalysisManager

from utils.uwarl_plot import Color_Wheel, get_color_table
CWheel = Color_Wheel(get_color_table("tab10", 10))

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
    # "vins-euroc-stereo-imu": f"{CONFIG_DIR}/euroc/euroc_stereo_config.yaml",
    # "vins-simulation": f"{CONFIG_DIR}/simulation/simulation_config.yaml",
    # "vins-d435i-stereo-imu": f"{CONFIG_DIR}/realsense_d435i/realsense_stereo_imu_config.yaml",
    # "vins-mynteye-mono-imu":   f"{CONFIG_DIR}/mynteye/mynteye_mono_imu_config.yaml",
    # "vins-mynteye-stereo-imu": f"{CONFIG_DIR}/mynteye/mynteye_stereo_imu_config.yaml",
    # "l515-mono-imu": f"{CONFIG_DIR}/uwarl_l515/mono_imu_config_EE.yaml",
    # "d455-stereo-imu": f"{CONFIG_DIR}/uwarl_d455/stereo_imu_config_EE.yaml",
    # "d435i-stereo": f"{CONFIG_DIR}/uwarl_d435i/stereo_config_EE.yaml",
    # "d435i-stereo-imu": f"{CONFIG_DIR}/uwarl_d435i/stereo_imu_config_EE.yaml",
    # "euroc-stereo":f"{CONFIG_DIR}/euroc/euroc_stereo_config.yaml",
    # "euroc-stereo-imu":f"{CONFIG_DIR}/euroc/euroc_stereo_imu_config.yaml",
    # "euroc-mono-imu":f"{CONFIG_DIR}/euroc/euroc_mono_imu_config.yaml",
    "d455-mono-imu-color-EE": f"{CONFIG_DIR}/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    "d455-mono-imu-color-base": f"{CONFIG_DIR}/uwarl_d455/mono_rgb_imu_config_base.yaml",
    "d435i-stereo-imu": f"{CONFIG_DIR}/realsense_d435i/realsense_stereo_imu_config.yaml",
    # "d455-stereo-imu-test":f"{CONFIG_DIR}/uwarl_d455/stereo_imu_config_test.yaml",
    # "d455-base-manufacture-Tic":f"{CONFIG_DIR}/uwarl_d455/eval_config_base_manufacture_Tic_c2i.yaml",
    # "d455-EE-manufacture-Tic":f"{CONFIG_DIR}/uwarl_d455/eval_config_EE_manufacture_Tic_c2i.yaml",
    # "d455-EE-kalibr-Tic":f"{CONFIG_DIR}/uwarl_d455/eval_config_EE_kalibr_Tic_c2i.yaml",
    # "d455-nase-kalibr-Tic":f"{CONFIG_DIR}/uwarl_d455/eval_config_base_kalibr_Tic_c2i.yaml",
    # "d455-stereo-imu":f"{CONFIG_DIR}/uwarl_d455/stereo_imu_config_EE.yaml",
}
COMBINED_OVERLAY = True

cams = dict()
fig, ax = None, None
cam_names = []
colors = []
for cam_name, cam_config_path in CONFIGS.items():
    cam_names.append(cam_name)
    cams[cam_name] = MultiSensor_Camera_Node(_config_file=cam_config_path, _verbose=False)
    if fig is None or not COMBINED_OVERLAY:
        fig, ax = cams[cam_name].create_3d_figure(view_angles=(20,45))
    # a = SE3.EulerVec([-np.pi/4,0,0]).A
    if COMBINED_OVERLAY:
        colors.append(CWheel.next())
        cams[cam_name].plot_camera(ax=ax, facecolors=colors[-1], alpha=0.2)
    else:
        cams[cam_name].plot_camera(ax=ax)
        AM.save_fig(fig, tag=cam_name, title=f"Camera Config ({cam_name})")

if COMBINED_OVERLAY:
    AM.save_fig(fig, tag="+".join(cam_names), title=f"Camera Config (Overlay)")

# %%

# %% 
# NOW, LET'S ROTATE THE CAMERA, AND SEE THE CONFIGURATION:
from spatialmath import SE3
ENABLE_TRANSFORM = False
if ENABLE_TRANSFORM:
    cam_E = cams["d455-mono-imu-color-base"]
    # cam_b = cams["d455-stereo-imu-base"]

def vins_d455_extrinsic_transformation(cam):
    A = cam.get_cam_extrinsic(index=0)
    # B = cam.get_cam_extrinsic(index=1)
    
    ## NOTE: here is the inverse:
    Ainv = np.linalg.inv(A)
    # Binv = np.linalg.inv(B)

    A = np.array(A).reshape((4,4))
    # B = np.array(B).reshape((4,4))
    # its equivalent to inverse:
    a = SE3.EulerVec([0,0,-np.pi/2]).A
    a = a @ SE3.EulerVec([-np.pi/2,0,0]).A 

    A = a @ A 
    # B = a @ B 
    # ic(A,a, A2);
    ic(A.reshape(16));
    # ic(B.reshape(16));
    ic(Ainv.reshape(16));
    # ic(Binv.reshape(16));
    return a, A, 0 #, B

if ENABLE_TRANSFORM:
    T_E, L_E, R_E= vins_d455_extrinsic_transformation(cam_E)
    ic(L_E, R_E);
    fig, ax = cam_E.create_3d_figure()
    cam_E.plot_camera(ax=ax, RBT_SE3=T_E)
    
    # T_b, L_b, R_b= vins_d455_extrinsic_transformation(cam_b)
    # ic(L_b, R_b);
    # fig, ax = cam_b.create_3d_figure()
    # cam_b.plot_camera(ax=ax, RBT_SE3=T_b)

# %%
