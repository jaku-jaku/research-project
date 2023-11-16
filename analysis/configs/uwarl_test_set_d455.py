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
class DATASET_DEMO_1101_MONO_RGB_DUAL_ALL(Enum):
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
    
    SQR_H  = ["dual-1-1_DEMO-37_vins-replay.bag"]
    SQR_E  = ["dual-1-2_DEMO-38_vins-replay.bag"]

class DUAL_MONO_IMU_1101_1106_comparison(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_arm_baseline/2023-11-06", 
            "arm_odom(B2E)": "S-1_E-1_dual_arm_odometry/2023-11-06"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL

class DUAL_MONO_IMU_1101_1106_base_vs_both(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_arm_baseline/2023-11-06", 
            "arm_odom(both)": "S-1_E-1_dual_arm_odometry_both/2023-11-06"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL

class DUAL_MONO_IMU_1101_1106_arm_vs_both(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": {
            "arm_odom(B2E)": "S-1_E-1_dual_arm_odometry/2023-11-06", 
            "arm_odom(both)": "S-1_E-1_dual_arm_odometry_both/2023-11-06"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL

class DUAL_MONO_IMU_1101_1106_arm_vs_all(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_arm_baseline/2023-11-06", 
            "arm_odom(B2E)": "S-1_E-1_dual_arm_odometry/2023-11-06", 
            "arm_odom(both)": "S-1_E-1_dual_arm_odometry_both/2023-11-06"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL

class DUAL_MONO_IMU_1101_1107_base_vs_both(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_arm_baseline/2023-11-07", 
            "arm_odom(both)": "S-1_E-1_dual_arm_odometry_both/2023-11-07"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL


####### 1108    Collection :
class DATASET_DEMO_1108_BASICS(Enum):
    SPI_H   = ["dual-0-1_DEMO-7_vins-replay.bag"]
    SPI_E   = ["dual-0-2_DEMO-8_vins-replay.bag"]
    SPI_U   = ["dual-0-3_DEMO-9_vins-replay.bag"]
    SPI_D   = ["dual-0-4_DEMO-10_vins-replay.bag"]
    SPI_LR  = ["dual-0-5_DEMO-11_vins-replay.bag"]
    SPI_UD  = ["dual-0-6_DEMO-12_vins-replay.bag"]
    
    # driving facing towards checkerboard 
    FWD_H   = ["dual-0-7_DEMO-13_vins-replay.bag"]
    FWD_E   = ["dual-0-9_DEMO-14_vins-replay.bag"]
    FWD_U   = ["dual-0-11_DEMO-15_vins-replay.bag"]
    FWD_D   = ["dual-0-13_DEMO-16_vins-replay.bag"]
    FWD_LR  = ["dual-0-15_DEMO-17_vins-replay.bag"]
    FWD_UD  = ["dual-0-17_DEMO-18_vins-replay.bag"]
    
    RVR_H   = ["dual-0-8_DEMO-19_vins-replay.bag"]
    RVR_E   = ["dual-0-10_DEMO-20_vins-replay.bag"]
    RVR_U   = ["dual-0-12_DEMO-21_vins-replay.bag"]
    RVR_D   = ["dual-0-14_DEMO-22_vins-replay.bag"]
    RVR_LR  = ["dual-0-16_DEMO-23_vins-replay.bag"]
    RVR_UD  = ["dual-0-18_DEMO-24_vins-replay.bag"]
    
    # not seeing checkerboard
    FWD_H_NB   = ["dual-1-1_DEMO-13_vins-replay.bag"]
    FWD_E_NB   = ["dual-1-3_DEMO-14_vins-replay.bag"]
    FWD_U_NB   = ["dual-1-5_DEMO-15_vins-replay.bag"]
    FWD_D_NB   = ["dual-1-7_DEMO-16_vins-replay.bag"]
    FWD_LR_NB  = ["dual-1-9_DEMO-17_vins-replay.bag"]
    FWD_UD_NB  = ["dual-1-11_DEMO-18_vins-replay.bag"]
    
    RVR_H_NB   = ["dual-1-2_DEMO-19_vins-replay.bag"]
    RVR_E_NB   = ["dual-1-4_DEMO-20_vins-replay.bag"]
    RVR_U_NB   = ["dual-1-6_DEMO-21_vins-replay.bag"]
    RVR_D_NB   = ["dual-1-8_DEMO-22_vins-replay.bag"]
    RVR_LR_NB  = ["dual-1-10_DEMO-23_vins-replay.bag"]
    RVR_UD_NB  = ["dual-1-12_DEMO-24_vins-replay.bag"]

class DATASET_DEMO_1108_DYNAMICS(Enum):
    # Circular motion
    CIR_H  = ["dual-2-0_DEMO-25_vins-replay.bag"]
    CIR_E  = ["dual-2-1_DEMO-26_vins-replay.bag"]
    CIR_U  = ["dual-2-2_DEMO-27_vins-replay.bag"]
    CIR_D  = ["dual-2-3_DEMO-28_vins-replay.bag"]
    CIR_LR = ["dual-2-4_DEMO-29_vins-replay.bag"]
    CIR_UD = ["dual-2-5_DEMO-30_vins-replay.bag"]
    # BEE motion 8
    BEE_H  = ["dual-2-6_DEMO-31_vins-replay.bag"]
    BEE_E  = ["dual-2-7_DEMO-32_vins-replay.bag"]
    BEE_U  = ["dual-2-8_DEMO-33_vins-replay.bag"]
    BEE_D  = ["dual-2-9_DEMO-34_vins-replay.bag"]
    BEE_LR = ["dual-2-10_DEMO-35_vins-replay.bag"]
    BEE_UD = ["dual-2-11_DEMO-36_vins-replay.bag"]
    # Square
    SQR_H  = ["dual-2-13_DEMO-37_vins-replay.bag"]
    SQR_E  = ["dual-2-14_DEMO-38_vins-replay.bag"]
    SQR_U  = ["dual-2-15_DEMO-39_vins-replay.bag"]
    SQR_D  = ["dual-2-16_DEMO-40_vins-replay.bag"]
    SQR_LR = ["dual-2-17_DEMO-41_vins-replay.bag"]
    SQR_UD = ["dual-2-18_DEMO-42_vins-replay.bag"]
    
    TRI_H  = ["dual-2-19_DEMO-43_vins-replay.bag"]
    TRI_E  = ["dual-2-20_DEMO-44_vins-replay.bag"]
    TRI_U  = ["dual-2-21_DEMO-45_vins-replay.bag"]
    TRI_D  = ["dual-2-22_DEMO-46_vins-replay.bag"]
    TRI_LR = ["dual-2-23_DEMO-47_vins-replay.bag"]
    TRI_UD = ["dual-2-24_DEMO-48_vins-replay.bag"]
    
class DATASET_DEMO_1108_LONG_AM(Enum):
    # 3 mins: 
    BEE_H  = ["dual-2-25_DEMO-49_vins-replay.bag"]
    # BEE_E  = []
    # BEE_U  = []
    BEE_D  = ["dual-2-28_DEMO-52_vins-replay.bag"]
    BEE_LR = ["dual-2-27_DEMO-53_vins-replay.bag"]
    BEE_UD = ["dual-2-26_DEMO-54_vins-replay.bag"]

class DATASET_DEMO_1108_LONG_PM(Enum): 
    # Tim base base trajectory follower - contains amcl:
    TIM_1= ["dual-0-0_DEMO-1_vins-replay.bag"]
    TIM_2= ["dual-0-1_DEMO-1_vins-replay.bag"]
    # contains amcl:
    BEE_H= ["dual-0-2_DEMO-49_vins-replay.bag"]
    BEE_E= ["dual-0-3_DEMO-50_vins-replay.bag"]
    BEE_U= ["dual-0-4_DEMO-51_vins-replay.bag"]
    # x rogue
    ROG_RH    = ["dual-0-5_DEMO-60_vins-replay.bag"]
    ROG_123   = ["dual-1-0_DEMO-55_vins-replay.bag"] # 1st to second floor
    ROG_3_LR  = ["dual-3-0_DEMO-59_vins-replay.bag"]
    ROG_3_U   = ["dual-3-1_DEMO-57_vins-replay.bag"]


CONFIG_1108_AM = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_1108_am/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-11-09", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-11-09"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_1108_am/session_0/demo_map.json",
}
CONFIG_1108_PM = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_1108_pm/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-11-09", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-11-09"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_1108_pm/session_0/demo_map.json",
    "AXIS_BOUNDARY_MAX": [50,50,10],# 50 x 50 x 10 meters world boundary
}
class DUAL_1108_BASICS_baseline_vs_decoupled(Enum):
    CONFIG = CONFIG_1108_AM
    TEST_SET = DATASET_DEMO_1108_BASICS

class DUAL_1108_DYNAMICS_baseline_vs_decoupled(Enum):
    CONFIG = CONFIG_1108_AM
    TEST_SET = DATASET_DEMO_1108_DYNAMICS

class DUAL_1108_LONG_AM_baseline_vs_decoupled(Enum):
    CONFIG = CONFIG_1108_AM
    TEST_SET = DATASET_DEMO_1108_LONG_AM
    
class DUAL_1108_LONG_PM_baseline_vs_decoupled(Enum):
    CONFIG = CONFIG_1108_PM
    TEST_SET = DATASET_DEMO_1108_LONG_PM

