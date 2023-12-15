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
####### 1213 A    Collection :
class DATASET_DEMO_1213_A:
    class STA(Enum):
        H   = ["dual-0-0_DEMO-1_vins-replay.bag"]
        E   = ["dual-0-1_DEMO-2_vins-replay.bag"]
        U   = ["dual-0-2_DEMO-3_vins-replay.bag"]
        D   = ["dual-0-3_DEMO-4_vins-replay.bag"]
        LR  = ["dual-0-4_DEMO-5_vins-replay.bag"]
        UD  = ["dual-0-5_DEMO-6_vins-replay.bag"]
    class SPI(Enum):
        H   = ["dual-0-6_DEMO-7_vins-replay.bag"]
        E   = ["dual-0-7_DEMO-8_vins-replay.bag"]
        U   = ["dual-0-8_DEMO-9_vins-replay.bag"]
        D   = ["dual-0-9_DEMO-10_vins-replay.bag"]
        LR  = ["dual-0-10_DEMO-11_vins-replay.bag"]
        UD  = ["dual-0-11_DEMO-12_vins-replay.bag"]
        LR2 = ["dual-1-1_DEMO-11_vins-replay.bag"]
    class FWD(Enum):
        H   = ["dual-1-2_DEMO-13_vins-replay.bag"]
        E   = ["dual-1-4_DEMO-14_vins-replay.bag"]
        U   = ["dual-1-6_DEMO-15_vins-replay.bag"]
        D   = ["dual-1-8_DEMO-16_vins-replay.bag"]
        LR  = ["dual-1-10_DEMO-17_vins-replay.bag"]
        UD  = ["dual-1-12_DEMO-18_vins-replay.bag"]
    class RVR(Enum):
        H   = ["dual-1-3_DEMO-19_vins-replay.bag"]
        E   = ["dual-1-5_DEMO-20_vins-replay.bag"]
        U   = ["dual-1-7_DEMO-21_vins-replay.bag"]
        D   = ["dual-1-9_DEMO-22_vins-replay.bag"]
        LR  = ["dual-1-11_DEMO-23_vins-replay.bag"]
        UD  = ["dual-1-13_DEMO-24_vins-replay.bag"]
    class CIR(Enum):
        H  = ["dual-1-14_DEMO-25_vins-replay.bag"]
        E  = ["dual-1-15_DEMO-26_vins-replay.bag"]
        U  = ["dual-1-16_DEMO-27_vins-replay.bag"]
        D  = ["dual-1-17_DEMO-28_vins-replay.bag"]
        LR = ["dual-1-18_DEMO-29_vins-replay.bag"]
        UD = ["dual-1-19_DEMO-30_vins-replay.bag"]
    class BEE(Enum):
        H  = ["dual-1-20_DEMO-31_vins-replay.bag"]
        E  = ["dual-1-21_DEMO-32_vins-replay.bag"]
        U  = ["dual-1-22_DEMO-33_vins-replay.bag"]
        D  = ["dual-1-23_DEMO-34_vins-replay.bag"]
        LR = ["dual-1-24_DEMO-35_vins-replay.bag"]
        UD = ["dual-1-25_DEMO-36_vins-replay.bag"]
    class SQR_A(Enum):
        H  = ["dual-1-26_DEMO-37_vins-replay.bag"]
        E  = ["dual-1-27_DEMO-38_vins-replay.bag"]
        E2 = ["dual-1-28_DEMO-38_vins-replay.bag"]
        U  = ["dual-1-29_DEMO-39_vins-replay.bag"]
        D  = ["dual-1-30_DEMO-40_vins-replay.bag"]
        LR = ["dual-1-31_DEMO-41_vins-replay.bag"]
        LR1= ["dual-1-32_DEMO-41_vins-replay.bag"]
        LR2= ["dual-1-33_DEMO-41_vins-replay.bag"]
        LR3= ["dual-1-35_DEMO-41_vins-replay.bag"]
        UD = ["dual-1-34_DEMO-42_vins-replay.bag"]
    class SQR_B(Enum):
        H  = ["dual-2-5_DEMO-37_vins-replay.bag"]
        E  = ["dual-2-3_DEMO-39_vins-replay.bag"]
        U  = ["dual-2-4_DEMO-38_vins-replay.bag"]
        D  = ["dual-2-2_DEMO-40_vins-replay.bag"]
        LR = ["dual-2-1_DEMO-41_vins-replay.bag"]
        UD = ["dual-2-0_DEMO-42_vins-replay.bag"]
    class TRI(Enum):
        H  = ["dual-2-6_DEMO-43_vins-replay.bag"]
        E  = ["dual-2-7_DEMO-44_vins-replay.bag"]
        U  = ["dual-2-8_DEMO-45_vins-replay.bag"]
        D  = ["dual-2-9_DEMO-46_vins-replay.bag"]
        LR = ["dual-2-10_DEMO-47_vins-replay.bag"]
        UD = ["dual-2-11_DEMO-48_vins-replay.bag"]

CONFIG_1213A = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1213A/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baaseline/2023-12-15", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-12-15"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1213A/session_1/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}
class DEMO_1213_A_STA(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.STA
class DEMO_1213_A_SPI(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.SPI
class DEMO_1213_A_FWD(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.FWD
class DEMO_1213_A_RVR(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.RVR
class DEMO_1213_A_CIR(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.CIR
class DEMO_1213_A_BEE(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.BEE
class DEMO_1213_A_SQR_A(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.SQR_A
class DEMO_1213_A_SQR_B(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.SQR_B
class DEMO_1213_A_TRI(Enum):
    CONFIG = CONFIG_1213A
    TEST_SET = DATASET_DEMO_1213_A.TRI


####### 1213 B    Collection :
class DATASET_DEMO_1213_B:
    class STA(Enum):
        H   = ["dual-1-0_DEMO-1_vins-replay.bag"]
        E   = ["dual-1-1_DEMO-2_vins-replay.bag"]
        U   = ["dual-1-2_DEMO-3_vins-replay.bag"]
        D   = ["dual-1-3_DEMO-4_vins-replay.bag"]
        LR  = ["dual-1-4_DEMO-5_vins-replay.bag"]
        UD  = ["dual-1-5_DEMO-6_vins-replay.bag"]
    
    class SPI(Enum):
        H   = ["dual-1-6_DEMO-7_vins-replay.bag"]
        E   = ["dual-1-7_DEMO-8_vins-replay.bag"]
        U   = ["dual-1-8_DEMO-9_vins-replay.bag"]
        D   = ["dual-1-9_DEMO-10_vins-replay.bag"]
        LR  = ["dual-1-10_DEMO-11_vins-replay.bag"]
        UD  = ["dual-1-11_DEMO-12_vins-replay.bag"]
    
    class FWD(Enum):
        H   = ["dual-1-13_DEMO-13_vins-replay.bag"]
        E   = ["dual-1-15_DEMO-14_vins-replay.bag"]
        U   = ["dual-1-17_DEMO-15_vins-replay.bag"]
        D   = ["dual-1-19_DEMO-16_vins-replay.bag"]
        LR  = ["dual-1-21_DEMO-17_vins-replay.bag"]
        UD  = ["dual-1-23_DEMO-18_vins-replay.bag"]
    
    class RVR(Enum):
        H   = ["dual-1-14_DEMO-19_vins-replay.bag"]
        E   = ["dual-1-16_DEMO-20_vins-replay.bag"]
        U   = ["dual-1-18_DEMO-21_vins-replay.bag"]
        D   = ["dual-1-20_DEMO-22_vins-replay.bag"]
        LR  = ["dual-1-22_DEMO-23_vins-replay.bag"]
        UD  = ["dual-1-24_DEMO-24_vins-replay.bag"]
    
    class CIR(Enum):
        H  = ["dual-1-25_DEMO-25_vins-replay.bag"]
        E  = ["dual-1-26_DEMO-26_vins-replay.bag"]
        U  = ["dual-1-27_DEMO-27_vins-replay.bag"]
        D  = ["dual-1-28_DEMO-28_vins-replay.bag"]
        LR = ["dual-1-29_DEMO-29_vins-replay.bag"]
        UD = ["dual-1-30_DEMO-30_vins-replay.bag"]
    
    class BEE(Enum):
        H  = ["dual-1-31_DEMO-31_vins-replay.bag"]
        E  = ["dual-1-32_DEMO-32_vins-replay.bag"]
        U  = ["dual-1-33_DEMO-33_vins-replay.bag"]
        D  = ["dual-1-34_DEMO-34_vins-replay.bag"]
        LR = ["dual-1-35_DEMO-35_vins-replay.bag"]
        UD = ["dual-1-36_DEMO-36_vins-replay.bag"]
    
    class SQR(Enum):
        H  = ["dual-1-37_DEMO-37_vins-replay.bag"]
        E  = ["dual-1-38_DEMO-38_vins-replay.bag"]
        U  = ["dual-1-39_DEMO-39_vins-replay.bag"]
        D  = ["dual-1-40_DEMO-40_vins-replay.bag"]
        LR = ["dual-1-41_DEMO-41_vins-replay.bag"]
        UD = ["dual-1-42_DEMO-42_vins-replay.bag"]
        UD2 = ["dual-2-5_DEMO-42_vins-replay.bag"]
    
    class TRI(Enum):
        H  = ["dual-1-43_DEMO-43_vins-replay.bag"]
        E  = ["dual-1-44_DEMO-45_vins-replay.bag"]
        U  = ["dual-1-45_DEMO-46_vins-replay.bag"]
        D  = ["dual-1-46_DEMO-47_vins-replay.bag"]
        LR = ["dual-1-47_DEMO-47_vins-replay.bag"]
        UD = ["dual-1-48_DEMO-48_vins-replay.bag"]

CONFIG_1213B = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1213B/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baseline/2023-12-15", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-12-15"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1213B/session_1/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}

class DEMO_1213_B_STA(Enum):
    CONFIG = CONFIG_1213B
    TEST_SET = DATASET_DEMO_1213_B.STA
class DEMO_1213_B_SPI(Enum):
    CONFIG = CONFIG_1213B
    TEST_SET = DATASET_DEMO_1213_B.SPI
class DEMO_1213_B_FWD(Enum):
    CONFIG = CONFIG_1213B
    TEST_SET = DATASET_DEMO_1213_B.FWD
class DEMO_1213_B_RVR(Enum):
    CONFIG = CONFIG_1213B
    TEST_SET = DATASET_DEMO_1213_B.RVR
class DEMO_1213_B_CIR(Enum):
    CONFIG = CONFIG_1213B
    TEST_SET = DATASET_DEMO_1213_B.CIR
class DEMO_1213_B_BEE(Enum):
    CONFIG = CONFIG_1213B
    TEST_SET = DATASET_DEMO_1213_B.BEE
class DEMO_1213_B_SQR(Enum):
    CONFIG = CONFIG_1213B
    TEST_SET = DATASET_DEMO_1213_B.SQR
class DEMO_1213_B_TRI(Enum):
    CONFIG = CONFIG_1213B
    TEST_SET = DATASET_DEMO_1213_B.TRI


####### 1213 C    Collection :
class DATASET_DEMO_1213_C:
    class ROGUE_H(Enum):
        H0 = ["dual-0-0_DEMO-55_vins-replay.bag"]
        H1 = ["dual-0-1_DEMO-55_vins-replay.bag"]
        H2 = ["dual-0-2_DEMO-55_vins-replay.bag"]
        H3 = ["dual-0-3_DEMO-55_vins-replay.bag"]
        H4 = ["dual-0-4_DEMO-55_vins-replay.bag"]
        
    class ROGUES(Enum):
        E  = ["dual-0-5_DEMO-56_vins-replay.bag"]
        U  = ["dual-0-6_DEMO-57_vins-replay.bag"]
        D  = ["dual-0-7_DEMO-58_vins-replay.bag"]
        LR = ["dual-0-8_DEMO-59_vins-replay.bag"]
        UD = ["dual-0-9_DEMO-60_vins-replay.bag"]
        
    class LONG_SQR(Enum):
        H  = ["dual-0-11_DEMO-61_vins-replay.bag"]
        E  = ["dual-0-12_DEMO-62_vins-replay.bag"]
        U  = ["dual-0-13_DEMO-63_vins-replay.bag"]
        D  = ["dual-0-14_DEMO-64_vins-replay.bag"]
        LR = ["dual-0-16_DEMO-65_vins-replay.bag"]
        UD = ["dual-0-17_DEMO-66_vins-replay.bag"]
  
    class SQR(Enum):
        H  = ["dual-1-0_DEMO-37_vins-replay.bag"]
        E  = ["dual-1-1_DEMO-38_vins-replay.bag"]
        U  = ["dual-1-2_DEMO-39_vins-replay.bag"]
        D  = ["dual-1-3_DEMO-40_vins-replay.bag"]
        LR = ["dual-1-4_DEMO-41_vins-replay.bag"]
        UD = ["dual-1-5_DEMO-42_vins-replay.bag"]
    
    class ROGUE_NO_VICON(Enum):
        H = ["dual-1-6_DEMO-55_vins-replay.bag"] # 1-2 elevator
        U = ["dual-1-7_DEMO-57_vins-replay.bag"] # 2nd floor

CONFIG_1213C = {
    "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1213C/mono_rgb_imu",
    "rungs": {
        "baseline": "S-1_E-1_dual_baaseline/2023-12-15", 
        "coupled (ours)": "S-1_E-1_dual_arm_odom/2023-12-15"
    },
    "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
    "demo_map": ".ros/bagfiles/waterloo_steel_demo_1213C/session_1/demo_map.json",
    "AXIS_BOUNDARY_MAX": [10,10,5],# in meters world boundary
}
class DEMO_1213_C_ROG_1(Enum):
    CONFIG = CONFIG_1213C
    TEST_SET = DATASET_DEMO_1213_C.ROGUE_H
class DEMO_1213_C_ROG_2(Enum):
    CONFIG = CONFIG_1213C
    TEST_SET = DATASET_DEMO_1213_C.ROGUES
class DEMO_1213_C_LONG_SQR(Enum):
    CONFIG = CONFIG_1213C
    TEST_SET = DATASET_DEMO_1213_C.LONG_SQR
class DEMO_1213_C_SQR(Enum):
    CONFIG = CONFIG_1213C
    TEST_SET = DATASET_DEMO_1213_C.SQR
class DEMO_1213_C_ROG_3(Enum):
    CONFIG = CONFIG_1213C
    TEST_SET = DATASET_DEMO_1213_C.ROGUE_NO_VICON
