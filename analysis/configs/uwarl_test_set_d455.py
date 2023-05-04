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

class TEST_SET_MONO_RGB_IMU(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0421/mono_rgb_imu/S7_E30/2023-05-03",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/mono_rgb_imu_config_EE.yaml",
    }
    EE_ExtF = [
        "EE-0-0_DEMO-1_vins-replay.bag",
        "EE-0-1_DEMO-2_vins-replay.bag",
        "EE-0-2_DEMO-3_vins-replay.bag",
        "EE-0-3_DEMO-4_vins-replay.bag",
        "EE-0-4_DEMO-5_vins-replay.bag",
        "EE-0-5_DEMO-6_vins-replay.bag",
    ]
    EE_Spin = [
        "EE-0-6_DEMO-7_vins-replay.bag",
        "EE-0-7_DEMO-8_vins-replay.bag",
        "EE-0-8_DEMO-9_vins-replay.bag",
        "EE-0-9_DEMO-10_vins-replay.bag",
        "EE-0-10_DEMO-11_vins-replay.bag",
        "EE-0-11_DEMO-12_vins-replay.bag",        
    ]
    EE_FWD = [
        "EE-0-12_DEMO-13_vins-replay.bag",        
        "EE-0-14_DEMO-14_vins-replay.bag",        
        "EE-0-16_DEMO-15_vins-replay.bag",        
        "EE-0-18_DEMO-16_vins-replay.bag",        
        "EE-0-20_DEMO-17_vins-replay.bag",        
        "EE-0-22_DEMO-18_vins-replay.bag",        
    ]
    EE_RVR = [
        "EE-0-13_DEMO-19_vins-replay.bag",
        "EE-0-15_DEMO-20_vins-replay.bag",
        "EE-0-17_DEMO-21_vins-replay.bag",
        "EE-0-19_DEMO-22_vins-replay.bag",
        "EE-0-21_DEMO-23_vins-replay.bag",
        "EE-0-23_DEMO-24_vins-replay.bag",
    ]
    EE_CIR = [
        "EE-0-24_DEMO-25_vins-replay.bag",
        "EE-0-25_DEMO-26_vins-replay.bag",
        "EE-0-26_DEMO-27_vins-replay.bag",
        "EE-0-27_DEMO-28_vins-replay.bag",
        "EE-0-28_DEMO-29_vins-replay.bag",
        "EE-0-29_DEMO-30_vins-replay.bag",
    ]
    EE_88 = [
        "EE-0-30_DEMO-31_vins-replay.bag",
        "EE-0-31_DEMO-32_vins-replay.bag",
        "EE-0-32_DEMO-33_vins-replay.bag",
        "EE-0-33_DEMO-34_vins-replay.bag",
        # "EE-0-34_DEMO-35_vins-replay.bag",
        "EE-0-35_DEMO-35_vins-replay.bag",
        "EE-0-36_DEMO-36_vins-replay.bag",
    ]
    base_ExtF = [
        "base-0-0_DEMO-1_vins-replay.bag",
        "base-0-1_DEMO-2_vins-replay.bag",
        "base-0-2_DEMO-3_vins-replay.bag",
        "base-0-3_DEMO-4_vins-replay.bag",
        "base-0-4_DEMO-5_vins-replay.bag",
        "base-0-5_DEMO-6_vins-replay.bag",
    ]
    base_Spin = [
        "base-0-6_DEMO-7_vins-replay.bag",
        "base-0-7_DEMO-8_vins-replay.bag",
        "base-0-8_DEMO-9_vins-replay.bag",
        "base-0-9_DEMO-10_vins-replay.bag",
        "base-0-10_DEMO-11_vins-replay.bag",
        "base-0-11_DEMO-12_vins-replay.bag",        
    ]
    base_FWD = [
        "base-0-12_DEMO-13_vins-replay.bag",        
        "base-0-14_DEMO-14_vins-replay.bag",        
        "base-0-16_DEMO-15_vins-replay.bag",        
        "base-0-18_DEMO-16_vins-replay.bag",        
        "base-0-20_DEMO-17_vins-replay.bag",        
        "base-0-22_DEMO-18_vins-replay.bag",        
    ]
    base_RVR = [
        "base-0-13_DEMO-19_vins-replay.bag",
        "base-0-15_DEMO-20_vins-replay.bag",
        "base-0-17_DEMO-21_vins-replay.bag",
        "base-0-19_DEMO-22_vins-replay.bag",
        "base-0-21_DEMO-23_vins-replay.bag",
        "base-0-23_DEMO-24_vins-replay.bag",
    ]
    base_CIR = [
        "base-0-24_DEMO-25_vins-replay.bag",
        "base-0-25_DEMO-26_vins-replay.bag",
        "base-0-26_DEMO-27_vins-replay.bag",
        "base-0-27_DEMO-28_vins-replay.bag",
        "base-0-28_DEMO-29_vins-replay.bag",
        "base-0-29_DEMO-30_vins-replay.bag",
    ]
    base_88 = [
        "base-0-30_DEMO-31_vins-replay.bag",
        "base-0-31_DEMO-32_vins-replay.bag",
        "base-0-32_DEMO-33_vins-replay.bag",
        "base-0-33_DEMO-34_vins-replay.bag",
        # "base-0-34_DEMO-35_vins-replay.bag",
        "base-0-35_DEMO-35_vins-replay.bag",
        "base-0-36_DEMO-36_vins-replay.bag",
    ]
 
class TEST_SET_MONO_IMU(Enum):
    CONFIG = {
        
        
    }
    EE_ExtF = [
        
    ]
    EE_Spin = [

    ]
    EE_FWD = [

    ]
    EE_RVR = [

    ]
    EE_CIR = [

    ]
    EE_88 = [

    ]
    Base_ExtF = [

    ]
    Base_Spin = [

    ]
    Base_FWD = [

    ]
    Base_RVR = [

    ]
    Base_CIR = [

    ]
    Base_88 = [

    ]
    
class TEST_SET_STEREO_IMU(Enum):
    CONFIG = {
        "directory": f"{Path.home()}/.ros/bag_replay_recorder_files/waterloo_steel_demo_0421/stereo_imu/S7_E30/2023-05-02",
        "camera_config_file": f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/VINS-Fusion/config/uwarl_d455/stereo_imu_config_EE.yaml",
    }
    EE_ExtF = [
        "EE-0-0_DEMO-1_vins-replay.bag",
        "EE-0-1_DEMO-2_vins-replay.bag",
        "EE-0-2_DEMO-3_vins-replay.bag",
        "EE-0-3_DEMO-4_vins-replay.bag",
        "EE-0-4_DEMO-5_vins-replay.bag",
        "EE-0-5_DEMO-6_vins-replay.bag",
    ]
    EE_Spin = [
        "EE-0-6_DEMO-7_vins-replay.bag",
        "EE-0-7_DEMO-8_vins-replay.bag",
        "EE-0-8_DEMO-9_vins-replay.bag",
        "EE-0-9_DEMO-10_vins-replay.bag",
        "EE-0-10_DEMO-11_vins-replay.bag",
        "EE-0-11_DEMO-12_vins-replay.bag",        
    ]
    EE_FWD = [
        "EE-0-12_DEMO-13_vins-replay.bag",        
        "EE-0-14_DEMO-14_vins-replay.bag",        
        "EE-0-16_DEMO-15_vins-replay.bag",        
        "EE-0-18_DEMO-16_vins-replay.bag",        
        "EE-0-20_DEMO-17_vins-replay.bag",        
        "EE-0-22_DEMO-18_vins-replay.bag",        
    ]
    EE_RVR = [
        "EE-0-13_DEMO-19_vins-replay.bag",
        "EE-0-15_DEMO-20_vins-replay.bag",
        "EE-0-17_DEMO-21_vins-replay.bag",
        "EE-0-19_DEMO-22_vins-replay.bag",
        "EE-0-21_DEMO-23_vins-replay.bag",
        "EE-0-23_DEMO-24_vins-replay.bag",
    ]
    EE_CIR = [
        "EE-0-24_DEMO-25_vins-replay.bag",
        "EE-0-25_DEMO-26_vins-replay.bag",
        "EE-0-26_DEMO-27_vins-replay.bag",
        "EE-0-27_DEMO-28_vins-replay.bag",
        "EE-0-28_DEMO-29_vins-replay.bag",
        "EE-0-29_DEMO-30_vins-replay.bag",
    ]
    EE_88 = [
        "EE-0-30_DEMO-31_vins-replay.bag",
        "EE-0-31_DEMO-32_vins-replay.bag",
        "EE-0-32_DEMO-33_vins-replay.bag",
        "EE-0-33_DEMO-34_vins-replay.bag",
        # "EE-0-34_DEMO-35_vins-replay.bag",
        "EE-0-35_DEMO-35_vins-replay.bag",
        "EE-0-36_DEMO-36_vins-replay.bag",
    ]
    base_ExtF = [
        "base-0-0_DEMO-1_vins-replay.bag",
        "base-0-1_DEMO-2_vins-replay.bag",
        "base-0-2_DEMO-3_vins-replay.bag",
        "base-0-3_DEMO-4_vins-replay.bag",
        "base-0-4_DEMO-5_vins-replay.bag",
        "base-0-5_DEMO-6_vins-replay.bag",
    ]
    base_Spin = [
        "base-0-6_DEMO-7_vins-replay.bag",
        "base-0-7_DEMO-8_vins-replay.bag",
        "base-0-8_DEMO-9_vins-replay.bag",
        "base-0-9_DEMO-10_vins-replay.bag",
        "base-0-10_DEMO-11_vins-replay.bag",
        "base-0-11_DEMO-12_vins-replay.bag",        
    ]
    base_FWD = [
        "base-0-12_DEMO-13_vins-replay.bag",        
        "base-0-14_DEMO-14_vins-replay.bag",        
        "base-0-16_DEMO-15_vins-replay.bag",        
        "base-0-18_DEMO-16_vins-replay.bag",        
        "base-0-20_DEMO-17_vins-replay.bag",        
        "base-0-22_DEMO-18_vins-replay.bag",        
    ]
    base_RVR = [
        "base-0-13_DEMO-19_vins-replay.bag",
        "base-0-15_DEMO-20_vins-replay.bag",
        "base-0-17_DEMO-21_vins-replay.bag",
        "base-0-19_DEMO-22_vins-replay.bag",
        "base-0-21_DEMO-23_vins-replay.bag",
        "base-0-23_DEMO-24_vins-replay.bag",
    ]
    base_CIR = [
        "base-0-24_DEMO-25_vins-replay.bag",
        "base-0-25_DEMO-26_vins-replay.bag",
        "base-0-26_DEMO-27_vins-replay.bag",
        "base-0-27_DEMO-28_vins-replay.bag",
        "base-0-28_DEMO-29_vins-replay.bag",
        "base-0-29_DEMO-30_vins-replay.bag",
    ]
    base_88 = [
        "base-0-30_DEMO-31_vins-replay.bag",
        "base-0-31_DEMO-32_vins-replay.bag",
        "base-0-32_DEMO-33_vins-replay.bag",
        "base-0-33_DEMO-34_vins-replay.bag",
        # "base-0-34_DEMO-35_vins-replay.bag",
        "base-0-35_DEMO-35_vins-replay.bag",
        "base-0-36_DEMO-36_vins-replay.bag",
    ]


class TEST_SET_STEREO(Enum):
    CONFIG = {
        
        
        # "vins_pre_process_functions": {
        #     TYPES_VAR.POSITION_XYZ: (lambda x: rx.apply(x)),
        # },
    }
    EE_ExtF = [
    
    
    
    
    
    
    ]
    EE_Spin = [
    
    
    
    
    
    
    ]
    EE_FWD = [
    
    
    
    
    
    
    ]
    EE_RVR = [
    
    
    
    
    
    
    ]
    EE_CIR = [
    
    
    
    
    
    
    ]
    EE_88 = [
    
    
    
    
    # 
    
    
    ]
    Base_ExtF = [
    
    
    
    
    
    
    ]
    Base_Spin = [
    
    
    
    
    
    
    ]
    Base_FWD = [
    
    
    
    
    
    
    ]
    Base_RVR = [
    
    
    
    
    
    
    ]
    Base_CIR = [    
    
    
    
    
    
    
    ]
    Base_88 = [
    
    
    
    
    # 
    
    
    ]

# ==================================================================================================== TEMPLATE:
class TEST_SET_TEMPLATE(Enum):
    CONFIG = {
    }
    EE_ExtF = [
    ]
    EE_Spin = [
    ]
    EE_FWD = [
    ]
    EE_RVR = [
    ]
    EE_CIR = [
    ]
    EE_88 = [
    ]
    Base_ExtF = [
    ]
    Base_Spin = [
    ]
    Base_FWD = [
    ]
    Base_RVR = [
    ]
    Base_CIR = [
    ]
    Base_88 = [
    ]
    

# ==================================================================================================== TEST_SET_TEMPLATE:
class TEST_SET_SINGLE(Enum):
    CONFIG = {
    }