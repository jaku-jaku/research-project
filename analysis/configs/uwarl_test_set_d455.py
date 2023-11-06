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

class DUAL_MONO_IMU_1101_1104_baseline(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": "S-1_E-1_dual_baseline/2023-11-04",
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL
class DUAL_MONO_IMU_1101_1104_armOdom(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": "S-1_E-1_dual_arm_odom/2023-11-04",
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL

class DUAL_MONO_IMU_1101_1104_comparison(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_baseline/2023-11-04", 
            "arm_odom": "S-1_E-1_dual_arm_odom/2023-11-04"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL
class DUAL_MONO_IMU_1101_1104_comparison_v2(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_baseline/2023-11-04", 
            "arm_odom": "S-1_E-1_dual_arm_odom_v2/2023-11-05"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL

class DUAL_MONO_IMU_1101_1104_comparison_v3(Enum):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1101/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_baseline/2023-11-04", 
            "arm_odom": "S-1_E-1_dual_arm_odom_v3/2023-11-06"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1101/session_1/demo_map.json",
    }
    TEST_SET = DATASET_DEMO_1101_MONO_RGB_DUAL_ALL

