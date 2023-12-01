from enum import Enum

#   Base    \Arm:| Pt-FWD | Ext-F | Pt-Up | Pt-Down | **Pt-L/R| *Up-Down | 
#   Stationary   | 01   | 02     | 03    | 04      | 05      | 06       |       
#   *Spin        | 07   | 08     | 09    | 10      | 11      | 12       |
#   *FWD         | 13   | 14     | 15    | 16      | 17      | 18       |
#   *RVR         | 19   | 20     | 21    | 22      | 23      | 24       |
#   *Circling    | 25   | 26     | 27    | 28      | 29      | 30       |
#   88           | 31   | 32     | 33    | 34      | 35      | 36       |    
#
#   SQR.         | 37   | x      | 39    | x       | 41      | 42       |
#   TRI.         | 43   | x      | 45    | x       | 47      | 48       |
#
#   long-88:     | 49   | 50.    | 51    | 52      | 53      | 54     |
#   rogue.       | 55   | 56     | 57    | 58      | 59      | 60
#   sqr-4.       | 61   | 62.    | 63.   | 64      | 65.     | 66
#   long-O:	     | 67   | 68.    | 69.   | 70.     | 71.     | 72

from scipy.spatial.transform import Rotation as R
from utils.uwarl_bag_parser import TYPES_VAR

TEST_SET_TITLE = "D455"
####### 1101    Collection :
class DATASET_DEMO_1127_EVE_DEGEN(Enum):
    FWD_H   = ["dual-0-0_DEMO-13_vins-replay.bag"]
    FWD_E   = ["dual-0-2_DEMO-14_vins-replay.bag"]
    FWD_U   = ["dual-0-4_DEMO-15_vins-replay.bag"]
    FWD_D   = ["dual-0-6_DEMO-16_vins-replay.bag"]
    FWD_LR  = ["dual-0-8_DEMO-17_vins-replay.bag"]
    FWD_UD  = ["dual-0-10_DEMO-18_vins-replay.bag"]
      
    RVR_H   = ["dual-0-1_DEMO-19_vins-replay.bag"]
    RVR_E   = ["dual-0-3_DEMO-20_vins-replay.bag"]
    RVR_U   = ["dual-0-5_DEMO-21_vins-replay.bag"]
    RVR_D   = ["dual-0-7_DEMO-22_vins-replay.bag"]
    RVR_LR  = ["dual-0-9_DEMO-23_vins-replay.bag"]
    RVR_UD  = ["dual-0-11_DEMO-24_vins-replay.bag"]
    
class DATASET_DEMO_1127_EVE_DYNAMIC(Enum):
    CIR_H  = ["dual-0-12_DEMO-25_vins-replay.bag"]
    CIR_E  = ["dual-0-13_DEMO-26_vins-replay.bag"]
    CIR_U  = ["dual-0-14_DEMO-27_vins-replay.bag"]
    CIR_D  = ["dual-0-15_DEMO-28_vins-replay.bag"]
    CIR_LR = ["dual-0-16_DEMO-29_vins-replay.bag"]
    CIR_UD = ["dual-0-17_DEMO-30_vins-replay.bag"]
  
    BEE_H  = ["dual-0-18_DEMO-31_vins-replay.bag"]
    BEE_E  = ["dual-0-19_DEMO-32_vins-replay.bag"]
    BEE_U  = ["dual-0-20_DEMO-33_vins-replay.bag"]
    BEE_D  = ["dual-0-21_DEMO-34_vins-replay.bag"]
    BEE_LR = ["dual-1-0_DEMO-35_vins-replay.bag"]
    BEE_UD = ["dual-1-1_DEMO-36_vins-replay.bag"]
  
    SQR_H  = ["dual-1-2_DEMO-37_vins-replay.bag"]
    SQR_E  = ["dual-1-3_DEMO-38_vins-replay.bag"]
    SQR_U  = ["dual-1-4_DEMO-39_vins-replay.bag"]
    SQR_D  = ["dual-1-5_DEMO-40_vins-replay.bag"]
    SQR_LR = ["dual-1-6_DEMO-41_vins-replay.bag"]
    SQR_UD = ["dual-1-7_DEMO-42_vins-replay.bag"]
  
    TRI_H  = ["dual-2-0_DEMO-43_vins-replay.bag"]
    TRI_E  = ["dual-2-1_DEMO-44_vins-replay.bag"]
    TRI_U  = ["dual-2-2_DEMO-45_vins-replay.bag"]
    TRI_D  = ["dual-2-3_DEMO-46_vins-replay.bag"]
    TRI_LR = ["dual-2-4_DEMO-47_vins-replay.bag"]
    TRI_UD = ["dual-2-5_DEMO-48_vins-replay.bag"]

CONFIG_1127_EVENING = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1127_ev/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-11-28", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-11-30"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1127_ev/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [50,50,10],# 50 x 50 x 10 meters world boundary
}

class DATASET_DEMO_1127_PM_LONG(Enum):
    # L_BEE_H   =[""]
    # L_BEE_E   =[""]
    # L_BEE_U   =[""]
    L_BEE_D   =["dual-0-0_DEMO-52_vins-replay.bag"]
    L_BEE_LR  =["dual-0-1_DEMO-53_vins-replay.bag"]
    L_BEE_UD  =["dual-0-2_DEMO-54_vins-replay.bag"]
    
    L_SQR_H   =["dual-0-3_DEMO-61_vins-replay.bag"]
    L_SQR_E   =["dual-0-4_DEMO-62_vins-replay.bag"]
    L_SQR_U   =["dual-0-5_DEMO-63_vins-replay.bag"]
    L_SQR_D   =["dual-0-6_DEMO-64_vins-replay.bag"]
    L_SQR_LR  =["dual-0-7_DEMO-65_vins-replay.bag"]
    L_SQR_UD  =["dual-0-8_DEMO-66_vins-replay.bag"]
    
    ROGUE_H   =["dual-1-0_DEMO-55_vins-replay.bag"]
    ROGUE_LR  =["dual-1-3_DEMO-59_vins-replay.bag"]
    ROGUE_UD  =["dual-1-1_DEMO-60_vins-replay.bag"]
    
    L_CIR_H   =["dual-2-0_DEMO-67_vins-replay.bag"]
    L_CIR_E   =["dual-2-1_DEMO-68_vins-replay.bag"]
    L_CIR_LR  =["dual-2-3_DEMO-71_vins-replay.bag"]
    L_CIR_UD  =["dual-2-2_DEMO-72_vins-replay.bag"]

CONFIG_1127_AFTERNOON = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1127_pm/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-11-28", 
        # "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-11-28"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1127_pm/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [50,50,10],# 50 x 50 x 10 meters world boundary
}

class DATASET_DEMO_1127_AM_DEGEN(Enum):
    STA_H   = ["dual-0-0_DEMO-1_vins-replay.bag"]
    STA_E   = ["dual-0-1_DEMO-2_vins-replay.bag"]
    STA_U   = ["dual-0-2_DEMO-3_vins-replay.bag"]
    STA_D   = ["dual-0-3_DEMO-4_vins-replay.bag"]
    STA_LR  = ["dual-0-4_DEMO-5_vins-replay.bag"]
    STA_UD  = ["dual-0-5_DEMO-6_vins-replay.bag"]
    
    SPI_H   = ["dual-0-6_DEMO-7_vins-replay.bag"]
    SPI_E   = ["dual-0-7_DEMO-8_vins-replay.bag"]
    SPI_U   = ["dual-0-8_DEMO-9_vins-replay.bag"]
    SPI_D   = ["dual-0-9_DEMO-10_vins-replay.bag"]
    SPI_LR  = ["dual-0-10_DEMO-11_vins-replay.bag"]
    SPI_UD  = ["dual-0-11_DEMO-12_vins-replay.bag"]
    
    FWD_H   = ["dual-0-12_DEMO-13_vins-replay.bag"]
    FWD_E   = ["dual-0-14_DEMO-14_vins-replay.bag"]
    FWD_U   = ["dual-0-16_DEMO-15_vins-replay.bag"]
    FWD_D   = ["dual-0-18_DEMO-16_vins-replay.bag"]
    FWD_LR  = ["dual-0-20_DEMO-17_vins-replay.bag"]
    FWD_UD  = ["dual-0-22_DEMO-18_vins-replay.bag"]
  
    RVR_H   = ["dual-0-13_DEMO-19_vins-replay.bag"]
    RVR_E   = ["dual-0-15_DEMO-20_vins-replay.bag"]
    RVR_U   = ["dual-0-17_DEMO-21_vins-replay.bag"]
    RVR_D   = ["dual-0-19_DEMO-22_vins-replay.bag"]
    RVR_LR  = ["dual-0-21_DEMO-23_vins-replay.bag"]
    RVR_UD  = ["dual-0-23_DEMO-24_vins-replay.bag"]
    
class DATASET_DEMO_1127_AM_DYNAMIC(Enum):
    CIR_H  = ["dual-0-24_DEMO-25_vins-replay.bag"]
    CIR_E  = ["dual-0-25_DEMO-26_vins-replay.bag"]
    CIR_U  = ["dual-0-26_DEMO-27_vins-replay.bag"]
    CIR_D  = ["dual-0-27_DEMO-28_vins-replay.bag"]
    CIR_LR = ["dual-0-28_DEMO-29_vins-replay.bag"]
    CIR_UD = ["dual-0-29_DEMO-30_vins-replay.bag"]
  
    BEE_H  = ["dual-0-30_DEMO-31_vins-replay.bag"]
    BEE_E  = ["dual-0-31_DEMO-32_vins-replay.bag"]
    BEE_U  = ["dual-0-32_DEMO-33_vins-replay.bag"]
    BEE_D  = ["dual-0-33_DEMO-34_vins-replay.bag"]
    BEE_LR = ["dual-0-34_DEMO-35_vins-replay.bag"]
    BEE_UD = ["dual-0-35_DEMO-36_vins-replay.bag"]
  
    SQR_H  = ["dual-0-36_DEMO-37_vins-replay.bag"]
    SQR_E  = ["dual-0-37_DEMO-38_vins-replay.bag"]
    SQR_U  = ["dual-0-38_DEMO-39_vins-replay.bag"]
    SQR_D  = ["dual-0-39_DEMO-40_vins-replay.bag"]
    SQR_LR = ["dual-0-40_DEMO-41_vins-replay.bag"]
    # SQR_UD = [""]
  
    TRI_H  = ["dual-0-41_DEMO-43_vins-replay.bag"]
    TRI_E  = ["dual-0-42_DEMO-44_vins-replay.bag"]
    TRI_U  = ["dual-0-43_DEMO-45_vins-replay.bag"]
    TRI_D  = ["dual-0-44_DEMO-46_vins-replay.bag"]
    TRI_LR = ["dual-0-45_DEMO-47_vins-replay.bag"]
    TRI_UD = ["dual-0-46_DEMO-48_vins-replay.bag"]
    
    L_BEE_H   =["dual-1-0_DEMO-49_vins-replay.bag"]
    L_BEE_E   =["dual-1-1_DEMO-50_vins-replay.bag"]
    L_BEE_U   =["dual-1-2_DEMO-51_vins-replay.bag"]

CONFIG_1127_MORNING = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1127_am/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-11-28", 
        # "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-11-28"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1127_am/session_0/demo_map.json",
}

class DUAL_1127_DEG_EVE(Enum):
    CONFIG = CONFIG_1127_EVENING
    TEST_SET = DATASET_DEMO_1127_EVE_DEGEN

class DUAL_1127_DYN_EVE(Enum):
    CONFIG = CONFIG_1127_EVENING
    TEST_SET = DATASET_DEMO_1127_EVE_DYNAMIC
    
class DUAL_1127_DEG_AM(Enum):
    CONFIG = CONFIG_1127_MORNING
    TEST_SET = DATASET_DEMO_1127_AM_DEGEN

class DUAL_1127_DYN_AM(Enum):
    CONFIG = CONFIG_1127_MORNING
    TEST_SET = DATASET_DEMO_1127_AM_DYNAMIC

class DUAL_1127_LONG_PM(Enum):
    CONFIG = CONFIG_1127_AFTERNOON
    TEST_SET = DATASET_DEMO_1127_PM_LONG

