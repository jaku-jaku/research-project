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
TEST_SET_TITLE = "D455_v2"

### Structure:
from dataclasses import dataclass, field
@dataclass
class DEMO_STRUCT:
    CONFIG: dict
    TEST_SET: Enum

####### 1221 A    Collection :
class DATASET_DEMO_1221_A:
    class SPI(Enum):
        H   = ["dual-0-7_DEMO-7_vins-replay.bag"]
        E   = ["dual-0-8_DEMO-8_vins-replay.bag"]
        U   = ["dual-0-9_DEMO-9_vins-replay.bag"]
        D   = ["dual-0-10_DEMO-10_vins-replay.bag"]
        LR  = ["dual-0-11_DEMO-11_vins-replay.bag"]
        UD  = ["dual-0-12_DEMO-12_vins-replay.bag"]
    class FWD(Enum):
        H   = ["dual-0-13_DEMO-13_vins-replay.bag"]
        E   = ["dual-0-15_DEMO-14_vins-replay.bag"]
        U   = ["dual-0-19_DEMO-15_vins-replay.bag"]
        D   = ["dual-0-21_DEMO-16_vins-replay.bag"]
        LR  = ["dual-0-23_DEMO-17_vins-replay.bag"]
        UD  = ["dual-0-25_DEMO-18_vins-replay.bag"]
    class RVR(Enum):
        H   = ["dual-0-14_DEMO-19_vins-replay.bag"]
        E   = ["dual-0-18_DEMO-20_vins-replay.bag"]
        U   = ["dual-0-20_DEMO-21_vins-replay.bag"]
        D   = ["dual-0-22_DEMO-22_vins-replay.bag"]
        LR  = ["dual-0-24_DEMO-23_vins-replay.bag"]
        UD  = ["dual-0-26_DEMO-24_vins-replay.bag"]
    class CIR(Enum):
        H  = ["dual-1-1_DEMO-25_vins-replay.bag"]
        E  = ["dual-1-2_DEMO-26_vins-replay.bag"]
        U  = ["dual-1-3_DEMO-27_vins-replay.bag"]
        D  = ["dual-1-4_DEMO-28_vins-replay.bag"]
        LR = ["dual-1-5_DEMO-29_vins-replay.bag"]
        UD = ["dual-1-6_DEMO-30_vins-replay.bag"]
    class BEE(Enum):
        H  = ["dual-1-7_DEMO-31_vins-replay.bag"]
        E  = ["dual-1-8_DEMO-32_vins-replay.bag"]
        U  = ["dual-1-9_DEMO-33_vins-replay.bag"]
        D  = ["dual-1-10_DEMO-34_vins-replay.bag"]
        LR = ["dual-1-11_DEMO-35_vins-replay.bag"]
        UD = ["dual-1-12_DEMO-36_vins-replay.bag"]
    class SQR(Enum):
        H  = ["dual-1-13_DEMO-37_vins-replay.bag"]
        E  = ["dual-1-14_DEMO-38_vins-replay.bag"]
        U  = ["dual-1-15_DEMO-39_vins-replay.bag"]
        D  = ["dual-1-16_DEMO-40_vins-replay.bag"]
        LR = ["dual-1-17_DEMO-41_vins-replay.bag"]
        UD = ["dual-1-18_DEMO-42_vins-replay.bag"]
    class TRI(Enum):
        H  = ["dual-1-19_DEMO-43_vins-replay.bag"]
        E  = ["dual-1-20_DEMO-44_vins-replay.bag"]
        U  = ["dual-1-21_DEMO-45_vins-replay.bag"]
        D  = ["dual-1-22_DEMO-46_vins-replay.bag"]
        LR = ["dual-1-23_DEMO-47_vins-replay.bag"]
        UD = ["dual-1-24_DEMO-48_vins-replay.bag"]


class DEMO_1221_A(DEMO_STRUCT):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1221_A/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_baseline_final/2023-12-23", 
            "coupled (ours)": "S-1_E-1_dual_arm_odom_final/2024-01-01"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1221_A/session_1/demo_map.json",
        "AXIS_BOUNDARY_MAX": [4,4,1],# in meters world boundary
    }

class DEMO_1221_A_SPI(DEMO_1221_A):
    TEST_SET = DATASET_DEMO_1221_A.SPI
class DEMO_1221_A_FWD(DEMO_1221_A):
    TEST_SET = DATASET_DEMO_1221_A.FWD
class DEMO_1221_A_RVR(DEMO_1221_A):
    TEST_SET = DATASET_DEMO_1221_A.RVR
class DEMO_1221_A_CIR(DEMO_1221_A):
    TEST_SET = DATASET_DEMO_1221_A.CIR
class DEMO_1221_A_BEE(DEMO_1221_A):
    TEST_SET = DATASET_DEMO_1221_A.BEE
class DEMO_1221_A_SQR(DEMO_1221_A):
    TEST_SET = DATASET_DEMO_1221_A.SQR
class DEMO_1221_A_TRI(DEMO_1221_A):
    TEST_SET = DATASET_DEMO_1221_A.TRI
    
####### 1221 B    Collection :
class DATASET_DEMO_1221_B:
    class SPI(Enum):
        H   = ["dual-0-6_DEMO-7_vins-replay.bag"]
        E   = ["dual-0-7_DEMO-8_vins-replay.bag"]
        U   = ["dual-0-8_DEMO-9_vins-replay.bag"]
        D   = ["dual-0-9_DEMO-10_vins-replay.bag"]
        LR  = ["dual-0-10_DEMO-11_vins-replay.bag"]
        UD  = ["dual-0-11_DEMO-12_vins-replay.bag"]
    class FWD(Enum):
        H   = ["dual-0-12_DEMO-13_vins-replay.bag"]
        E   = ["dual-0-14_DEMO-14_vins-replay.bag"]
        U   = ["dual-0-16_DEMO-15_vins-replay.bag"]
        D   = ["dual-0-18_DEMO-16_vins-replay.bag"]
        LR  = ["dual-0-20_DEMO-17_vins-replay.bag"]
        UD  = ["dual-0-26_DEMO-18_vins-replay.bag"]
    class RVR(Enum):
        H   = ["dual-0-13_DEMO-19_vins-replay.bag"]
        E   = ["dual-0-15_DEMO-20_vins-replay.bag"]
        U   = ["dual-0-17_DEMO-21_vins-replay.bag"]
        D   = ["dual-0-19_DEMO-22_vins-replay.bag"]
        LR  = ["dual-0-21_DEMO-23_vins-replay.bag"]
        UD  = ["dual-0-27_DEMO-24_vins-replay.bag"]
    class CIR(Enum):
        H   = ["dual-0-28_DEMO-25_vins-replay.bag"]
        E   = ["dual-0-29_DEMO-26_vins-replay.bag"]
        U   = ["dual-0-30_DEMO-27_vins-replay.bag"]
        D   = ["dual-0-31_DEMO-28_vins-replay.bag"]
        LR  = ["dual-0-32_DEMO-29_vins-replay.bag"]
        UD  = ["dual-0-33_DEMO-30_vins-replay.bag"]
    class SQR(Enum):
        H   = ["dual-0-34_DEMO-37_vins-replay.bag"]
        E   = ["dual-0-35_DEMO-38_vins-replay.bag"]
        U   = ["dual-0-36_DEMO-39_vins-replay.bag"]
        D   = ["dual-0-37_DEMO-40_vins-replay.bag"]
        LR  = ["dual-0-38_DEMO-41_vins-replay.bag"]
        UD  = ["dual-0-39_DEMO-42_vins-replay.bag"]
    class TRI(Enum):
        H   = ["dual-0-40_DEMO-43_vins-replay.bag"]
        E   = ["dual-0-42_DEMO-44_vins-replay.bag"]
        U   = ["dual-0-43_DEMO-45_vins-replay.bag"]
        D   = ["dual-0-44_DEMO-46_vins-replay.bag"]
        LR  = ["dual-0-45_DEMO-47_vins-replay.bag"]
        

class DEMO_1221_B(DEMO_STRUCT):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1221_B/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_baseline_final/2023-12-23", 
            "coupled (ours)": "S-1_E-1_dual_arm_odom_final/2024-01-01"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1221_B/session_0/demo_map.json",
        "AXIS_BOUNDARY_MAX": [4,4,1],# in meters world boundary
    }

class DEMO_1221_B_SPI(DEMO_1221_B):
    TEST_SET = DATASET_DEMO_1221_B.SPI
class DEMO_1221_B_FWD(DEMO_1221_B):
    TEST_SET = DATASET_DEMO_1221_B.FWD
class DEMO_1221_B_RVR(DEMO_1221_B):
    TEST_SET = DATASET_DEMO_1221_B.RVR
class DEMO_1221_B_CIR(DEMO_1221_B):
    TEST_SET = DATASET_DEMO_1221_B.CIR
class DEMO_1221_B_SQR(DEMO_1221_B):
    TEST_SET = DATASET_DEMO_1221_B.SQR
class DEMO_1221_B_TRI(DEMO_1221_B):
    TEST_SET = DATASET_DEMO_1221_B.TRI


####### 1221 C    Collection :
class DATASET_DEMO_1221_C:
    class ARM_Pt_LeftDownRightUp_R1(Enum):
        STA = ["dual-1-8_DEMO-3_vins-replay.bag"]
        SPI = ["dual-1-1_DEMO-9_vins-replay.bag"]
        FWD = ["dual-1-2_DEMO-15_vins-replay.bag"]
        RVR = ["dual-1-3_DEMO-21_vins-replay.bag"]
        CIR = ["dual-1-4_DEMO-27_vins-replay.bag"]
        BEE = ["dual-1-9_DEMO-33_vins-replay.bag"]
        SQR = ["dual-1-5_DEMO-39_vins-replay.bag"]
        SQR_2 = ["dual-1-6_DEMO-39_vins-replay.bag"]
        TRI = ["dual-1-7_DEMO-45_vins-replay.bag"]
    class ARM_Pt_LeftDownRightUp_R2(Enum):
        STA = ["dual-1-18_DEMO-3_vins-replay.bag"]
        SPI = ["dual-1-19_DEMO-9_vins-replay.bag"]
        FWD = ["dual-1-20_DEMO-15_vins-replay.bag"]
        RVR = ["dual-1-21_DEMO-21_vins-replay.bag"]
        CIR = ["dual-1-22_DEMO-27_vins-replay.bag"]
        SQR = ["dual-1-23_DEMO-39_vins-replay.bag"]
        TRI = ["dual-1-24_DEMO-45_vins-replay.bag"]
    class BASE_BEE(Enum):
        H   = ["dual-1-30_DEMO-31_vins-replay.bag"]
        E   = ["dual-1-29_DEMO-32_vins-replay.bag"]
        U   = ["dual-1-25_DEMO-33_vins-replay.bag"]
        D   = ["dual-1-26_DEMO-34_vins-replay.bag"]
        LR  = ["dual-1-27_DEMO-35_vins-replay.bag"]
        UD  = ["dual-1-28_DEMO-36_vins-replay.bag"]
    class BASE_ROGUE(Enum):
        U   = ["dual-1-10_DEMO-57_vins-replay.bag"]
        D   = ["dual-1-12_DEMO-58_vins-replay.bag"]
        LR  = ["dual-1-14_DEMO-59_vins-replay.bag"]
        UD  = ["dual-1-16_DEMO-60_vins-replay.bag"]
    class Pt_UpRight_R1(Enum):
        SPI = ["dual-0-2_DEMO-10_vins-replay.bag"]
        FWD = ["dual-0-7_DEMO-16_vins-replay.bag"]
        RVR = ["dual-0-8_DEMO-22_vins-replay.bag"]
        CIR = ["dual-0-10_DEMO-28_vins-replay.bag"]
        SQR = ["dual-0-12_DEMO-40_vins-replay.bag"]
        TRI = ["dual-0-14_DEMO-46_vins-replay.bag"]
    class Pt_UpRight_R2(Enum):
        STA = ["dual-1-31_DEMO-4_vins-replay.bag"]
        SPI = ["dual-1-32_DEMO-10_vins-replay.bag"]
        FWD = ["dual-1-33_DEMO-16_vins-replay.bag"]
        RVR = ["dual-1-34_DEMO-22_vins-replay.bag"]
        CIR = ["dual-1-35_DEMO-28_vins-replay.bag"]
        SQR = ["dual-1-36_DEMO-40_vins-replay.bag"]
        TRI = ["dual-1-37_DEMO-46_vins-replay.bag"]

class DEMO_1221_C(DEMO_STRUCT):
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1221_C/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_baseline_final/2024-01-01", 
            "coupled (ours)": "S-1_E-1_dual_arm_odom_final/2024-01-01"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1221_C/session_0/demo_map.json",
        "AXIS_BOUNDARY_MAX": [4,4,1],# in meters world boundary
    }

class DEMO_1221_C_ARM_Pt_LeftDownRightUp_R1(DEMO_1221_C):
    TEST_SET = DATASET_DEMO_1221_C.ARM_Pt_LeftDownRightUp_R1
class DEMO_1221_C_ARM_Pt_LeftDownRightUp_R2(DEMO_1221_C):
    TEST_SET = DATASET_DEMO_1221_C.ARM_Pt_LeftDownRightUp_R2
class DEMO_1221_C_BASE_BEE(DEMO_1221_C):
    TEST_SET = DATASET_DEMO_1221_C.BASE_BEE
class DEMO_1221_C_BASE_ROGUE(DEMO_1221_C):
    TEST_SET = DATASET_DEMO_1221_C.BASE_ROGUE
    CONFIG = {
        "folder": ".ros/bag_replay_recorder_files/waterloo_steel_demo_1221_C/mono_rgb_imu",
        "rungs": {
            "baseline": "S-1_E-1_dual_baseline_final/2024-01-01", 
            "coupled (ours)": "S-1_E-1_dual_arm_odom_final/2024-01-01"
        },
        "camera_config_file_dual": "mono_rgb_imu_config_dual.yaml",
        "demo_map": ".ros/bagfiles/waterloo_steel_demo_1221_C/session_0/demo_map.json",
        "AXIS_BOUNDARY_MAX": [10,10,1],# in meters world boundary
    }
class DEMO_1221_C_Pt_UpRight_R1(DEMO_1221_C):
    TEST_SET = DATASET_DEMO_1221_C.Pt_UpRight_R1
class DEMO_1221_C_Pt_UpRight_R2(DEMO_1221_C):
    TEST_SET = DATASET_DEMO_1221_C.Pt_UpRight_R2
