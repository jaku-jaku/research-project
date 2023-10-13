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

#### BATCH TESTS 05 04 2023 ####
class DATASET_DEMO_0504_MONO_RGB(Enum):
    ExtF = [
    ]
    Spin_7 = [
        "base-1-0_DEMO-7_vins-replay.bag",
        "EE-1-0_DEMO-7_vins-replay.bag",
    ]
    Spin_8 = [
        "base-1-1_DEMO-8_vins-replay.bag",
        "EE-1-1_DEMO-8_vins-replay.bag",
    ]
    Spin_9 = [
        "base-1-2_DEMO-9_vins-replay.bag",
        "EE-1-2_DEMO-9_vins-replay.bag",
    ]
    Spin_10 = [
        "base-1-3_DEMO-10_vins-replay.bag",
        "EE-1-3_DEMO-10_vins-replay.bag",
    ]
    Spin_11 = [
        "base-1-4_DEMO-11_vins-replay.bag",
        "EE-1-4_DEMO-11_vins-replay.bag",
    ]
    Spin_12 = [
        "base-1-5_DEMO-12_vins-replay.bag",     
        "EE-1-5_DEMO-12_vins-replay.bag",     
    ]
    FWD_13 = [
        "base-0-0_DEMO-13_vins-replay.bag",
        "EE-0-0_DEMO-13_vins-replay.bag",
    ]
    FWD_13v2 = [
        "base-0-12_DEMO-13_vins-replay.bag",
        "EE-0-12_DEMO-13_vins-replay.bag",
    ]
    FWD_14 = [
        "base-0-2_DEMO-14_vins-replay.bag",
        "EE-0-2_DEMO-14_vins-replay.bag",
    ]
    FWD_15 = [
        "base-0-4_DEMO-15_vins-replay.bag",
        "EE-0-4_DEMO-15_vins-replay.bag",
    ]
    FWD_16 = [
        "base-0-6_DEMO-16_vins-replay.bag",
        "EE-0-6_DEMO-16_vins-replay.bag",
    ]
    FWD_17 = [
        "base-0-8_DEMO-17_vins-replay.bag",
        "EE-0-8_DEMO-17_vins-replay.bag",
    ]
    FWD_18 = [
        "base-0-10_DEMO-18_vins-replay.bag",     
        "EE-0-10_DEMO-18_vins-replay.bag",     
    ]
    RVR_19 = [
        "base-0-1_DEMO-19_vins-replay.bag",
        "EE-0-1_DEMO-19_vins-replay.bag",
    ]
    RVR_20 = [
        "base-0-3_DEMO-20_vins-replay.bag",
        "EE-0-3_DEMO-20_vins-replay.bag",
    ]
    RVR_21 = [
        "base-0-5_DEMO-21_vins-replay.bag",
        "EE-0-5_DEMO-21_vins-replay.bag",
    ]
    RVR_22 = [
        "base-0-7_DEMO-22_vins-replay.bag",
        "EE-0-7_DEMO-22_vins-replay.bag",
    ]
    RVR_23 = [
        "base-0-9_DEMO-23_vins-replay.bag",
        "EE-0-9_DEMO-23_vins-replay.bag",
    ]
    RVR_24 = [
        "base-0-11_DEMO-24_vins-replay.bag",
        "EE-0-11_DEMO-24_vins-replay.bag",
    ]
    CIR_25 = [
        "base-2-0_DEMO-25_vins-replay.bag",
        "EE-2-0_DEMO-25_vins-replay.bag",
    ]
    CIR_26 = [
        "base-2-1_DEMO-26_vins-replay.bag",
        "EE-2-1_DEMO-26_vins-replay.bag",
    ]
    CIR_27 = [
        "base-2-2_DEMO-27_vins-replay.bag",
        "EE-2-2_DEMO-27_vins-replay.bag",
    ]
    CIR_28 = [
        "base-2-3_DEMO-28_vins-replay.bag",
        "EE-2-3_DEMO-28_vins-replay.bag",
    ]
    CIR_29 = [
        "base-2-4_DEMO-29_vins-replay.bag",
        "EE-2-4_DEMO-29_vins-replay.bag",
    ]
    CIR_29v2 = [
        "base-2-6_DEMO-29_vins-replay.bag",
        "EE-2-6_DEMO-29_vins-replay.bag",
    ]
    CIR_30 = [
        "base-2-5_DEMO-30_vins-replay.bag",
        "EE-2-5_DEMO-30_vins-replay.bag",
    ]
    BEE_31 = [
        "base-2-7_DEMO-31_vins-replay.bag",
        "EE-2-7_DEMO-31_vins-replay.bag",
    ]
    BEE_31v2 = [
        "base-2-8_DEMO-31_vins-replay.bag",
        "EE-2-8_DEMO-31_vins-replay.bag",
    ]
    BEE_33 = [
        "base-2-9_DEMO-33_vins-replay.bag",
        "EE-2-9_DEMO-33_vins-replay.bag",
    ]
    BEE_34 = [
        "base-2-10_DEMO-34_vins-replay.bag",
        "EE-2-10_DEMO-34_vins-replay.bag",
    ]
    BEE_35 = [
        "base-2-11_DEMO-35_vins-replay.bag",
        "EE-2-11_DEMO-35_vins-replay.bag",
    ]
    BEE_36 = [
        "base-2-12_DEMO-36_vins-replay.bag",
        "EE-2-12_DEMO-36_vins-replay.bag",
    ]

class TEST_SET_MONO_RGB_IMU(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1-1/2023-05-05",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0504/session_5/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_TIC(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ic/2023-05-07",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0504/session_5/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_INIT_GUESS_TIC(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_init_guess_T_ic/2023-05-08",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0504/session_5/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB
class TEST_SET_MONO_RGB_IMU_ACC_TCI(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ci/2023-05-08",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0504/session_5/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_TIC_MANUFACTURED(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ic_manufactured/2023-05-08",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0504/session_5/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_TIC_V2(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ic_v2/2023-05-08",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0504/session_5/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_TIC_V5(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ic_v5/2023-05-10",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0504/session_5/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB


#### BATCH TESTS 05 11 2023 ####
class DATASET_DEMO_0511_MONO_RGB(Enum):
    BEE_31 = [
        "base-2-1_DEMO-31_vins-replay.bag",
        "EE-2-1_DEMO-31_vins-replay.bag",
    ]
    BEE_32 = [
        "base-2-2_DEMO-32_vins-replay.bag",
        "EE-2-2_DEMO-32_vins-replay.bag",
    ]
    BEE_33 = [
        "base-2-3_DEMO-33_vins-replay.bag",
        "EE-2-3_DEMO-33_vins-replay.bag",
    ]
    BEE_34 = [
        "base-2-4_DEMO-34_vins-replay.bag",
        "EE-2-4_DEMO-34_vins-replay.bag",
    ]
    BEE_35 = [
        "base-2-5_DEMO-35_vins-replay.bag",
        "EE-2-5_DEMO-35_vins-replay.bag",
    ]
    BEE_36 = [
        "base-2-6_DEMO-36_vins-replay.bag",
        "EE-2-6_DEMO-36_vins-replay.bag",
    ]

    SPIN_07 = [
        "base-1-13_DEMO-7_vins-replay.bag",
        "EE-1-13_DEMO-7_vins-replay.bag",
    ]
    SPIN_08 = [
        "base-1-14_DEMO-8_vins-replay.bag",
        "EE-1-14_DEMO-8_vins-replay.bag",
    ]
    SPIN_09 = [
        "base-1-15_DEMO-9_vins-replay.bag",
        "EE-1-15_DEMO-9_vins-replay.bag",
    ]
    SPIN_10 = [
        "base-1-16_DEMO-10_vins-replay.bag",
        "EE-1-16_DEMO-10_vins-replay.bag",
    ]
    SPIN_11 = [
        "base-1-17_DEMO-11_vins-replay.bag",
        "EE-1-17_DEMO-11_vins-replay.bag",
    ]

    CIRC_25 = [
        "base-1-18_DEMO-25_vins-replay.bag",
        "EE-1-18_DEMO-25_vins-replay.bag",
    ]
    CIRC_26 = [
        "base-1-19_DEMO-26_vins-replay.bag",
        "EE-1-19_DEMO-26_vins-replay.bag",
    ]
    CIRC_27 = [
        "base-1-20_DEMO-27_vins-replay.bag",
        "EE-1-20_DEMO-27_vins-replay.bag",
    ]
    CIRC_28 = [
        "base-1-21_DEMO-28_vins-replay.bag",
        "EE-1-21_DEMO-28_vins-replay.bag",
    ]
    CIRC_29 = [
        "base-1-22_DEMO-29_vins-replay.bag",
        "EE-1-22_DEMO-29_vins-replay.bag",
    ]
    
    FWD_13_NO_BOARD = [
        "base-0-1_DEMO-13_vins-replay.bag",
        "EE-0-1_DEMO-13_vins-replay.bag",
    ]
    FWD_14_NO_BOARD = [
        "base-0-3_DEMO-14_vins-replay.bag",
        "EE-0-3_DEMO-14_vins-replay.bag",
    ]
    FWD_15_NO_BOARD = [
        "base-0-6_DEMO-15_vins-replay.bag",
        "EE-0-6_DEMO-15_vins-replay.bag",
    ]
    FWD_16_NO_BOARD = [
        "base-0-8_DEMO-16_vins-replay.bag",
        "EE-0-8_DEMO-16_vins-replay.bag",
    ]
    FWD_17_NO_BOARD = [
        "base-0-10_DEMO-17_vins-replay.bag",
        "EE-0-10_DEMO-17_vins-replay.bag",
    ]
    FWD_18_NO_BOARD = [
        "base-0-12_DEMO-18_vins-replay.bag",
        "EE-0-12_DEMO-18_vins-replay.bag",
    ]

    RVR_19_NO_BOARD = [
        "base-0-2_DEMO-19_vins-replay.bag",
        "EE-0-2_DEMO-19_vins-replay.bag",
    ]
    RVR_20_NO_BOARD = [
        "base-0-5_DEMO-20_vins-replay.bag",
        "EE-0-5_DEMO-20_vins-replay.bag",
    ]
    RVR_21_NO_BOARD = [
        "base-0-7_DEMO-21_vins-replay.bag",
        "EE-0-7_DEMO-21_vins-replay.bag",
    ]
    RVR_22_NO_BOARD = [
        "base-0-9_DEMO-22_vins-replay.bag",
        "EE-0-9_DEMO-22_vins-replay.bag",
    ]
    RVR_23_NO_BOARD = [
        "base-0-11_DEMO-23_vins-replay.bag",
        "EE-0-11_DEMO-23_vins-replay.bag",
    ]
    RVR_24_NO_BOARD = [
        "base-0-13_DEMO-24_vins-replay.bag",
        "EE-0-13_DEMO-24_vins-replay.bag",
    ]

    FWD_13 = [
        "base-1-0_DEMO-13_vins-replay.bag",
        "EE-1-0_DEMO-13_vins-replay.bag",
    ]
    FWD_14 = [
        "base-1-2_DEMO-14_vins-replay.bag",
        "EE-1-2_DEMO-14_vins-replay.bag",
    ]
    FWD_15 = [
        "base-1-5_DEMO-15_vins-replay.bag",
        "EE-1-5_DEMO-15_vins-replay.bag",
    ]
    FWD_16 = [
        "base-1-7_DEMO-16_vins-replay.bag",
        "EE-1-7_DEMO-16_vins-replay.bag",
    ]
    FWD_17 = [
        "base-1-9_DEMO-17_vins-replay.bag",
        "EE-1-9_DEMO-17_vins-replay.bag",
    ]
    FWD_18 = [
        "base-1-11_DEMO-18_vins-replay.bag",
        "EE-1-11_DEMO-18_vins-replay.bag",
    ]

    RVR_19 = [
        "base-1-1_DEMO-19_vins-replay.bag",
        "EE-1-1_DEMO-19_vins-replay.bag",
    ]
    RVR_20 = [
        "base-1-4_DEMO-20_vins-replay.bag",
        "EE-1-4_DEMO-20_vins-replay.bag",
    ]
    RVR_21 = [
        "base-1-6_DEMO-21_vins-replay.bag",
        "EE-1-6_DEMO-21_vins-replay.bag",
    ]
    RVR_22 = [
        "base-1-8_DEMO-22_vins-replay.bag",
        "EE-1-8_DEMO-22_vins-replay.bag",
    ]
    RVR_23 = [
        "base-1-10_DEMO-23_vins-replay.bag",
        "EE-1-10_DEMO-23_vins-replay.bag",
    ]
    RVR_24 = [
        "base-1-12_DEMO-24_vins-replay.bag",
        "EE-1-12_DEMO-24_vins-replay.bag",
    ]

    STATIONARY_3 = [
        "base-3-0_DEMO-3_vins-replay.bag",
        "EE-3-0_DEMO-3_vins-replay.bag",
    ]
    STATIONARY_5 = [
        "base-3-1_DEMO-5_vins-replay.bag",
        "EE-3-1_DEMO-5_vins-replay.bag",
    ]
    STATIONARY_6 = [
        "base-3-2_DEMO-6_vins-replay.bag",
        "EE-3-2_DEMO-6_vins-replay.bag",
    ]

    FREE_STYLE_1 = [
        "base-4-0_DEMO-2_vins-replay.bag",
        "EE-4-0_DEMO-2_vins-replay.bag",
    ]
    FREE_STYLE_2 = [
        "base-4-1_DEMO-1_vins-replay.bag",
        "EE-4-1_DEMO-1_vins-replay.bag",
    ]
    STATIONARY_LAB = [
        "base-5-0_DEMO-1_vins-replay.bag",
        "EE-5-0_DEMO-1_vins-replay.bag",
    ]

class TEST_SET_MONO_RGB_IMU_ACC_0511(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0511/mono_rgb_imu/S-1_E-1_accurate_T_ic/2023-05-16",
        "camera_config_file_base": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0511/session_0/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0511_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_0511_MAF(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0511/mono_rgb_imu/S-1_E-1_accurate_T_ic_manufacture/2023-05-16",
        "camera_config_file_base": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0511/session_0/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0511_MONO_RGB


#### BATCH TESTS 05 18 2023 ####
class DATASET_DEMO_0518_MONO_RGB(Enum):
    BEE_31 = ["EE-1-5_DEMO-31_vins-replay.bag","EE-0-27_DEMO-31_vins-replay.bag"]
    BEE_32 = ["EE-1-4_DEMO-32_vins-replay.bag","EE-0-28_DEMO-32_vins-replay.bag"]
    BEE_33 = ["EE-1-3_DEMO-33_vins-replay.bag","EE-0-29_DEMO-33_vins-replay.bag"]
    BEE_34 = ["EE-1-2_DEMO-34_vins-replay.bag","EE-0-30_DEMO-34_vins-replay.bag"]
    BEE_35 = ["EE-1-1_DEMO-35_vins-replay.bag","EE-0-31_DEMO-35_vins-replay.bag"]
    BEE_36 = ["EE-1-0_DEMO-36_vins-replay.bag","EE-0-32_DEMO-36_vins-replay.bag"]

    SPIN_07 = ["EE-0-15_DEMO-7_vins-replay.bag"]
    SPIN_08 = ["EE-0-16_DEMO-8_vins-replay.bag"]
    SPIN_09 = ["EE-0-17_DEMO-9_vins-replay.bag"]
    SPIN_10 = ["EE-0-18_DEMO-10_vins-replay.bag"]
    SPIN_11 = ["EE-0-19_DEMO-11_vins-replay.bag"]
    SPIN_12 = ["EE-0-20_DEMO-12_vins-replay.bag"]

    CIRC_25 = ["EE-1-26_DEMO-25_vins-replay.bag","EE-0-21_DEMO-25_vins-replay.bag"]
    CIRC_26 = ["EE-1-27_DEMO-26_vins-replay.bag","EE-0-22_DEMO-26_vins-replay.bag"]
    CIRC_27 = ["EE-1-28_DEMO-27_vins-replay.bag","EE-0-23_DEMO-27_vins-replay.bag"]
    CIRC_28 = ["EE-1-29_DEMO-28_vins-replay.bag","EE-0-24_DEMO-28_vins-replay.bag"]
    CIRC_29 = ["EE-1-30_DEMO-29_vins-replay.bag","EE-0-25_DEMO-29_vins-replay.bag"]
    CIRC_30 = ["EE-1-31_DEMO-30_vins-replay.bag","EE-0-26_DEMO-30_vins-replay.bag"]
    
    FWD_13 = ["EE-1-15_DEMO-13_vins-replay.bag","EE-0-3_DEMO-13_vins-replay.bag"]
    FWD_14 = ["EE-1-17_DEMO-14_vins-replay.bag","EE-0-5_DEMO-14_vins-replay.bag"]
    FWD_15 = ["EE-1-19_DEMO-15_vins-replay.bag","EE-0-7_DEMO-15_vins-replay.bag"]
    FWD_16 = ["EE-1-21_DEMO-16_vins-replay.bag","EE-0-9_DEMO-16_vins-replay.bag"]
    FWD_17 = ["EE-1-23_DEMO-17_vins-replay.bag","EE-0-11_DEMO-17_vins-replay.bag"]
    FWD_18 = ["EE-1-25_DEMO-18_vins-replay.bag","EE-0-13_DEMO-18_vins-replay.bag"]

    RVR_19 = ["EE-1-14_DEMO-19_vins-replay.bag","EE-0-4_DEMO-19_vins-replay.bag"]
    RVR_20 = ["EE-1-16_DEMO-20_vins-replay.bag","EE-0-6_DEMO-20_vins-replay.bag"]
    RVR_21 = ["EE-1-18_DEMO-21_vins-replay.bag","EE-0-8_DEMO-21_vins-replay.bag"]
    RVR_22 = ["EE-1-20_DEMO-22_vins-replay.bag","EE-0-10_DEMO-22_vins-replay.bag"]
    RVR_23 = ["EE-1-22_DEMO-23_vins-replay.bag","EE-0-12_DEMO-23_vins-replay.bag"]
    RVR_24 = ["EE-1-24_DEMO-24_vins-replay.bag","EE-0-14_DEMO-24_vins-replay.bag"]

    STATIONARY_5 = [
        "EE-0-1_DEMO-5_vins-replay.bag",
    ]
    STATIONARY_6 = [
        "EE-0-2_DEMO-6_vins-replay.bag",
    ]

class DATASET_DEMO_0612_MONO_RGB_DUAL(Enum):
    SQR_39 = ["dual-1-0_DEMO-39_vins-replay.bag"]

class DATASET_DEMO_0612_MONO_RGB_DUAL_2(Enum):
    SPIN_07 = ["dual-0-0_DEMO-7_vins-replay.bag"]
    SQR_39 = ["dual-0-0_DEMO-32_vins-replay.bag"]
    
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

class DATASET_DEMO_0612_MONO_RGB_DUAL_3(Enum):
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

class TEST_SET_MONO_RGB_IMU_ACC_0518(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0518/mono_rgb_imu/S-1_E-1_accurate_T_ic_manufacture/2023-05-18",
        "camera_config_file_base": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0518/mono_rgb_imu/S-1_E-1_accurate_T_ic_manufacture/mono_rgb_imu_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0518/mono_rgb_imu/S-1_E-1_accurate_T_ic_manufacture/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0518/session_0/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0518_MONO_RGB


#### BATCH TESTS 05 19 2023 ####
class DATASET_DEMO_0519_MONO_RGB(Enum):
    BEE_31 = ["base-0-29_DEMO-31_vins-replay.bag","EE-0-29_DEMO-31_vins-replay.bag"]
    BEE_32 = ["base-0-30_DEMO-32_vins-replay.bag","EE-0-30_DEMO-32_vins-replay.bag"]
    BEE_33 = ["base-0-31_DEMO-33_vins-replay.bag","EE-0-31_DEMO-33_vins-replay.bag"]
    BEE_34 = ["base-0-32_DEMO-34_vins-replay.bag","EE-0-32_DEMO-34_vins-replay.bag"]
    BEE_35 = ["base-0-33_DEMO-35_vins-replay.bag","EE-0-33_DEMO-35_vins-replay.bag"]
    BEE_36 = ["base-0-35_DEMO-36_vins-replay.bag","EE-0-35_DEMO-36_vins-replay.bag"]

    SPIN_07 = ["base-0-22_DEMO-7_vins-replay.bag", "EE-0-22_DEMO-7_vins-replay.bag"]
    SPIN_08 = ["base-0-23_DEMO-8_vins-replay.bag", "EE-0-23_DEMO-8_vins-replay.bag"]
    SPIN_09 = ["base-0-25_DEMO-9_vins-replay.bag", "EE-0-25_DEMO-9_vins-replay.bag"]
    SPIN_10 = ["base-0-26_DEMO-10_vins-replay.bag", "EE-0-26_DEMO-10_vins-replay.bag"]
    SPIN_11 = ["base-0-27_DEMO-11_vins-replay.bag", "EE-0-27_DEMO-11_vins-replay.bag"]
    SPIN_12 = ["base-0-28_DEMO-12_vins-replay.bag", "EE-0-28_DEMO-12_vins-replay.bag"]

    CIRC_25 = ["base-0-16_DEMO-25_vins-replay.bag", "EE-0-16_DEMO-25_vins-replay.bag"]
    CIRC_26 = ["base-0-17_DEMO-26_vins-replay.bag", "EE-0-17_DEMO-26_vins-replay.bag"]
    CIRC_27 = ["base-0-18_DEMO-27_vins-replay.bag", "EE-0-18_DEMO-27_vins-replay.bag"]
    CIRC_28 = ["base-0-19_DEMO-28_vins-replay.bag", "EE-0-19_DEMO-28_vins-replay.bag"]
    CIRC_29 = ["base-0-20_DEMO-29_vins-replay.bag", "EE-0-20_DEMO-29_vins-replay.bag"]
    CIRC_30 = ["base-0-21_DEMO-30_vins-replay.bag", "EE-0-21_DEMO-30_vins-replay.bag"]
    
    FWD_13 = ["base-0-4_DEMO-13_vins-replay.bag", "EE-0-4_DEMO-13_vins-replay.bag"]
    FWD_14 = ["base-0-6_DEMO-14_vins-replay.bag", "EE-0-6_DEMO-14_vins-replay.bag"]
    FWD_15 = ["base-0-8_DEMO-15_vins-replay.bag", "EE-0-8_DEMO-15_vins-replay.bag"]
    FWD_16 = ["base-0-10_DEMO-16_vins-replay.bag", "EE-0-10_DEMO-16_vins-replay.bag"]
    FWD_17 = ["base-0-12_DEMO-17_vins-replay.bag", "EE-0-12_DEMO-17_vins-replay.bag"]
    FWD_18 = ["base-0-14_DEMO-18_vins-replay.bag", "EE-0-14_DEMO-18_vins-replay.bag"]

    # RVR_19 = ["EE-1-14_DEMO-19_vins-replay.bag","EE-0-4_DEMO-19_vins-replay.bag"]
    RVR_20 = ["base-0-7_DEMO-20_vins-replay.bag", "EE-0-7_DEMO-20_vins-replay.bag"]
    RVR_21 = ["base-0-9_DEMO-21_vins-replay.bag", "EE-0-9_DEMO-21_vins-replay.bag"]
    RVR_22 = ["base-0-11_DEMO-22_vins-replay.bag", "EE-0-11_DEMO-22_vins-replay.bag"]
    RVR_23 = ["base-0-13_DEMO-23_vins-replay.bag", "EE-0-13_DEMO-23_vins-replay.bag"]
    RVR_24 = ["base-0-15_DEMO-24_vins-replay.bag", "EE-0-15_DEMO-24_vins-replay.bag"]

    STATIONARY_5 = ["base-0-1_DEMO-5_vins-replay.bag", "EE-0-1_DEMO-5_vins-replay.bag"]
    STATIONARY_6 = ["base-0-2_DEMO-6_vins-replay.bag", "EE-0-2_DEMO-6_vins-replay.bag"]

class TEST_SET_MONO_RGB_IMU_ACC_0519(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0519/mono_rgb_imu/S-1_E-1_accurate_T_ic/2023-05-19",
        "camera_config_file_base": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0519/mono_rgb_imu/S-1_E-1_accurate_T_ic/mono_rgb_imu_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0519/mono_rgb_imu/S-1_E-1_accurate_T_ic/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0519/session_0/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0519_MONO_RGB

#### BATCH TESTS 06 12 2023 ####
class DATASET_DEMO_0612_MONO_RGB(Enum):
    SPIN_07 = ["EE-0-0_DEMO-7_vins-replay.bag",]
    
    BEE_31 = ["base-0-19_DEMO-31_vins-replay.bag","EE-0-19_DEMO-31_vins-replay.bag"]
    BEE_32 = ["base-0-20_DEMO-32_vins-replay.bag","EE-0-20_DEMO-32_vins-replay.bag"]
    BEE_33 = ["base-0-21_DEMO-33_vins-replay.bag","EE-0-21_DEMO-33_vins-replay.bag"]
    BEE_34 = ["base-0-22_DEMO-34_vins-replay.bag","EE-0-22_DEMO-34_vins-replay.bag"]
    BEE_35 = ["base-0-24_DEMO-35_vins-replay.bag","EE-0-24_DEMO-35_vins-replay.bag"]
    BEE_36 = ["base-0-25_DEMO-36_vins-replay.bag","EE-0-25_DEMO-36_vins-replay.bag"]

    CIRC_25 = ["base-0-13_DEMO-25_vins-replay.bag","EE-0-13_DEMO-25_vins-replay.bag"]
    CIRC_26 = ["base-0-14_DEMO-26_vins-replay.bag","EE-0-14_DEMO-26_vins-replay.bag"]
    CIRC_27 = ["base-0-15_DEMO-27_vins-replay.bag","EE-0-15_DEMO-27_vins-replay.bag"]
    CIRC_28 = ["base-0-16_DEMO-28_vins-replay.bag","EE-0-16_DEMO-28_vins-replay.bag"]
    CIRC_29 = ["base-0-17_DEMO-29_vins-replay.bag","EE-0-17_DEMO-29_vins-replay.bag"]
    CIRC_30 = ["base-0-18_DEMO-30_vins-replay.bag","EE-0-18_DEMO-30_vins-replay.bag"]
    
    FWD_13 = ["base-0-1_DEMO-13_vins-replay.bag","EE-0-1_DEMO-13_vins-replay.bag"]
    FWD_14 = ["base-0-3_DEMO-14_vins-replay.bag","EE-0-3_DEMO-14_vins-replay.bag"]
    FWD_15 = ["base-0-5_DEMO-15_vins-replay.bag","EE-0-5_DEMO-15_vins-replay.bag"]
    FWD_16 = ["base-0-7_DEMO-16_vins-replay.bag","EE-0-7_DEMO-16_vins-replay.bag"]
    FWD_17 = ["base-0-9_DEMO-17_vins-replay.bag","EE-0-9_DEMO-17_vins-replay.bag"]
    FWD_18 = ["base-0-11_DEMO-18_vins-replay.bag","EE-0-11_DEMO-18_vins-replay.bag"]

    RVR_19 = ["base-0-2_DEMO-19_vins-replay.bag","EE-0-2_DEMO-19_vins-replay.bag"]
    RVR_20 = ["base-0-4_DEMO-20_vins-replay.bag","EE-0-4_DEMO-20_vins-replay.bag"]
    RVR_21 = ["base-0-6_DEMO-21_vins-replay.bag","EE-0-6_DEMO-21_vins-replay.bag"]
    RVR_22 = ["base-0-8_DEMO-22_vins-replay.bag","EE-0-8_DEMO-22_vins-replay.bag"]
    RVR_23 = ["base-0-10_DEMO-23_vins-replay.bag","EE-0-10_DEMO-23_vins-replay.bag"]
    RVR_24 = ["base-0-12_DEMO-24_vins-replay.bag","EE-0-12_DEMO-24_vins-replay.bag"]

    SQR_37 = ["base-1-0_DEMO-37_vins-replay.bag","EE-1-0_DEMO-37_vins-replay.bag"]
    SQR_39 = ["base-1-1_DEMO-39_vins-replay.bag","EE-1-1_DEMO-39_vins-replay.bag"]
    SQR_41 = ["base-1-2_DEMO-41_vins-replay.bag","EE-1-2_DEMO-41_vins-replay.bag"]
    SQR_42 = ["base-1-3_DEMO-42_vins-replay.bag","EE-1-3_DEMO-42_vins-replay.bag"]
    TRI_43 = ["base-1-4_DEMO-43_vins-replay.bag","EE-1-4_DEMO-43_vins-replay.bag"]
    TRI_47 = ["base-1-5_DEMO-47_vins-replay.bag","EE-1-5_DEMO-47_vins-replay.bag"]
    
    ROGUE_1 = ["base-1-6_DEMO-1_vins-replay.bag","EE-1-6_DEMO-1_vins-replay.bag"]
    ROGUE_2 = ["base-1-7_DEMO-1_vins-replay.bag","EE-1-7_DEMO-1_vins-replay.bag"]
    
class TEST_SET_MONO_RGB_IMU_ACC_0612(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/2023-06-13",
        "camera_config_file_base": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/mono_rgb_imu_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_0612_0821(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/2023-08-21",
        "camera_config_file_base": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/mono_rgb_imu_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_0612_0922(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/2023-09-22",
        "camera_config_file_base": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/mono_rgb_imu_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_accurate_T_ic/mono_rgb_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB

class TEST_SET_STEREO_ACC_0612(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/stereo/S-1_E-1_accurate_T_ic/2023-06-13",
        "camera_config_file_base": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/stereo/S-1_E-1_accurate_T_ic/stereo_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/stereo/S-1_E-1_accurate_T_ic/stereo_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB

class TEST_SET_STEREO_IMU_ACC_0612(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/stereo_imu/S-1_E-1_accurate_T_ic/2023-06-13",
        "camera_config_file_base": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/stereo_imu/S-1_E-1_accurate_T_ic/stereo_imu_config_base.yaml",
        "camera_config_file_EE": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/stereo_imu/S-1_E-1_accurate_T_ic/stereo_imu_config_EE.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB
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
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_2

class TEST_SET_DUAL_MONO_IMU_0612_1012(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v3/2023-10-12",
        "camera_config_file_dual": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0612/mono_rgb_imu/S-1_E-1_dual_v3/mono_rgb_imu_config_dual.yaml",
        "demo_map": f"{Path.home()}/.ros/bagfiles/waterloo_steel_demo_0612/session_1/demo_map.json",
    }
    TESTSET = DATASET_DEMO_0612_MONO_RGB_DUAL_3
