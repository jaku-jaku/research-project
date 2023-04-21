# %% -------------------------------- Import Lib -------------------------------- %% #
# built-in
import os
from datetime import datetime
from pathlib import Path

# 3rd party lib
import numpy as np

# 3rd party util
from icecream import ic

# %% 
# -------------------------------- Import Our Lib -------------------------------- %% #
# ours:
from utils.uwarl_bag_parser import BagParser, TYPES_VAR

from configs.uwarl_common import PARSER_CALLBACKS
from configs.uwarl_test_set import TEST_SET_STEREO_IMU, TEST_SET_MONO_IMU, TEST_SET_STEREO, TEST_SET_SINGLE

from vins_replay_utils.uwarl_replay_decoder import auto_generate_labels_from_bag_file_name, ProcessedData
from vins_replay_utils.uwarl_analysis_plot import AnalysisManager, MultiBagsDataManager, plot_time_parallel, plot_time_series, plot_spatial

from scipy.ndimage import gaussian_filter1d

# -------------------------------- Files Automation -------------------------------- %% #
# # 1. Pre-Config
FIG_OUT_DIR = f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/research-project/output/vins_analysis"
FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS  = True
FEATURE_OUTPUT_BAG_META             = True
FEATURE_AUTO_SAVE                   = True
FEATURE_AUTO_CLOSE_FIGS             = True

PLOT_FEATURE_FIG_SIZE               = (10,8)
PLOT_FEATURE_ORIENTING              = False
PLOT_FEATURE_SHOW_ORIENTATIONS      = False
PLOT_FEATURE_VIEW_ANGLES            = [(30,10),(70,45),(10,10)]

# -------------------------------- REPORT -------------------------------- %% #
def generate_report(bag_test_case_name, bag_test_case_config, bag_subset):
    
    AUTO_BAG_DICT = auto_generate_labels_from_bag_file_name(bag_subset.value)
    ic(AUTO_BAG_DICT);
            
    # -------------------------------- Manager & Configs -------------------------------- %% #
    BP = BagParser(PARSER_CALLBACKS)
    AM = AnalysisManager(
        bag_dict=AUTO_BAG_DICT,
        output_dir=FIG_OUT_DIR,
        run_name="run_{}".format(datetime.now().strftime("%Y-%m-%d")), 
        test_set_name=bag_test_case_name,
        prefix=bag_subset.name,
        auto_save=FEATURE_AUTO_SAVE,
        auto_close=FEATURE_AUTO_CLOSE_FIGS,
        bag_directory=bag_test_case_config["directory"],
    )

    # # 2. Data Pre-Processing
    # -------------------------------- Pre-Processing -------------------------------- %% #
    # 1. Process and Aggregate data from multiple bags:
    pData={}
    for label, path in AM._bag_dict.items():
        pData[label] = ProcessedData(BP, AM._bag_directory, path)
    # -------------------------------- DEBUG -------------------------------- %% #
    # DEBUG: save a sample here:
    if FEATURE_OUTPUT_BAG_META:
        for label, data in pData.items():
            AM.save_dict(data.bag_samples, "bag_samples")
            AM.save_dict(data.bag_topics, "bag_topics")
            AM.save_dict(data.bag_info, "bag_info")
            break

    # # 3. Plotting Multiple datasets from multiple bagfiles
    # -------------------------------- Multi-Bag Data -------------------------------- %% #    
    # 2. Load into data plotter:
    DM = MultiBagsDataManager(pData)

    # -------------------------------- Plot: Voltage & Joint Efforts -------------------------------- #
    if FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS:
        # 3. assemble data sets:
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
        plot_time_series(AM, DM, data_sets_y)
        plot_time_parallel(AM, DM, data_sets_y, figsize=(15,4))

    # -------------------------------- Plot Data Prep: 3D trajectories -------------------------------- %% #
    # 3. assemble data sets:
    POSE_VARS = {
        TYPES_VAR.POSITION_XYZ: 'y',
        TYPES_VAR.ORIENTATION_XYZW: 'r',
    }
    data_sets_3d = dict()
    # TODO: please re-orient Vicon data based on the initial orientation:
    if "Base" in AM._prefix:
        data_sets_3d["Vicon Base"]         = DM.extract_data(
            bag_topic="/vicon/summit_base/summit_base", zeroing=True, dict_var_type=POSE_VARS,
        )
    else:
        data_sets_3d["Vicon EE"]              = DM.extract_data(
            bag_topic="/vicon/wam_EE/wam_EE", zeroing=True, dict_var_type=POSE_VARS,
        )
        # data_sets_3d["WAM base"]= BagPlot.extract_data(
        #     bag_topic="/vicon/base_EE/base_base", zeroing=True, dict_var_type=POSE_VARS,
        # ),

    vins_pre_process_funcs = None
    if "vins_pre_process_functions" in bag_test_case_config:
        vins_pre_process_funcs = bag_test_case_config["vins_pre_process_functions"]
        
    data_sets_3d.update({
        "VINS est"                          : DM.extract_data(
            bag_topic="/vins_estimator/path", zeroing=True, dict_var_type=POSE_VARS,
            pre_process_funcs=vins_pre_process_funcs,
        ),
        "VINS loop"                         : DM.extract_data(
            bag_topic="/loop_fusion/pose_graph_path", zeroing=True, dict_var_type=POSE_VARS,
            pre_process_funcs=vins_pre_process_funcs,
        ),
    })

    for label,data in data_sets_3d.items():
        print(f"> [{label}] t0:{data['t0']}")
        
    # # 4. Plot:
    ### pip install ipympl
    # fig, axs = plot_spatial(BagPlot, data_sets_3d, figsize=(10,8), view_angles=[(30,45)], show_orientations=False)
    fig, axs = plot_spatial(AM, DM, data_sets_3d, scatter_or_line='scatter',
        figsize=PLOT_FEATURE_FIG_SIZE, 
        zero_orienting=True, 
        show_orientations=PLOT_FEATURE_SHOW_ORIENTATIONS,
        view_angles=PLOT_FEATURE_VIEW_ANGLES,
    ) # default 3 views
    fig, axs = plot_spatial(AM, DM, data_sets_3d, scatter_or_line='line',
        figsize=PLOT_FEATURE_FIG_SIZE, 
        zero_orienting=PLOT_FEATURE_ORIENTING,
        show_orientations=PLOT_FEATURE_SHOW_ORIENTATIONS,
        view_angles=PLOT_FEATURE_VIEW_ANGLES,
    ) # default 3 views

# %% MAIN --------------------------------:
# - organize your replayed vins dataset in `uwarl_test_set.py`
# - run this script to generate plots

# -------------------------------- bag_test_set -------------------------------- #
# go through each test set:
for bag_test_case in [TEST_SET_MONO_IMU, TEST_SET_STEREO_IMU, TEST_SET_STEREO]:
    # go through all the bags set in each test set
    for bag_subset in bag_test_case:
        if_valid = bag_subset is not bag_test_case.CONFIG
        if_exist = len(bag_subset.value) > 0
        if if_valid and if_exist:
            generate_report(bag_test_case.__name__, bag_test_case.CONFIG.value, bag_subset)
            