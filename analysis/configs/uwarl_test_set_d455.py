from enum import Enum
from pathlib import Path

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

class DATASET_DEMO_0612_MONO_RGB_DUAL(Enum):
    SQR_39 = ["dual-1-0_DEMO-39_vins-replay.bag"]

class DATASET_DEMO_0612_MONO_RGB_DUAL_ALL(Enum):
    SPIN_07 = ["dual-0-0_DEMO-7_vins-replay.bag"]
    
    BEE_31 = ["dual-0-19_DEMO-31_vins-replay.bag"]
    BEE_32 = ["dual-0-20_DEMO-32_vins-replay.bag"]
    BEE_33 = ["dual-0-21_DEMO-33_vins-replay.bag"]
    BEE_34 = ["dual-0-22_DEMO-34_vins-replay.bag"]
    BEE_35 = ["dual-0-24_DEMO-35_vins-replay.bag"]
    BEE_36 = ["dual-0-25_DEMO-36_vins-replay.bag"]

    CIRC_25 = ["dual-0-13_DEMO-25_vins-replay.bag"]
    CIRC_26 = ["dual-0-14_DEMO-26_vins-replay.bag"]
    CIRC_27 = ["dual-0-15_DEMO-27_vins-replay.bag"]
    CIRC_28 = ["dual-0-16_DEMO-28_vins-replay.bag"]
    CIRC_29 = ["dual-0-17_DEMO-29_vins-replay.bag"]
    CIRC_30 = ["dual-0-18_DEMO-30_vins-replay.bag"]
    
    FWD_13 = ["dual-0-1_DEMO-13_vins-replay.bag"]
    FWD_14 = ["dual-0-3_DEMO-14_vins-replay.bag"]
    FWD_15 = ["dual-0-5_DEMO-15_vins-replay.bag"]
    FWD_16 = ["dual-0-7_DEMO-16_vins-replay.bag"]
    FWD_17 = ["dual-0-9_DEMO-17_vins-replay.bag"]
    FWD_18 = ["dual-0-11_DEMO-18_vins-replay.bag"]

    RVR_19 = ["dual-0-2_DEMO-19_vins-replay.bag"]
    RVR_20 = ["dual-0-4_DEMO-20_vins-replay.bag"]
    RVR_21 = ["dual-0-6_DEMO-21_vins-replay.bag"]
    RVR_22 = ["dual-0-8_DEMO-22_vins-replay.bag"]
    RVR_23 = ["dual-0-10_DEMO-23_vins-replay.bag"]
    RVR_24 = ["dual-0-12_DEMO-24_vins-replay.bag"]
    
    SQR_37 = ["dual-1-0_DEMO-37_vins-replay.bag"]
    SQR_39 = ["dual-1-1_DEMO-39_vins-replay.bag"]
    SQR_41 = ["dual-1-2_DEMO-41_vins-replay.bag"]
    SQR_42 = ["dual-1-3_DEMO-42_vins-replay.bag"]
    TRI_43 = ["dual-1-4_DEMO-43_vins-replay.bag"]
    TRI_47 = ["dual-1-5_DEMO-47_vins-replay.bag"]
    
    ROGUE_1 = ["dual-1-6_DEMO-1_vins-replay.bag"]
    ROGUE_2 = ["dual-1-7_DEMO-1_vins-replay.bag"]

class TEST_SET_DUAL_MONO_IMU_0612_1010(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual/2023-10-10",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL
class TEST_SET_DUAL_MONO_IMU_0612_1011(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual/2023-10-11",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_ALL

class TEST_SET_DUAL_MONO_IMU_0612_1017_v4(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v4/2023-10-17",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v4/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_ALL
class TEST_SET_DUAL_MONO_IMU_0612_1018_v6(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v6/2023-10-18",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v6/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_ALL
class TEST_SET_DUAL_MONO_IMU_0612_1019_v7(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v7/2023-10-19",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v7/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_ALL

class TEST_SET_DUAL_MONO_IMU_0612_1019_v9(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v9/2023-10-19",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v9/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_ALL
class TEST_SET_DUAL_MONO_IMU_0612_1022_v10(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v10/2023-10-22",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v10/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_ALL
class TEST_SET_DUAL_MONO_IMU_0612_1022_v11(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v11/2023-10-22",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v11/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_ALL
