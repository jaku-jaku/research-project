from enum import Enum

#   Base    \Arm:| Pt-FWD | Ext-F | Pt-Up | Pt-Down | **Pt-L/R| *Up-Down | 
#   Stationary   | 01   | 02     | 03    | 04      | 05      | 06       |       
#   *Spin        | 07   | 08     | 09    | 10      | 11      | 12       |
#   *FWD         | 13   | 14     | 15    | 16      | 17      | 18       |
#   *RVR         | 19   | 20     | 21    | 22      | 23      | 24       |
#   *Circling    | 25   | 26     | 27    | 28      | 29      | 30       |
#   88           | 31   | 32     | 33    | 34      | 35      | 36       |    

from scipy.spatial.transform import Rotation as R
from utils.uwarl_bag_parser import TYPES_VAR

rx = R.from_euler('x', 90, degrees=True)

TEST_SET_TITLE = "D455 (640)"
####### 1108    Collection :
class DATASET_DEMO_1115_BASICS(Enum):
    SPI_H   = ["dual_640-0-0_DEMO-7_vins-replay.bag"]
    SPI_E   = ["dual_640-0-1_DEMO-8_vins-replay.bag"]
    SPI_U   = ["dual_640-0-2_DEMO-9_vins-replay.bag"]
    SPI_D   = ["dual_640-0-3_DEMO-10_vins-replay.bag"]
    SPI_LR  = ["dual_640-0-4_DEMO-11_vins-replay.bag"]
    SPI_UD  = ["dual_640-0-5_DEMO-12_vins-replay.bag"]
    
    # driving facing towards checkerboard 
    FWD_H   = ["dual_640-0-6_DEMO-13_vins-replay.bag"]
    FWD_E   = ["dual_640-0-8_DEMO-14_vins-replay.bag"]
    FWD_U   = ["dual_640-0-10_DEMO-15_vins-replay.bag"]
    FWD_D   = ["dual_640-0-12_DEMO-16_vins-replay.bag"]
    FWD_LR  = ["dual_640-0-14_DEMO-17_vins-replay.bag"]
    FWD_UD  = ["dual_640-0-16_DEMO-18_vins-replay.bag"]
    
    RVR_H   = ["dual_640-0-7_DEMO-19_vins-replay.bag"]
    RVR_E   = ["dual_640-0-9_DEMO-20_vins-replay.bag"]
    RVR_U   = ["dual_640-0-11_DEMO-21_vins-replay.bag"]
    RVR_D   = ["dual_640-0-13_DEMO-22_vins-replay.bag"]
    RVR_LR  = ["dual_640-0-15_DEMO-23_vins-replay.bag"]
    RVR_UD  = ["dual_640-0-17_DEMO-24_vins-replay.bag"]

class DATASET_DEMO_1115_DYNAMICS(Enum):
    # Circular motion
    CIR_H  = ["dual_640-0-18_DEMO-25_vins-replay.bag"]
    CIR_E  = ["dual_640-0-19_DEMO-26_vins-replay.bag"]
    CIR_U  = ["dual_640-0-20_DEMO-27_vins-replay.bag"]
    CIR_D  = ["dual_640-0-21_DEMO-28_vins-replay.bag"]
    CIR_LR = ["dual_640-0-22_DEMO-29_vins-replay.bag"]
    CIR_UD = ["dual_640-0-23_DEMO-30_vins-replay.bag"]
    # BEE motion 8
    BEE_H  = ["dual_640-0-24_DEMO-31_vins-replay.bag"]
    BEE_E  = ["dual_640-0-25_DEMO-32_vins-replay.bag"]
    BEE_U  = ["dual_640-0-26_DEMO-33_vins-replay.bag"]
    BEE_D  = ["dual_640-0-27_DEMO-34_vins-replay.bag"]
    BEE_LR = ["dual_640-0-28_DEMO-35_vins-replay.bag"]
    BEE_UD = ["dual_640-0-29_DEMO-36_vins-replay.bag"]
    # Square
    SQR_H  = ["dual_640-0-30_DEMO-37_vins-replay.bag"]
    SQR_E  = ["dual_640-0-31_DEMO-38_vins-replay.bag"]
    SQR_U  = ["dual_640-0-32_DEMO-39_vins-replay.bag"]
    SQR_D  = ["dual_640-0-34_DEMO-40_vins-replay.bag"]
    SQR_LR = ["dual_640-0-35_DEMO-41_vins-replay.bag"]
    SQR_UD = ["dual_640-0-36_DEMO-42_vins-replay.bag"]
    
    TRI_H  = ["dual_640-0-37_DEMO-49_vins-replay.bag"]
    TRI_E  = ["dual_640-0-38_DEMO-50_vins-replay.bag"]
    TRI_U  = ["dual_640-0-39_DEMO-51_vins-replay.bag"]
    TRI_D  = ["dual_640-0-40_DEMO-52_vins-replay.bag"]
    TRI_LR = ["dual_640-0-41_DEMO-53_vins-replay.bag"]
    TRI_UD = ["dual_640-0-42_DEMO-54_vins-replay.bag"]

CONFIG_1115_640x480 = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_1115_640x480/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-11-16", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-11-16"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual_640.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_1115_640x480/session_0/demo_map.json",
}
class DUAL_1115_BASICS_baseline_vs_decoupled(Enum):
    CONFIG = CONFIG_1115_640x480
    TEST_SET = DATASET_DEMO_1115_BASICS

class DUAL_1115_DYNAMICS_baseline_vs_decoupled(Enum):
    CONFIG = CONFIG_1115_640x480
    TEST_SET = DATASET_DEMO_1115_DYNAMICS

