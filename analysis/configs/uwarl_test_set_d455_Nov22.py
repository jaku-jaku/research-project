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

TEST_SET_TITLE = "D455"
####### 1101    Collection :
class DATASET_DEMO_1122_BASIC_1(Enum):
    SPI_H   = ["dual-1-0_DEMO-7_vins-replay.bag"]
    SPI_E   = ["dual-1-1_DEMO-8_vins-replay.bag"]
    SPI_U   = ["dual-1-2_DEMO-9_vins-replay.bag"]
    SPI_D   = ["dual-1-3_DEMO-10_vins-replay.bag"]
    SPI_LR  = ["dual-1-4_DEMO-11_vins-replay.bag"]
    SPI_UD  = ["dual-1-5_DEMO-12_vins-replay.bag"]
    
    FWD_H   = ["dual-1-6_DEMO-13_vins-replay.bag"]
    FWD_E   = ["dual-1-8_DEMO-14_vins-replay.bag"]
    FWD_U   = ["dual-1-10_DEMO-15_vins-replay.bag"]
    FWD_D   = ["dual-1-12_DEMO-16_vins-replay.bag"]
    FWD_LR  = ["dual-1-14_DEMO-17_vins-replay.bag"]
    FWD_UD  = ["dual-1-16_DEMO-18_vins-replay.bag"]
    
    RVR_H   = ["dual-1-7_DEMO-19_vins-replay.bag"]
    RVR_E   = ["dual-1-9_DEMO-20_vins-replay.bag"]
    RVR_U   = ["dual-1-11_DEMO-21_vins-replay.bag"]
    RVR_D   = ["dual-1-13_DEMO-22_vins-replay.bag"]
    RVR_LR  = ["dual-1-15_DEMO-23_vins-replay.bag"]
    RVR_UD  = ["dual-1-17_DEMO-24_vins-replay.bag"]
    
class DATASET_DEMO_1122_BASIC_2(Enum):
    CIR_H  = ["dual-2-1_DEMO-25_vins-replay.bag"]
    CIR_E  = ["dual-2-2_DEMO-26_vins-replay.bag"]
    CIR_U  = ["dual-2-3_DEMO-27_vins-replay.bag"]
    CIR_D  = ["dual-2-4_DEMO-28_vins-replay.bag"]
    CIR_LR = ["dual-2-5_DEMO-29_vins-replay.bag"]
    CIR_UD = ["dual-2-6_DEMO-30_vins-replay.bag"]
    
    BEE_H  = ["dual-2-7_DEMO-31_vins-replay.bag"]
    BEE_E  = ["dual-2-8_DEMO-32_vins-replay.bag"]
    BEE_U  = ["dual-2-9_DEMO-33_vins-replay.bag"]
    BEE_D  = ["dual-2-10_DEMO-34_vins-replay.bag"]
    BEE_LR = ["dual-2-11_DEMO-35_vins-replay.bag"]
    BEE_UD = ["dual-2-12_DEMO-36_vins-replay.bag"]
    
    SQR_H  = ["dual-2-14_DEMO-37_vins-replay.bag"]
    SQR_E  = ["dual-2-15_DEMO-38_vins-replay.bag"]
    SQR_U  = ["dual-2-16_DEMO-39_vins-replay.bag"]
    SQR_D  = ["dual-2-17_DEMO-40_vins-replay.bag"]
    SQR_LR = ["dual-2-18_DEMO-41_vins-replay.bag"]
    SQR_UD = ["dual-2-19_DEMO-42_vins-replay.bag"]
    
    TRI_H  = ["dual-3-2_DEMO-43_vins-replay.bag"]
    TRI_E  = ["dual-3-3_DEMO-44_vins-replay.bag"]
    TRI_U  = ["dual-3-4_DEMO-45_vins-replay.bag"]
    TRI_D  = ["dual-3-5_DEMO-46_vins-replay.bag"]
    TRI_LR = ["dual-3-6_DEMO-47_vins-replay.bag"]
    TRI_UD = ["dual-3-7_DEMO-48_vins-replay.bag"]

class DATASET_DEMO_1122_BASIC_ROGUE(Enum):
    TIM_H  = ["dual-0-1_DEMO-55_vins-replay.bag"]
    TIM_U  = ["dual-0-2_DEMO-57_vins-replay.bag"]
    TIM_UD = ["dual-0-3_DEMO-60_vins-replay.bag"]

class DATASET_DEMO_1122_LONG_1(Enum):
    L_BEE_H   =["dual-0-0_DEMO-49_vins-replay.bag"]
    L_BEE_E   =["dual-0-1_DEMO-50_vins-replay.bag"]
    L_BEE_U   =["dual-0-2_DEMO-51_vins-replay.bag"]
    L_BEE_D   =["dual-0-3_DEMO-52_vins-replay.bag"]
    L_BEE_LR  =["dual-0-4_DEMO-53_vins-replay.bag"]
    L_BEE_UD  =["dual-0-5_DEMO-54_vins-replay.bag"]
    
    L_SQR_H   =["dual-1-0_DEMO-61_vins-replay.bag"]
    L_SQR_E   =["dual-1-1_DEMO-62_vins-replay.bag"]
    L_SQR_U   =["dual-1-2_DEMO-63_vins-replay.bag"]
    L_SQR_D   =["dual-1-3_DEMO-64_vins-replay.bag"]
    L_SQR_LR  =["dual-1-4_DEMO-65_vins-replay.bag"]
    L_SQR_UD  =["dual-1-5_DEMO-66_vins-replay.bag"]

class DATASET_DEMO_1122_LONG_ROGUE(Enum):
    ROG_UD   = ["dual-2-1_DEMO-60_vins-replay.bag"]
    # ROG_LR_2 = ["dual-2-2_DEMO-1_vins-replay.bag"]
    ROG_LR_1 = ["dual-2-3_DEMO-59_vins-replay.bag"]
    # WILD     = ["dual-3-0_DEMO-59_vins-replay.bag"]

CONFIG_1122_BASIC = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1122_basic/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-11-22", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-11-22"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1122_basic/session_0/demo_map.json",
}
CONFIG_1122_LONG = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1122_long/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-11-23", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-11-23"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1122_long/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [50,50,10],# 50 x 50 x 10 meters world boundary
}

class DUAL_1122_BASIC_1(Enum):
    CONFIG = CONFIG_1122_BASIC
    TEST_SET = DATASET_DEMO_1122_BASIC_1
    
class DUAL_1122_BASIC_2(Enum):
    CONFIG = CONFIG_1122_BASIC
    TEST_SET = DATASET_DEMO_1122_BASIC_2

class DUAL_1122_BASIC_ROG(Enum):
    CONFIG = CONFIG_1122_BASIC
    TEST_SET = DATASET_DEMO_1122_BASIC_ROGUE
    
class DUAL_1122_LONG(Enum):
    CONFIG = CONFIG_1122_LONG
    TEST_SET = DATASET_DEMO_1122_LONG_1
    
class DUAL_1122_LONG_ROG(Enum):
    CONFIG = CONFIG_1122_LONG
    TEST_SET = DATASET_DEMO_1122_LONG_ROGUE