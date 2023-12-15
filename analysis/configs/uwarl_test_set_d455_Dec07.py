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
class DATASET_DEMO_1207_A(Enum):
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
    FWD_D_0 = ["dual-0-18_DEMO-16_vins-replay.bag"]
    FWD_D_1 = ["dual-0-24_DEMO-16_vins-replay.bag"]
    FWD_D_2 = ["dual-0-25_DEMO-16_vins-replay.bag"]
    FWD_LR  = ["dual-0-20_DEMO-17_vins-replay.bag"]
    FWD_UD  = ["dual-0-22_DEMO-18_vins-replay.bag"]
    
    RVR_H   = ["dual-0-13_DEMO-19_vins-replay.bag"]
    RVR_E   = ["dual-0-15_DEMO-20_vins-replay.bag"]
    RVR_U   = ["dual-0-17_DEMO-21_vins-replay.bag"]
    RVR_D_0 = ["dual-0-19_DEMO-22_vins-replay.bag"]
    RVR_D_1 = ["dual-0-26_DEMO-22_vins-replay.bag"]
    RVR_LR  = ["dual-0-21_DEMO-23_vins-replay.bag"]
    RVR_UD  = ["dual-0-23_DEMO-24_vins-replay.bag"]
    
    CIR_E  = ["dual-1-1_DEMO-26_vins-replay.bag"]
    CIR_H  = ["dual-1-0_DEMO-25_vins-replay.bag"]
    CIR_U  = ["dual-1-2_DEMO-27_vins-replay.bag"]
    CIR_D  = ["dual-1-3_DEMO-28_vins-replay.bag"]
    CIR_LR = ["dual-1-4_DEMO-29_vins-replay.bag"]
    CIR_UD = ["dual-1-5_DEMO-30_vins-replay.bag"]
    
    SQR_H  = ["dual-2-0_DEMO-37_vins-replay.bag"]
    SQR_E  = ["dual-2-1_DEMO-38_vins-replay.bag"]
    SQR_U  = ["dual-2-2_DEMO-39_vins-replay.bag"]
    SQR_D  = ["dual-2-3_DEMO-40_vins-replay.bag"]
    SQR_LR = ["dual-2-4_DEMO-41_vins-replay.bag"]
    SQR_UD = ["dual-2-5_DEMO-42_vins-replay.bag"]
    
    TRI_H  = ["dual-2-6_DEMO-43_vins-replay.bag"]
    TRI_E  = ["dual-2-7_DEMO-44_vins-replay.bag"]
    TRI_U  = ["dual-2-8_DEMO-45_vins-replay.bag"]
    TRI_D  = ["dual-2-9_DEMO-46_vins-replay.bag"]
    TRI_LR = ["dual-2-10_DEMO-47_vins-replay.bag"]
    TRI_UD = ["dual-2-11_DEMO-48_vins-replay.bag"]

    L88_H_0 = ["dual-2-12_DEMO-49_vins-replay.bag"]
    L88_E_0 = ["dual-2-13_DEMO-50_vins-replay.bag"]
    L88_H_1 = ["dual-2-14_DEMO-49_vins-replay.bag"]
    L88_E_1 = ["dual-2-15_DEMO-50_vins-replay.bag"]
    
    
class DATASET_DEMO_1207_B(Enum):
    L88_H  = ["dual-0-0_DEMO-49_vins-replay.bag"]
    L88_E  = ["dual-0-1_DEMO-50_vins-replay.bag"]
    L88_U  = ["dual-0-2_DEMO-51_vins-replay.bag"]
    L88_D  = ["dual-0-3_DEMO-52_vins-replay.bag"]
    L88_LR = ["dual-0-4_DEMO-53_vins-replay.bag"]
    L88_UD = ["dual-0-5_DEMO-54_vins-replay.bag"]
    LSQ_H  = ["dual-1-0_DEMO-61_vins-replay.bag"]
    LSQ_E  = ["dual-1-1_DEMO-62_vins-replay.bag"]
    LSQ_U  = ["dual-1-2_DEMO-63_vins-replay.bag"]
    LSQ_D  = ["dual-1-3_DEMO-64_vins-replay.bag"]
    LSQ_LR = ["dual-1-4_DEMO-65_vins-replay.bag"]
    
    ROG_H   = ["dual-2-0_DEMO-55_vins-replay.bag"]
    ROG_E_0 = ["dual-2-1_DEMO-56_vins-replay.bag"]
    ROG_E_1 = ["dual-2-2_DEMO-56_vins-replay.bag"]
    ROG_U   = ["dual-2-3_DEMO-57_vins-replay.bag"]
    ROG_D   = ["dual-2-4_DEMO-58_vins-replay.bag"]
    ROG_LR  = ["dual-2-5_DEMO-59_vins-replay.bag"]
    ROG_UD  = ["dual-2-6_DEMO-60_vins-replay.bag"]

class DATASET_DEMO_1207_C1(Enum): 
    LO_E    = ["dual-0-0_DEMO-67_vins-replay.bag"]
    LO_H    = ["dual-0-1_DEMO-68_vins-replay.bag"]
    LO_U    = ["dual-0-2_DEMO-69_vins-replay.bag"]
    LO_D    = ["dual-0-3_DEMO-70_vins-replay.bag"]
    LO_LR   = ["dual-0-4_DEMO-71_vins-replay.bag"]
    LO_UD   = ["dual-0-5_DEMO-72_vins-replay.bag"]
    
    # glass window fog on
    FWD_E   = ["dual-1-0_DEMO-13_vins-replay.bag"]
    FWD_H   = ["dual-1-2_DEMO-14_vins-replay.bag"]
    FWD_U   = ["dual-1-4_DEMO-15_vins-replay.bag"]
    FWD_D   = ["dual-1-6_DEMO-16_vins-replay.bag"]
    FWD_LR  = ["dual-1-8_DEMO-17_vins-replay.bag"]
    FWD_UD  = ["dual-1-10_DEMO-18_vins-replay.bag"]

    RVR_E   = ["dual-1-1_DEMO-19_vins-replay.bag"]
    RVR_H   = ["dual-1-3_DEMO-20_vins-replay.bag"]
    RVR_U   = ["dual-1-5_DEMO-21_vins-replay.bag"]
    RVR_D   = ["dual-1-7_DEMO-22_vins-replay.bag"]
    RVR_LR  = ["dual-1-9_DEMO-23_vins-replay.bag"]
    RVR_UD  = ["dual-1-11_DEMO-24_vins-replay.bag"]

    SQR_E  = ["dual-1-12_DEMO-37_vins-replay.bag"]
    SQR_H  = ["dual-1-13_DEMO-38_vins-replay.bag"]
    SQR_U  = ["dual-1-14_DEMO-39_vins-replay.bag"]
    SQR_D  = ["dual-1-15_DEMO-40_vins-replay.bag"]
    SQR_LR = ["dual-1-16_DEMO-41_vins-replay.bag"]
    SQR_UD = ["dual-1-17_DEMO-42_vins-replay.bag"]

    OC1_SQR_E  = ["dual-2-0_DEMO-37_vins-replay.bag"]
    OC1_SQR_H  = ["dual-2-1_DEMO-38_vins-replay.bag"]
    OC1_SQR_U  = ["dual-2-2_DEMO-39_vins-replay.bag"]
    OC1_SQR_D  = ["dual-2-3_DEMO-40_vins-replay.bag"]
    OC1_SQR_LR = ["dual-2-4_DEMO-41_vins-replay.bag"]
    OC1_SQR_UD = ["dual-2-5_DEMO-42_vins-replay.bag"]

    OC2_SQR_E  = ["dual-3-0_DEMO-37_vins-replay.bag"]
    OC2_SQR_H  = ["dual-3-1_DEMO-38_vins-replay.bag"]
    OC2_SQR_U  = ["dual-3-2_DEMO-39_vins-replay.bag"]
    OC2_SQR_D  = ["dual-3-3_DEMO-40_vins-replay.bag"]
    OC2_SQR_LR = ["dual-3-4_DEMO-41_vins-replay.bag"]
    OC2_SQR_UD = ["dual-3-5_DEMO-42_vins-replay.bag"]# no power

    OC3_SQR_U  = ["dual-4-0_DEMO-39_vins-replay.bag"]# me walking in front
    OC3_SQR_LR = ["dual-4-1_DEMO-41_vins-replay.bag"]
    OC3_SQR_UD = ["dual-4-2_DEMO-42_vins-replay.bag"]# external force exerted

CONFIG_1207A = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1207A/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-12-12", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-12-12"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1207A/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}
CONFIG_1207A_v2 = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1207A/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-12-12", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom_v2/2023-12-13"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1207A/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}
CONFIG_1207A_v3 = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1207A/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-12-12", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom_v3/2023-12-13"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1207A/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}
CONFIG_1207B = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1207B/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-12-12", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-12-12"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1207B/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}
CONFIG_1207B_v3 = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1207B/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-12-12", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom_v3/2023-12-13"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1207B/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}
CONFIG_1207C = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1207C/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-12-12", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-12-12"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1207C/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}
CONFIG_1207C_v3 = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1207C/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-12-12", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom_v3/2023-12-13"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1207C/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}

class DEMO_1207_A(Enum):
    CONFIG = CONFIG_1207A
    TEST_SET = DATASET_DEMO_1207_A

class DEMO_1207_A_v2(Enum):
    CONFIG = CONFIG_1207A_v2
    TEST_SET = DATASET_DEMO_1207_A

class DEMO_1207_A_v3(Enum):
    CONFIG = CONFIG_1207A_v3
    TEST_SET = DATASET_DEMO_1207_A

class DEMO_1207_B(Enum):
    CONFIG = CONFIG_1207B
    TEST_SET = DATASET_DEMO_1207_B

class DEMO_1207_B_v3(Enum):
    CONFIG = CONFIG_1207B_v3
    TEST_SET = DATASET_DEMO_1207_B

class DEMO_1207_C(Enum):
    CONFIG = CONFIG_1207C
    TEST_SET = DATASET_DEMO_1207_C1

class DEMO_1207_C_v3(Enum):
    CONFIG = CONFIG_1207C_v3
    TEST_SET = DATASET_DEMO_1207_C1
