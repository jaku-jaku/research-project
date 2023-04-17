from enum import Enum

class TEST_SET_MONO_IMU(Enum):
    DIRECTORY = "/home/jx/.ros/bag_replay_recorder_files_bak"
    EE_i0 = [
        "EE-0-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-00-41_2023-04-14-10-06-46.bag",
        "EE-0-1_S5-E30_1_DEMO_3_recording_2023-04-06-16-03-40_2023-04-14-10-07-21.bag",
        "EE-0-2_S5-E30_2_DEMO_4_recording_2023-04-06-16-04-43_2023-04-14-10-07-57.bag",
        "EE-0-3_S5-E30_3_DEMO_5_recording_2023-04-06-16-05-35_2023-04-14-10-08-33.bag",
        "EE-0-4_S5-E30_4_DEMO_6_recording_2023-04-06-16-06-22_2023-04-14-10-09-08.bag",
        "EE-0-5_S5-E30_5_DEMO_8_recording_2023-04-06-16-07-16_2023-04-14-10-09-44.bag",
        "EE-0-6_S5-E30_6_DEMO_9_recording_2023-04-06-16-07-53_2023-04-14-10-10-20.bag",
        "EE-0-7_S5-E30_7_DEMO_10_recording_2023-04-06-16-08-40_2023-04-14-10-10-56.bag",
        "EE-0-8_S5-E30_8_DEMO_11_recording_2023-04-06-16-09-48_2023-04-14-10-11-31.bag",
        "EE-0-9_S5-E30_9_DEMO_12_recording_2023-04-06-16-10-26_2023-04-14-10-12-07.bag",
    ]
    EE_i1 = [
        "EE-1-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-11-35_2023-04-13-17-32-23.bag",
        "EE-1-10_S5-E30_10_DEMO_24_recording_2023-04-06-16-20-02_2023-04-13-17-38-15.bag",
        "EE-1-1_S5-E30_1_DEMO_14_recording_2023-04-06-16-12-19_2023-04-13-17-32-58.bag",
        "EE-1-2_S5-E30_2_DEMO_20_recording_2023-04-06-16-12-58_2023-04-13-17-33-33.bag",
        "EE-1-3_S5-E30_3_DEMO_15_recording_2023-04-06-16-13-39_2023-04-13-17-34-08.bag",
        "EE-1-4_S5-E30_4_DEMO_21_recording_2023-04-06-16-14-22_2023-04-13-17-34-44.bag",
        "EE-1-5_S5-E30_5_DEMO_16_recording_2023-04-06-16-16-27_2023-04-13-17-35-19.bag",
        "EE-1-6_S5-E30_6_DEMO_22_recording_2023-04-06-16-17-09_2023-04-13-17-35-54.bag",
        "EE-1-7_S5-E30_7_DEMO_17_recording_2023-04-06-16-17-57_2023-04-13-17-36-29.bag",
        "EE-1-8_S5-E30_8_DEMO_23_recording_2023-04-06-16-18-37_2023-04-13-17-37-04.bag",
        "EE-1-9_S5-E30_9_DEMO_18_recording_2023-04-06-16-19-17_2023-04-13-17-37-39.bag",
    ]
    EE_i2 = [
        "EE-2-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-21-00_2023-04-13-17-40-02.bag",
        "EE-2-1_S5-E30_1_DEMO_26_recording_2023-04-06-16-21-37_2023-04-13-17-40-38.bag",
        "EE-2-2_S5-E30_2_DEMO_27_recording_2023-04-06-16-22-14_2023-04-13-17-41-13.bag",
    ]
    EE_i3 = [
        "EE-3-0_S5-E30_0_DEMO_26_recording_2023-04-06-16-23-24_2023-04-13-17-42-16.bag",
        "EE-3-1_S5-E30_1_DEMO_27_recording_2023-04-06-16-24-04_2023-04-13-17-42-51.bag",
        "EE-3-2_S5-E30_2_DEMO_28_recording_2023-04-06-16-24-47_2023-04-13-17-43-26.bag",
        "EE-3-3_S5-E30_3_DEMO_29_recording_2023-04-06-16-25-30_2023-04-13-17-44-01.bag",
        "EE-3-4_S5-E30_4_DEMO_30_recording_2023-04-06-16-26-09_2023-04-13-17-44-37.bag",
        "EE-3-5_S5-E30_5_DEMO_32_recording_2023-04-06-16-26-52_2023-04-13-17-45-12.bag",
    ]
    Base_i8 = [
        "EE-8-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-34-42_2023-04-14-09-26-56.bag",
        "EE-8-1_S5-E30_1_DEMO_3_recording_2023-04-06-16-35-42_2023-04-14-09-27-32.bag",
        "EE-8-2_S5-E30_2_DEMO_4_recording_2023-04-06-16-36-27_2023-04-14-09-28-08.bag",
        "EE-8-3_S5-E30_3_DEMO_5_recording_2023-04-06-16-37-09_2023-04-14-09-28-43.bag",
        "EE-8-4_S5-E30_4_DEMO_6_recording_2023-04-06-16-37-49_2023-04-14-09-29-19.bag",
        "EE-8-5_S5-E30_5_DEMO_7_recording_2023-04-06-16-38-31_2023-04-14-09-29-55.bag",
        "EE-8-6_S5-E30_6_DEMO_8_recording_2023-04-06-16-39-07_2023-04-14-09-30-30.bag",
        "EE-8-7_S5-E30_7_DEMO_9_recording_2023-04-06-16-40-07_2023-04-14-09-31-06.bag",
        "EE-8-8_S5-E30_8_DEMO_11_recording_2023-04-06-16-40-53_2023-04-14-09-31-42.bag",
        "EE-8-9_S5-E30_9_DEMO_12_recording_2023-04-06-16-41-35_2023-04-14-09-32-18.bag",
    ]
    Base_i9 = [
        "EE-9-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-42-32_2023-04-14-09-16-37.bag",
        "EE-9-1_S5-E30_1_DEMO_14_recording_2023-04-06-16-43-11_2023-04-14-09-17-12.bag",
        "EE-9-2_S5-E30_2_DEMO_20_recording_2023-04-06-16-43-48_2023-04-14-09-17-48.bag",
        "EE-9-3_S5-E30_3_DEMO_16_recording_2023-04-06-16-44-25_2023-04-14-09-18-24.bag",
        "EE-9-4_S5-E30_4_DEMO_22_recording_2023-04-06-16-45-06_2023-04-14-09-18-59.bag",
        "EE-9-5_S5-E30_5_DEMO_17_recording_2023-04-06-16-46-12_2023-04-14-09-19-35.bag",
        "EE-9-6_S5-E30_6_DEMO_23_recording_2023-04-06-16-46-52_2023-04-14-09-20-11.bag",
        "EE-9-7_S5-E30_7_DEMO_18_recording_2023-04-06-16-47-35_2023-04-14-09-20-46.bag",
        "EE-9-8_S5-E30_8_DEMO_24_recording_2023-04-06-16-48-19_2023-04-14-09-21-22.bag",
        "EE-9-9_S5-E30_9_DEMO_25_recording_2023-04-06-16-49-30_2023-04-14-09-21-58.bag",
        "EE-9-10_S5-E30_10_DEMO_26_recording_2023-04-06-16-50-08_2023-04-14-09-22-34.bag",
        "EE-9-11_S5-E30_11_DEMO_27_recording_2023-04-06-16-50-46_2023-04-14-09-23-10.bag",
        "EE-9-12_S5-E30_12_DEMO_28_recording_2023-04-06-16-51-32_2023-04-14-09-23-45.bag",
        "EE-9-13_S5-E30_13_DEMO_29_recording_2023-04-06-16-52-14_2023-04-14-09-24-21.bag",
        "EE-9-14_S5-E30_14_DEMO_30_recording_2023-04-06-16-52-54_2023-04-14-09-24-57.bag",
    ]
    
class TEST_SET_STEREO_IMU(Enum):
    DIRECTORY = "/home/jx/.ros/bag_replay_recorder_files/stereo_imu"
    EE_i0 = [
    ]
    EE_i1 = [
    ]
    EE_i2 = [
        "EE-2-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-21-00_2023-04-16-15-32-26.bag",
        "EE-2-1_S5-E30_1_DEMO_26_recording_2023-04-06-16-21-37_2023-04-16-15-32-59.bag",
        "EE-2-2_S5-E30_2_DEMO_27_recording_2023-04-06-16-22-14_2023-04-16-15-33-33.bag",
    ]
    EE_i3 = [
        "EE-3-0_S5-E30_0_DEMO_26_recording_2023-04-06-16-23-24_2023-04-16-16-38-12.bag",
        "EE-3-1_S5-E30_1_DEMO_27_recording_2023-04-06-16-24-04_2023-04-16-16-38-45.bag",
        "EE-3-2_S5-E30_2_DEMO_28_recording_2023-04-06-16-24-47_2023-04-16-16-39-19.bag",
        "EE-3-3_S5-E30_3_DEMO_29_recording_2023-04-06-16-25-30_2023-04-16-16-39-52.bag",
        "EE-3-4_S5-E30_4_DEMO_30_recording_2023-04-06-16-26-09_2023-04-16-16-40-25.bag",
        "EE-3-5_S5-E30_5_DEMO_32_recording_2023-04-06-16-26-52_2023-04-16-16-40-59.bag",
    ]
    Base_i8 = [
        "EE-8-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-34-42_2023-04-16-16-43-33.bag",
        "EE-8-1_S5-E30_1_DEMO_3_recording_2023-04-06-16-35-42_2023-04-16-16-44-06.bag",
        "EE-8-2_S5-E30_2_DEMO_4_recording_2023-04-06-16-36-27_2023-04-16-16-44-40.bag",
        "EE-8-3_S5-E30_3_DEMO_5_recording_2023-04-06-16-37-09_2023-04-16-16-45-14.bag",
        "EE-8-4_S5-E30_4_DEMO_6_recording_2023-04-06-16-37-49_2023-04-16-16-45-48.bag",
        "EE-8-5_S5-E30_5_DEMO_7_recording_2023-04-06-16-38-31_2023-04-16-16-46-22.bag",
        "EE-8-6_S5-E30_6_DEMO_8_recording_2023-04-06-16-39-07_2023-04-16-16-46-56.bag",
        "EE-8-7_S5-E30_7_DEMO_9_recording_2023-04-06-16-40-07_2023-04-16-16-47-30.bag",
        "EE-8-8_S5-E30_8_DEMO_11_recording_2023-04-06-16-40-53_2023-04-16-16-48-03.bag",
        "EE-8-9_S5-E30_9_DEMO_12_recording_2023-04-06-16-41-35_2023-04-16-16-48-37.bag",
    ]
    Base_i9 = [
        "EE-9-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-42-32_2023-04-16-17-03-34.bag",
        "EE-9-1_S5-E30_1_DEMO_14_recording_2023-04-06-16-43-11_2023-04-16-17-04-08.bag",
        "EE-9-2_S5-E30_2_DEMO_20_recording_2023-04-06-16-43-48_2023-04-16-17-04-42.bag",
        "EE-9-3_S5-E30_3_DEMO_16_recording_2023-04-06-16-44-25_2023-04-16-17-05-15.bag",
        "EE-9-4_S5-E30_4_DEMO_22_recording_2023-04-06-16-45-06_2023-04-16-17-05-49.bag",
        "EE-9-5_S5-E30_5_DEMO_17_recording_2023-04-06-16-46-12_2023-04-16-17-06-23.bag",
        "EE-9-6_S5-E30_6_DEMO_23_recording_2023-04-06-16-46-52_2023-04-16-17-06-56.bag",
        "EE-9-7_S5-E30_7_DEMO_18_recording_2023-04-06-16-47-35_2023-04-16-17-07-30.bag",
        "EE-9-8_S5-E30_8_DEMO_24_recording_2023-04-06-16-48-19_2023-04-16-17-08-04.bag",
        "EE-9-9_S5-E30_9_DEMO_25_recording_2023-04-06-16-49-30_2023-04-16-17-08-38.bag",
        "EE-9-10_S5-E30_10_DEMO_26_recording_2023-04-06-16-50-08_2023-04-16-17-09-12.bag",
        "EE-9-11_S5-E30_11_DEMO_27_recording_2023-04-06-16-50-46_2023-04-16-17-09-45.bag",
        "EE-9-12_S5-E30_12_DEMO_28_recording_2023-04-06-16-51-32_2023-04-16-17-10-19.bag",
        "EE-9-13_S5-E30_13_DEMO_29_recording_2023-04-06-16-52-14_2023-04-16-17-10-53.bag",
        "EE-9-14_S5-E30_14_DEMO_30_recording_2023-04-06-16-52-54_2023-04-16-17-11-27.bag",
    ]


class TEST_SET_STEREO(Enum):
    DIRECTORY = "/home/jx/.ros/bag_replay_recorder_files"
    EE_i0 = [
    ]
    EE_i1 = [    
        "EE-1-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-11-35_2023-04-16-17-30-24.bag",
        "EE-1-10_S5-E30_10_DEMO_24_recording_2023-04-06-16-20-02_2023-04-16-17-35-57.bag",
        "EE-1-1_S5-E30_1_DEMO_14_recording_2023-04-06-16-12-19_2023-04-16-17-30-57.bag",
        "EE-1-2_S5-E30_2_DEMO_20_recording_2023-04-06-16-12-58_2023-04-16-17-31-30.bag",
        "EE-1-3_S5-E30_3_DEMO_15_recording_2023-04-06-16-13-39_2023-04-16-17-32-04.bag",
        "EE-1-4_S5-E30_4_DEMO_21_recording_2023-04-06-16-14-22_2023-04-16-17-32-37.bag",
        "EE-1-5_S5-E30_5_DEMO_16_recording_2023-04-06-16-16-27_2023-04-16-17-33-10.bag",
        "EE-1-6_S5-E30_6_DEMO_22_recording_2023-04-06-16-17-09_2023-04-16-17-33-44.bag",
        "EE-1-7_S5-E30_7_DEMO_17_recording_2023-04-06-16-17-57_2023-04-16-17-34-17.bag",
        "EE-1-8_S5-E30_8_DEMO_23_recording_2023-04-06-16-18-37_2023-04-16-17-34-50.bag",
        "EE-1-9_S5-E30_9_DEMO_18_recording_2023-04-06-16-19-17_2023-04-16-17-35-24.bag",
    ]
    EE_i2 = [
        "EE-2-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-21-00_2023-04-16-19-49-01.bag",
        "EE-2-1_S5-E30_1_DEMO_26_recording_2023-04-06-16-21-37_2023-04-16-19-49-34.bag",
        "EE-2-2_S5-E30_2_DEMO_27_recording_2023-04-06-16-22-14_2023-04-16-19-50-08.bag",
    ]
    EE_i3 = [
        "EE-3-0_S5-E30_0_DEMO_26_recording_2023-04-06-16-23-24_2023-04-16-19-50-47.bag",
        "EE-3-1_S5-E30_1_DEMO_27_recording_2023-04-06-16-24-04_2023-04-16-19-51-20.bag",
        "EE-3-2_S5-E30_2_DEMO_28_recording_2023-04-06-16-24-47_2023-04-16-19-51-54.bag",
        "EE-3-3_S5-E30_3_DEMO_29_recording_2023-04-06-16-25-30_2023-04-16-19-52-27.bag",
        "EE-3-4_S5-E30_4_DEMO_30_recording_2023-04-06-16-26-09_2023-04-16-19-53-01.bag",
        "EE-3-5_S5-E30_5_DEMO_32_recording_2023-04-06-16-26-52_2023-04-16-19-53-34.bag",
    ]
    Base_i8 = [
        "EE-8-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-34-42_2023-04-16-20-18-42.bag",
        "EE-8-1_S5-E30_1_DEMO_3_recording_2023-04-06-16-35-42_2023-04-16-20-19-15.bag",
        "EE-8-2_S5-E30_2_DEMO_4_recording_2023-04-06-16-36-27_2023-04-16-20-19-49.bag",
        "EE-8-3_S5-E30_3_DEMO_5_recording_2023-04-06-16-37-09_2023-04-16-20-20-22.bag",
        "EE-8-4_S5-E30_4_DEMO_6_recording_2023-04-06-16-37-49_2023-04-16-20-20-56.bag",
        "EE-8-5_S5-E30_5_DEMO_7_recording_2023-04-06-16-38-31_2023-04-16-20-21-30.bag",
        "EE-8-6_S5-E30_6_DEMO_8_recording_2023-04-06-16-39-07_2023-04-16-20-22-03.bag",
        "EE-8-7_S5-E30_7_DEMO_9_recording_2023-04-06-16-40-07_2023-04-16-20-22-37.bag",
        "EE-8-8_S5-E30_8_DEMO_11_recording_2023-04-06-16-40-53_2023-04-16-20-23-10.bag",
        "EE-8-9_S5-E30_9_DEMO_12_recording_2023-04-06-16-41-35_2023-04-16-20-23-44.bag",
    ]
    Base_i9 = [
        "EE-9-0_S5-E30_0_DEMO_2_recording_2023-04-06-16-42-32_2023-04-16-21-16-34.bag",
        "EE-9-1_S5-E30_1_DEMO_14_recording_2023-04-06-16-43-11_2023-04-16-21-17-07.bag",
        "EE-9-2_S5-E30_2_DEMO_20_recording_2023-04-06-16-43-48_2023-04-16-21-17-41.bag",
        "EE-9-3_S5-E30_3_DEMO_16_recording_2023-04-06-16-44-25_2023-04-16-21-18-14.bag",
        "EE-9-4_S5-E30_4_DEMO_22_recording_2023-04-06-16-45-06_2023-04-16-21-18-48.bag",
        "EE-9-5_S5-E30_5_DEMO_17_recording_2023-04-06-16-46-12_2023-04-16-21-19-22.bag",
        "EE-9-6_S5-E30_6_DEMO_23_recording_2023-04-06-16-46-52_2023-04-16-21-19-55.bag",
        "EE-9-7_S5-E30_7_DEMO_18_recording_2023-04-06-16-47-35_2023-04-16-21-20-29.bag",
        "EE-9-8_S5-E30_8_DEMO_24_recording_2023-04-06-16-48-19_2023-04-16-21-21-02.bag",
        "EE-9-9_S5-E30_9_DEMO_25_recording_2023-04-06-16-49-30_2023-04-16-21-21-36.bag",
        "EE-9-10_S5-E30_10_DEMO_26_recording_2023-04-06-16-50-08_2023-04-16-21-22-09.bag",
        "EE-9-11_S5-E30_11_DEMO_27_recording_2023-04-06-16-50-46_2023-04-16-21-22-43.bag",
        "EE-9-12_S5-E30_12_DEMO_28_recording_2023-04-06-16-51-32_2023-04-16-21-23-16.bag",
        "EE-9-13_S5-E30_13_DEMO_29_recording_2023-04-06-16-52-14_2023-04-16-21-23-50.bag",
        "EE-9-14_S5-E30_14_DEMO_30_recording_2023-04-06-16-52-54_2023-04-16-21-24-23.bag",
    ]


# ==================================================================================================== TEMPLATE:
class TEST_SET_TEMPLATE(Enum):
    DIRECTORY = "/home/jx/.ros/bag_replay_recorder_files"
    EE_i0 = [
    ]
    EE_i1 = [
    ]
    EE_i2 = [
    ]
    EE_i3 = [
    ]
    Base_i8 = [
    ]
    Base_i9 = [
    ]
# ==================================================================================================== TEST_SET_TEMPLATE: