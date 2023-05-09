from enum import Enum
from pathlib import Path

#   Base    \Arm:| Ext-F | Pt-FWD | Pt-Up | Pt-Down | **Pt-L/R| *Up-Down | 
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

class DATASET_DEMO_0504_MONO_RGB(Enum):
    EE_ExtF = [
    ]
    EE_Spin = [
        "EE-1-0_DEMO-7_vins-replay.bag",
        "EE-1-1_DEMO-8_vins-replay.bag",
        "EE-1-2_DEMO-9_vins-replay.bag",
        "EE-1-3_DEMO-10_vins-replay.bag",
        "EE-1-4_DEMO-11_vins-replay.bag",
        "EE-1-5_DEMO-12_vins-replay.bag",     
    ]
    EE_FWD = [
        "EE-0-0_DEMO-13_vins-replay.bag",
        "EE-0-12_DEMO-13_vins-replay.bag",
        "EE-0-2_DEMO-14_vins-replay.bag",
        "EE-0-4_DEMO-15_vins-replay.bag",
        "EE-0-6_DEMO-16_vins-replay.bag",
        "EE-0-8_DEMO-17_vins-replay.bag",
        "EE-0-10_DEMO-18_vins-replay.bag",     
    ]
    EE_RVR = [
        "EE-0-1_DEMO-19_vins-replay.bag",
        "EE-0-3_DEMO-20_vins-replay.bag",
        "EE-0-5_DEMO-21_vins-replay.bag",
        "EE-0-7_DEMO-22_vins-replay.bag",
        "EE-0-9_DEMO-23_vins-replay.bag",
        "EE-0-11_DEMO-24_vins-replay.bag",
    ]
    EE_CIR = [
        "EE-2-0_DEMO-25_vins-replay.bag",
        "EE-2-1_DEMO-26_vins-replay.bag",
        "EE-2-2_DEMO-27_vins-replay.bag",
        "EE-2-3_DEMO-28_vins-replay.bag",
        "EE-2-4_DEMO-29_vins-replay.bag",
        "EE-2-6_DEMO-29_vins-replay.bag",
        "EE-2-5_DEMO-30_vins-replay.bag",
    ]
    EE_88 = [
        "EE-2-7_DEMO-31_vins-replay.bag",
        "EE-2-8_DEMO-31_vins-replay.bag",
        "EE-2-9_DEMO-33_vins-replay.bag",
        "EE-2-10_DEMO-34_vins-replay.bag",
        "EE-2-11_DEMO-35_vins-replay.bag",
        "EE-2-12_DEMO-36_vins-replay.bag",
    ]
    base_ExtF = [
    ]
    base_Spin = [
        "base-1-0_DEMO-7_vins-replay.bag",
        "base-1-1_DEMO-8_vins-replay.bag",
        "base-1-2_DEMO-9_vins-replay.bag",
        "base-1-3_DEMO-10_vins-replay.bag",
        "base-1-4_DEMO-11_vins-replay.bag",
        "base-1-5_DEMO-12_vins-replay.bag",
    ]
    base_FWD = [
        "base-0-0_DEMO-13_vins-replay.bag",
        "base-0-12_DEMO-13_vins-replay.bag",
        "base-0-2_DEMO-14_vins-replay.bag",
        "base-0-4_DEMO-15_vins-replay.bag",
        "base-0-6_DEMO-16_vins-replay.bag",
        "base-0-8_DEMO-17_vins-replay.bag",
        "base-0-10_DEMO-18_vins-replay.bag",
    ]
    base_RVR = [
        "base-0-1_DEMO-19_vins-replay.bag",
        "base-0-3_DEMO-20_vins-replay.bag",
        "base-0-5_DEMO-21_vins-replay.bag",
        "base-0-7_DEMO-22_vins-replay.bag",
        "base-0-9_DEMO-23_vins-replay.bag",
        "base-0-11_DEMO-24_vins-replay.bag",
    ]
    base_CIR = [
        "base-2-0_DEMO-25_vins-replay.bag",
        "base-2-1_DEMO-26_vins-replay.bag",
        "base-2-2_DEMO-27_vins-replay.bag",
        "base-2-3_DEMO-28_vins-replay.bag",
        "base-2-4_DEMO-29_vins-replay.bag",
        "base-2-6_DEMO-29_vins-replay.bag",
        "base-2-5_DEMO-30_vins-replay.bag",
    ]
    base_88 = [
        "base-2-7_DEMO-31_vins-replay.bag",
        "base-2-8_DEMO-31_vins-replay.bag",
        "base-2-9_DEMO-33_vins-replay.bag",
        "base-2-10_DEMO-34_vins-replay.bag",
        "base-2-11_DEMO-35_vins-replay.bag",
        "base-2-12_DEMO-36_vins-replay.bag",
    ]
 

class TEST_SET_MONO_RGB_IMU(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1-1/2023-05-05",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_TIC(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ic/2023-05-07",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_INIT_GUESS_TIC(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_init_guess_T_ic/2023-05-08",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB
class TEST_SET_MONO_RGB_IMU_ACC_TCI(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ci/2023-05-08",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_TIC_MANUFACTURED(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ic_manufactured/2023-05-08",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB

class TEST_SET_MONO_RGB_IMU_ACC_TIC_V2(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0504/mono_rgb_imu/S-1_E-1_accurate_T_ic_v2/2023-05-08",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    }
    TESTSET = DATASET_DEMO_0504_MONO_RGB
