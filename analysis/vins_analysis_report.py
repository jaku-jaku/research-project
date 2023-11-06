# %% -------------------------------- Import Lib -------------------------------- %% #
# built-in
import os
import sys
from datetime import datetime
from pathlib import Path
import time

# 3rd party lib
import numpy as np
from scipy.ndimage import gaussian_filter1d

# 3rd party util
from icecream import ic

# %% 
# -------------------------------- Import Our Lib -------------------------------- %% #
# ours:
from utils.uwarl_bag_parser import BagParser, TYPES_VAR
from configs.uwarl_common import PARSER_CALLBACKS
# from configs.uwarl_test_set import TEST_SET_STEREO_IMU, TEST_SET_MONO_IMU, TEST_SET_STEREO, TEST_SET_SINGLE
from configs.uwarl_test_set_d455 import (
    TEST_SET_TITLE, 
    DUAL_MONO_IMU_1101_1104_baseline,
    DUAL_MONO_IMU_1101_1104_armOdom,
    DUAL_MONO_IMU_1101_1104_comparison_v3,
)

from vins_replay_utils.uwarl_replay_decoder import auto_generate_labels_from_bag_file_name_with_json_config, ProcessedData
from vins_replay_utils.uwarl_analysis_plot import AnalysisManager, MultiBagsDataManager, plot_time_parallel, plot_time_series, plot_spatial

from vins_replay_utils.uwarl_camera import MultiSensor_Camera_Node

# -------------------------------- Files Automation -------------------------------- %% #
# # 1. Pre-Config
FIG_OUT_DIR = f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/research-project/output/vins_analysis"
FEATURE_LOCAL_DEVELOPMENT  = True

FEATURE_ONLY_LAST                   = 10 #seconds

SPLIT_MAP = None
SPLIT_MAP = {1:"Base", 0:"EE"}

FEATURE_AUTO_SAVE                   = True
FEATURE_AUTO_CLOSE_FIGS             = True
FEATURE_OUTPUT_BAG_META             = False

FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS  = False
FEATURE_PLOT_3D_TRAJECTORIES        = True
FEATURE_PLOT_CAMERAS                = True
FEATURE_PLOT_CAM_CONFIGS            = False

PLOT_FEATURE_ORIENTING              = False # TODO: orientation correction needed to be implemented
PLOT_FEATURE_SHOW_ORIENTATIONS      = True
PLOT_FEATURE_VIEW_ANGLES            = [(30,10),(70,45),(10,10)]#[(30,10),(70,45),(10,10)]
PLOT_FEATURE_VIEW_ANGLES_SEPARATED  = True
PLOT_FEATURE_SCATTER_PLOT           = True
PLOT_FEATURE_FIG_SIZE_SCATTER       = (8,8)
PLOT_FEATURE_LINE_PLOT              = True
PLOT_FEATURE_FIG_SIZE_LINE          = (4,4)
RUN_NAME = ""
RUN_TAG = ""
if FEATURE_AUTO_CLOSE_FIGS:
    RUN_TAG = "[DEV]"
    
FEATURE_PROCESS_BAGS = (FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS or FEATURE_PLOT_3D_TRAJECTORIES)
# -------------------------------- REPORT -------------------------------- %% #
def generate_report(bag_test_case_name, bag_test_case_config, bag_subset):
    print(f"Generating Report for {bag_subset.name}")
    
    # -------------------------------- Manager & Configs -------------------------------- %% #
    date_time = datetime.now().strftime("%Y-%m-%d")
    AM = AnalysisManager(
        output_dir=FIG_OUT_DIR,
        run_name=f"run_{date_time}/{RUN_TAG}{TEST_SET_TITLE}", 
        test_set_name=bag_test_case_name,
        prefix=bag_subset.name,
        auto_save=FEATURE_AUTO_SAVE,
        auto_close=FEATURE_AUTO_CLOSE_FIGS,
    )
    DMs = {}
    # -------------------------------- Iterating each rung -------------------------------- %% #
    for bag_rung_label, bag_rung in bag_test_case_config["rungs"].items():
        bag_folder = bag_test_case_config["folder"]
        bag_directory = os.path.join(Path.home(), bag_folder, bag_rung)
        json_map = os.path.join(Path.home(), bag_test_case_config["demo_map"])
        ic(bag_directory)
        ic(json_map)
        ic(os.path.dirname(bag_directory))
        config_file = os.path.join(os.path.dirname(bag_directory), bag_test_case_config["camera_config_file_dual"])
        ic(config_file)
        
        if FEATURE_PROCESS_BAGS:
            # ASSUMPTION: this generation assumes that all test cases share same json config
            AUTO_BAG_DICT = auto_generate_labels_from_bag_file_name_with_json_config(
                list_of_bag_path=bag_subset.value, 
                json_map_file_name=json_map,
            )
        else:
            AUTO_BAG_DICT = None
        ic(AUTO_BAG_DICT)

        # # 2. Data Pre-Processing
        # -------------------------------- Pre-Processing -------------------------------- %% #
        # 0. Process Config File
        BP = BagParser(PARSER_CALLBACKS)
        # 0.1 generate camera pose:
        cameras = []
        if FEATURE_PLOT_CAMERAS:
            # TODO: add camera plot functions
            print("Process dual configuration file")
            cameras.append(MultiSensor_Camera_Node(_config_file=config_file, _prefix="d0_"))
            cameras.append(MultiSensor_Camera_Node(_config_file=config_file, _prefix="d1_"))
                
        if FEATURE_PLOT_CAM_CONFIGS:    
            for cam in cameras:
                fig, ax = cam.create_3d_figure()
                cam.plot_camera(ax=ax)
                AM.save_fig(fig, tag=f"{cam._prefix}camera_config")

        # 1. Process and Aggregate data from multiple bags:
        tic = time.perf_counter()
        if FEATURE_PROCESS_BAGS:    
            pData={}
            for label, path in AUTO_BAG_DICT.items():
                try:
                    pData[label] = ProcessedData(BP, bag_directory, path, T_LAST_S=FEATURE_ONLY_LAST)
                except Exception as e:
                    pass
                
        toc = time.perf_counter()
        print(f"[tic-toc] Bag Processed: {(toc - tic)/60:.0f} minutes {(toc - tic)%60:.2f} seconds")
            
        # -------------------------------- DEBUG -------------------------------- %% #
        # DEBUG: save a sample here:
        if FEATURE_OUTPUT_BAG_META and FEATURE_PROCESS_BAGS:
            for label, data in pData.items():
                if data.bag_exist:
                    AM.save_dict(AUTO_BAG_DICT, "info")
                    AM.save_dict(data.bag_samples, "bag_samples")
                    AM.save_dict(data.bag_topics, "bag_topics")
                    AM.save_dict(data.bag_info, "bag_info")
                    break

        # # 3. Plotting Multiple datasets from multiple bagfiles
        # -------------------------------- Multi-Bag Data -------------------------------- %% #    
        # 2. Load into data plotter:
        if FEATURE_PROCESS_BAGS:    
            DMs[bag_rung_label] = MultiBagsDataManager(pData)

    # -------------------------------- Plot: Voltage & Joint Efforts -------------------------------- #
    if FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS:
        # 3. assemble data sets:
        for label, DM in DMs.items():
            data_sets_y = {
                "Voltage (V)"                   : DM.extract_data(
                    bag_topic="/uwarl/robotnik_base_hw/voltage", 
                    dict_var_type={TYPES_VAR.VOLTAGE: 'y'},
                ),
                "Joint Effort (Filtered) (N.m)" : DM.extract_data(
                    bag_topic="/wam/joint_states", 
                    dict_var_type={TYPES_VAR.JOINT_EFFORT: 'y'},
                    pre_process_funcs={
                        TYPES_VAR.JOINT_EFFORT: (lambda x: gaussian_filter1d(np.linalg.norm(x, axis=1), 3)),
                    },
                ),
            }

            # 4. Plot:
            fig,ax,title = plot_time_series(DM, data_sets_y, title=label)
            AM.save_fig(fig, title)
            fig,ax,title = plot_time_parallel(DM, data_sets_y, figsize=(15,4), title=label)
            AM.save_fig(fig, title)

    # -------------------------------- Plot Data Prep: 3D trajectories -------------------------------- %% #
    if FEATURE_PLOT_3D_TRAJECTORIES:
        # 3. assemble data sets:
        POSE_VARS = {
            TYPES_VAR.POSITION_XYZ: 'y',
            TYPES_VAR.ORIENTATION_XYZW: 'r',
        }
        data_sets_3d = dict()
        for label, DM in DMs.items():
            data_sets_3d[f"Vicon Cam Base ({label})"]          = DM.extract_data(
                bag_topic="/vins_estimator/base/vicon/path", dict_var_type=POSE_VARS,
            )
            data_sets_3d[f"Vicon Cam EE ({label})"]            = DM.extract_data(
                bag_topic="/vins_estimator/EE/vicon/path", dict_var_type=POSE_VARS,
            )
            
        for label, DM in DMs.items():
            data_sets_3d[f"{label} VINS Est Base"]           = DM.extract_data(
                bag_topic="/vins_estimator/base/path", dict_var_type=POSE_VARS,
            )
            data_sets_3d[f"{label} VINS Est EE"]             = DM.extract_data(
                bag_topic="/vins_estimator/EE/path", dict_var_type=POSE_VARS,
            )
            data_sets_3d[f"{label} VINS Loop Base"]          = DM.extract_data(
                bag_topic="/loop_fusion/base/pose_graph_path", dict_var_type=POSE_VARS,
            )
            data_sets_3d[f"{label} VINS Loop EE"]            = DM.extract_data(
                bag_topic="/loop_fusion/EE/pose_graph_path", dict_var_type=POSE_VARS,
            )
        # debug print:
        for label,data in data_sets_3d.items():
            print(f"> [{label}] t0:{data['t0']}")

        # # 4. Plot:
        ### pip install ipympl
        # fig, axs = plot_spatial(BagPlot, data_sets_3d, figsize=(10,8), view_angles=[(30,45)], show_orientations=False)
        angle_v = [[x] for x in PLOT_FEATURE_VIEW_ANGLES] if PLOT_FEATURE_VIEW_ANGLES_SEPARATED else [PLOT_FEATURE_VIEW_ANGLES]
        # plot:
        for j, angles in enumerate(angle_v):
            if PLOT_FEATURE_SCATTER_PLOT:
                fig, axs, title = plot_spatial(DM, data_sets_3d, scatter_or_line='scatter',
                    figsize=PLOT_FEATURE_FIG_SIZE_SCATTER, 
                    zero_orienting=PLOT_FEATURE_ORIENTING, 
                    show_orientations=PLOT_FEATURE_SHOW_ORIENTATIONS,
                    view_angles=angles,
                    bag_subset=bag_subset.value,
                    title=RUN_NAME,
                    cameras=cameras,
                    split_map=SPLIT_MAP,
                ) # default 3 views
                AM.save_fig(fig, f"{title}_{j}")
            if PLOT_FEATURE_LINE_PLOT:
                fig, axs, title = plot_spatial(DM, data_sets_3d, scatter_or_line='line',
                    figsize=PLOT_FEATURE_FIG_SIZE_LINE, 
                    zero_orienting=PLOT_FEATURE_ORIENTING,
                    show_orientations=False,
                    view_angles=angles,
                    bag_subset=bag_subset.value,
                    title=RUN_NAME,
                    split_map=SPLIT_MAP,
                ) # default 3 views
                AM.save_fig(fig, f"{title}_{j}")
    

# %% MAIN --------------------------------:
# - organize your replayed vins dataset in `uwarl_test_set.py`
# - run this script to generate plots

# -------------------------------- bag_test_set -------------------------------- #
# go through each test set:
for bag_test_case in [
        # TEST_SET_DUAL_MONO_IMU_0612_1017_v4,
        # TEST_SET_DUAL_MONO_IMU_0612_1022_v10,
        DUAL_MONO_IMU_1101_1104_comparison_v3,
    ]:
    N_args = len(sys.argv)
    if (N_args == 3):
        folder_id = sys.argv[1]
        bag_id = sys.argv[2]
        print(f"Giving index @ {folder_id}:{bag_id}")
    #TEST_SET_MONO_RGB_IMU_ACC_TIC, TEST_SET_MONO_RGB_IMU_INIT_GUESS_TIC]:
    #[TEST_SET_MONO_RGB_IMU, TEST_SET_MONO_IMU, TEST_SET_STEREO_IMU, TEST_SET_STEREO]:
    # go through all the bags set in each test set
    N = len(bag_test_case.TEST_SET.value)
    for test_index, bag_subset in enumerate(bag_test_case.TEST_SET.value):
        print("\n\n====== TEST [%d/%d] =====\n" % (test_index+1, N))
        # [DEV]: uncomment to skip n tests
        # if FEATURE_LOCAL_DEVELOPMENT and test_index < 5: # skip n tests
        #     continue
        
        # [MAIN]:
        if_exist = len(bag_subset.value) > 0
        if if_exist:
            # filter for the right bag
            if (N_args == 3):
                attr = bag_subset.value[0].split('_')[0].split('-')
                if attr[1] == folder_id and attr[2] == bag_id:
                    print(f"Found index @ {folder_id}:{bag_id}")
                else:
                    continue # skip this rung
            # generate report here:
            ic(bag_subset.value)
            generate_report(bag_test_case.__name__, bag_test_case.CONFIG.value, bag_subset)
        else:
            print(f"WARNING, test subset is empty, skipping tests {bag_subset.name}")
        
        # # [DEV]: uncomment to only run the first one
        # break
            
# %%
