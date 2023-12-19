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
from scipy.spatial.transform import Rotation as SO3

# 3rd party util
from icecream import ic

# %% 
# -------------------------------- Import Our Lib -------------------------------- %% #
# ours:
from utils.uwarl_bag_parser import BagParser, TYPES_VAR
from configs.uwarl_common import PARSER_CALLBACKS
# from configs.uwarl_test_set import TEST_SET_STEREO_IMU, TEST_SET_MONO_IMU, TEST_SET_STEREO, TEST_SET_SINGLE
# from configs.uwarl_test_set_d455 import (
#     TEST_SET_TITLE, 
#     DUAL_1108_BASICS_baseline_vs_decoupled,
#     DUAL_1108_DYNAMICS_baseline_vs_decoupled,
#     DUAL_1108_LONG_AM_baseline_vs_decoupled,
#     DUAL_1108_LONG_PM_baseline_vs_decoupled,
# )
# from configs.uwarl_test_set_d455_640 import (
#     TEST_SET_TITLE, 
#     DUAL_1115_BASICS_baseline_vs_decoupled,
#     DUAL_1115_DYNAMICS_baseline_vs_decoupled,
# )
# from configs.uwarl_test_set_d455_Nov22 import (
#     TEST_SET_TITLE,
#     DUAL_1122_BASIC_1,
#     DUAL_1122_BASIC_2,
#     DUAL_1122_BASIC_ROG,
#     DUAL_1122_LONG,
#     DUAL_1122_LONG_ROG,
# )
# from configs.uwarl_test_set_d455_Nov27 import (
#     TEST_SET_TITLE,
#     DUAL_1127_DEG_EVE,
#     DUAL_1127_DYN_EVE,
#     DUAL_1127_DEG_AM,
#     DUAL_1127_DYN_AM,
#     DUAL_1127_LONG_PM,
# )
# from configs.uwarl_test_set_d455_Dec07 import (
#     TEST_SET_TITLE,
#     DEMO_1207_A, DEMO_1207_B, DEMO_1207_C, 
#     DEMO_1207_A_v2, DEMO_1207_A_v3, DEMO_1207_B_v3, DEMO_1207_C_v3,
# )
from configs.uwarl_test_set_d455_Dec13_v2 import (
    TEST_SET_TITLE,
    DEMO_1213_B_STA,DEMO_1213_B_SPI,DEMO_1213_B_FWD,DEMO_1213_B_RVR,DEMO_1213_B_CIR,DEMO_1213_B_BEE,DEMO_1213_B_SQR,DEMO_1213_B_TRI,
    DEMO_1213_A_STA,DEMO_1213_A_SPI,DEMO_1213_A_FWD,DEMO_1213_A_RVR,DEMO_1213_A_CIR,DEMO_1213_A_BEE,DEMO_1213_A_SQR_A,DEMO_1213_A_SQR_B,DEMO_1213_A_TRI,
    DEMO_1213_C_ROG_1, DEMO_1213_C_ROG_2, DEMO_1213_C_LONG_SQR, DEMO_1213_C_SQR, DEMO_1213_C_ROG_3,
)
from vins_replay_utils.uwarl_replay_decoder import auto_generate_labels_from_bag_file_name_with_json_config, ProcessedData
from vins_replay_utils.uwarl_analysis_plot import ReportGenerator, AnalysisManager, MultiBagsDataManager, plot_time_parallel, plot_time_series, plot_spatial

from vins_replay_utils.uwarl_camera import MultiSensor_Camera_Node

# -------------------------------- Files Automation -------------------------------- %% #
# # 1. Pre-Config
FIG_OUT_DIR = f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/research-project/output/vins_analysis"
FEATURE_LOCAL_DEVELOPMENT  = True

FEATURE_ONLY_LAST                   = -1 #seconds: negative to iterate through entire bag

## OPTION:
# SPLIT_MAP = None
SPLIT_MAP = {1:"Base", 0:"EE"}   # to split graphs by devices

## OPTION:
# SPLIT_MATRICS = True           # split xyz and rpy
SPLIT_MATRICS = False 
RELATIVE_MATRICS = True

## OPTION:
FEATURE_AUTO_SAVE                   = True
FEATURE_AUTO_CLOSE_FIGS             = True
FEATURE_OUTPUT_BAG_META             = False

## OPTION:
FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS  = False
FEATURE_PLOT_3D_TRAJECTORIES        = True
FEATURE_PLOT_ERROR_METRICS          = True
FEATURE_PLOT_CAMERAS                = True
FEATURE_PLOT_CAM_CONFIGS            = False
FEATURE_OUTPUT_EXTRACTED_DATASET    = True

## OPTION:
FIGSIZE_ERR = (3,2)
PLOT_FEATURE_VIEW_ANGLES            = [(30,10),(70,45),(10,10)]#[(30,10),(70,45),(10,10)]
PLOT_FEATURE_VIEW_ANGLES_SEPARATED  = True

## OPTION: (Block List:)
# label_filters = {"unified":[]}                                 # ALL IN ONE
label_filters = {"odom":["Loop"], "loop":["Est"]}              # SPLIT FOR ODOM VS LOOP
# label_filters = {"coupled":["baseline"], "baseline":["coupled"]} # SPLIT FOR BASELINE VS COUPLED

## OPTION:
PLOT_FEATURE_AXIS_BOUNDARY_MAX      = [5,5,2] # <--- for whole floor rungs, we need to change this
PLOT_CONFIGS = {
    "line" : {
        "figsize":(4,4),
        "scatter_or_line":"line",
        "orientation_group": [],
    },
    # "scatter" : {
    #     "figsize": (4,4),
    #     "scatter_or_line": "scatter",
    #     "orientation_group": ["Est"],
    # },
}
RUN_NAME = ""
RUN_TAG = ""
if FEATURE_AUTO_CLOSE_FIGS:
    RUN_TAG = "[DEV]"
    
FEATURE_PROCESS_BAGS = (FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS or FEATURE_PLOT_3D_TRAJECTORIES)

### Prepare parser callbacks: (remove unused callbacks to minimize runtime)
parser_callbacks_ = PARSER_CALLBACKS
if not FEATURE_PROCESS_BAGS:
    parser_callbacks_.pop('/uwarl/robotnik_base_hw/voltage', None)
    parser_callbacks_.pop('/wam/joint_states', None)
    parser_callbacks_.pop('/wam/pose', None)

# -------------------------------- REPORT -------------------------------- %% #
def generate_report(bag_test_case_name, bag_test_case_config, bag_subset, report_generator=None, load_from_pickle=False):
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
    bag_rung_label_end = None
    for bag_rung_label, bag_rung in bag_test_case_config["rungs"].items():
        bag_rung_label_end = bag_rung_label
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
        BP = BagParser(parser_callbacks_)
        # 0.1 generate camera pose:
        cameras = []
        if FEATURE_PLOT_CAMERAS:
            # TODO: add camera plot functions
            print("> Process dual configuration file ...")
            cameras.append(MultiSensor_Camera_Node(_config_file=config_file, _prefix="d0_"))
            cameras.append(MultiSensor_Camera_Node(_config_file=config_file, _prefix="d1_"))
                
        if FEATURE_PLOT_CAM_CONFIGS: 
            print("> plot camera configs ...")
            for cam in cameras:
                fig, ax = cam.create_3d_figure()
                cam.plot_camera(ax=ax)
                AM.save_fig(fig, tag=f"{cam._prefix}camera_config")

        # 0.3 try to load pickle
        data_sets_3d = dict()
        if load_from_pickle:
            print("> Data loading from pickle!")
            try:
                data_sets_3d = AM.load_dict_from_pickle("data_sets_3d")
                print(data_sets_3d.keys())
            except Exception as e:
                print(f"> Data loading from pickle failed due to {e}! Now, load process from bag files ...")
                load_from_pickle = False # otherwise try to load all data
            
        # 1. Process and Aggregate data from multiple bags:
        tic = time.perf_counter()
        if FEATURE_PROCESS_BAGS:
            print("> Pre-Processing Bags ...")
            pData={}
            for label, path in AUTO_BAG_DICT.items():
                try:
                    # just need to load some metadata, 0.1s sufficient for load from pickle
                    t_last_s = 0.1 if load_from_pickle else FEATURE_ONLY_LAST 
                    pData[label] = ProcessedData(BP, bag_directory, path, T_LAST_S=t_last_s)
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
            print("> Creating Multi-Bag Data Manager ...")
            DMs[bag_rung_label] = MultiBagsDataManager(pData)
            print(f"> [{len(DMs)}]:({bag_rung_label}) Multi-Bag Data Manager Created!")

    # -------------------------------- Plot: Voltage & Joint Efforts -------------------------------- #
    if FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS and not load_from_pickle:
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
            fig,ax,_,_,title = plot_time_series(DM, data_sets_y, title=label)
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
        if not load_from_pickle:
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
        for label, data in data_sets_3d.items():
            print(f"> [{label}] t0:{data['t0']}")
            # print(data_sets_3d[label])

        # # 4. Plot:
        ### pip install ipympl
        # prep:
        angle_v = [[x] for x in PLOT_FEATURE_VIEW_ANGLES] if PLOT_FEATURE_VIEW_ANGLES_SEPARATED else [PLOT_FEATURE_VIEW_ANGLES]
        # label_filters = {"unified":[]} if not PLOT_FEATURE_ODOM_ONLY else {"odom":["Loop"], "loop":["Est"]}
        plot_boundary_max = bag_test_case_config["AXIS_BOUNDARY_MAX"] if "AXIS_BOUNDARY_MAX" in bag_test_case_config else PLOT_FEATURE_AXIS_BOUNDARY_MAX
        # plot:
        for name_lf, label_filter in label_filters.items():         # (separate loop and odom)
            for j, angles in enumerate(angle_v):                    # (separate view_angles)
                for config_name, config in PLOT_CONFIGS.items():    # (different plots)
                    fig, axs, title = plot_spatial(
                        bag_manager         =DMs[bag_rung_label_end], 
                        data_sets_3d        =data_sets_3d, 
                        title               =RUN_NAME, 
                        figsize             =config["figsize"], 
                        view_angles         =angles,
                        show_orientations   =(bool)(len(config["orientation_group"]) > 0), 
                        zero_orienting      =False,
                        scatter_or_line     =config["scatter_or_line"],
                        cameras             =cameras, 
                        split_map           =SPLIT_MAP,
                        show_cameras        =(bool)(len(cameras) > 0),
                        orientation_group   =config["orientation_group"],
                        label_filter        =label_filter,
                        AXIS_BOUNDARY_MAX   =plot_boundary_max,
                        # default params:
                        # N_sample=1, 
                        # N_orientations_sample=20, zero_position=False,
                        # projection='3d', proj_type='ortho',
                        # show_grid=True, AXIS_BOUNDARY_MAX=[5,5,2], AXIS_BOUNDARY_MIN=[0.5,0.5,0.2]
                    )
                    file_name = AM.save_fig(fig, f"{title}_{name_lf}_{j}")
                    # append to report at first view angle
                    if j==0 and report_generator and file_name:
                        report_generator.append_figname(bag_subset.name,name_lf,file_name)
    
    if FEATURE_OUTPUT_EXTRACTED_DATASET and not load_from_pickle:
        # df = pd.DataFrame(data_sets_3d)
        print("> Data saving!")
        AM.save_dict_as_pickle(data_sets_3d, "data_sets_3d")
        print("> Data saved!")
        
    if FEATURE_PLOT_ERROR_METRICS and FEATURE_PLOT_3D_TRAJECTORIES:
        # 1. compute error metrics and plot:
        for device in ["Base", "EE"]:
            data_sets_y = {}
            for label, DM in DMs.items():
                data_ref  = data_sets_3d[f"Vicon Cam {device} ({label})"]
                data_est  = data_sets_3d[f"{label} VINS Est {device}"]
                data_loop = data_sets_3d[f"{label} VINS Loop {device}"]
                
                N_sub = len(data_ref['t'])
                list_of_data_delta = []
                
                data_delta = {"Est": {"t": [], "Pos": [], "Rot": []}, "Loop": {"t": [], "Pos": [], "Rot": []}}
                for i in range(N_sub): # should be just one bag for this plot
                    t_ref  = data_ref['t'][i]
                    if len(t_ref) <= 0:
                        print("> No data, skipping ...")
                        continue # skip
                    t0_ref = data_ref['t0'][i]
                    q_ref  = np.array(data_ref['r'][i])
                    p_ref  = np.array(data_ref['y'][i])
                    N_ref = len(data_ref['t'][i])
                    q_corr_w2c = np.array([[1,0,0],[0,0,1],[0,-1,0]])
                    print(q_corr_w2c)
                    if device == 'Base':
                        # convert to camera axis as base axis is not aligned with vicon
                        R_ref = SO3.from_quat(q_ref).as_matrix() @ q_corr_w2c
                    else:
                        R_ref = SO3.from_quat(q_ref).as_matrix()
                    if SPLIT_MATRICS:
                        Re_ref = np.array(SO3.from_matrix(R_ref).as_euler('xyz', degrees=True))
                        ic(np.shape(Re_ref))
                    else:
                        R_ref = np.array(R_ref)
                    
                    def _get_delta(data):
                        N_est = len(data['t'][i])
                        t_  = np.array([])
                        x1_ = np.array([])
                        x2_ = np.array([])
                        if (N_est > 0): # data exists
                            t_est  = data['t'][i]
                            t0_est = data['t0'][i]
                            q_est  = np.array(data['r'][i])
                            p_est  = np.array(data['y'][i])
                            
                            if SPLIT_MATRICS:
                                Re_est = np.array(SO3.from_quat(q_est).as_euler('xyz', degrees=True))
                                ic(np.shape(Re_est))
                            else:
                                R_est = np.array(SO3.from_quat(q_est).as_matrix())
                                                            
                            delta_t = (t0_est)-(t0_ref+t_ref[0]) # compute how late estimation is
                            print(f">> T_est(0)):{t0_est}, T_ref(0): {t0_ref}, estimation is late for {delta_t}")
                            
                            # time alignment with tol 0.01s: 
                            selected_k = 0
                            if delta_t < 0:
                                assert(delta_t < 0), "OOps, Estimation is earlier than reference"
                            else:
                                for k in range(N_ref):
                                    if (t_ref[k]) > delta_t:
                                        break
                                    selected_k = k # cache index
                            
                            k_max = min(selected_k + N_est, N_ref-1)
                            k_max_est = min(N_est-1, (k_max - selected_k)) # in case estimator ran shorter
                            k_max = selected_k + k_max_est
                            
                            ic(k_max_est, k_max)
                            ic(np.shape(t_est), np.shape(t_ref))
                            t_est = np.array(t_est) + delta_t
                            d_t0 = t_est[0]-t_ref[selected_k]
                            d_t1 = t_est[k_max_est]-t_ref[k_max]
                            print(f">> compensated for: {delta_t}, start_delta: {d_t0}, end_delta: {d_t1}")
                            
                            delta_p = p_est[0:k_max_est, :] - p_ref[selected_k:k_max, :]
                            if SPLIT_MATRICS:
                                x1_ = np.array(delta_p)
                            else:
                                x1_ = np.linalg.norm(delta_p, axis=1)
                            # || q.T * q ||_2  : frobenius norm
                            # err_R = [np.linalg.norm((SO3.from_quat(q_ref[z+selected_k, :]).inv() * SO3.from_quat(q_est[z,:])).as_quat()) - 1 for z in range(N_est)] 
                            if SPLIT_MATRICS:
                                err_R = Re_est[0:k_max_est,:] - Re_ref[selected_k:k_max,:]
                            else:
                                err_R = [np.linalg.norm(np.matmul(R_est[z, :].transpose(), R_ref[z+selected_k, :]) - np.eye(3)) for z in range(k_max_est)]
                            ic(np.shape(err_R))
                            x2_ = np.array(err_R)
                            # delta_RPY = RPY_est - RPY_ref[selected_k:k_max, :]
                            # x2_ = delta_RPY[:, 2]
                            # print("np.shape(delta_R):", np.shape(delta_R))
                            # print("np.shape(x2_)", np.shape(x2_))
                            t_ = t_est[0:k_max_est]

                        return t_, x1_, x2_

                    t_, x1_, x2_ = _get_delta(data_est)
                    t2_, x3_, x4_ = _get_delta(data_loop)
                    ic(len(t_), np.shape(x1_), np.shape(x2_), np.shape(x3_), np.shape(x4_))
                    
                    if SPLIT_MATRICS:
                        for i in range(3):
                            data_delta = {"Est": {"t": [], "Pos": [], "Rot": []}, "Loop": {"t": [], "Pos": [], "Rot": []}}
                            if len(t_) > 1:
                                data_delta["Est"]["t"].append(t_.tolist())
                                data_delta["Est"]["Pos"].append(x1_[:,i].tolist())
                                data_delta["Est"]["Rot"].append(x2_[:,i].tolist())
                            else:
                                data_delta["Est"]["t"].append([])
                                data_delta["Est"]["Pos"].append([])
                                data_delta["Est"]["Rot"].append([])
                            if len(t2_) > 1:
                                data_delta["Loop"]["t"].append(t2_.tolist())
                                data_delta["Loop"]["Pos"].append(x3_[:,i].tolist())
                                data_delta["Loop"]["Rot"].append(x4_[:,i].tolist())
                            else:
                                data_delta["Loop"]["t"].append([])
                                data_delta["Loop"]["Pos"].append([])
                                data_delta["Loop"]["Rot"].append([])
                            list_of_data_delta.append(data_delta)
                    else:
                        data_delta["Est"]["t"].append(t_.tolist())
                        data_delta["Est"]["Pos"].append(x1_.tolist())
                        data_delta["Est"]["Rot"].append(x2_.tolist())
                        data_delta["Loop"]["t"].append(t2_.tolist())
                        data_delta["Loop"]["Pos"].append(x3_.tolist())
                        data_delta["Loop"]["Rot"].append(x4_.tolist())

                # plot:
            
                if SPLIT_MATRICS:
                    for i in range(3):
                        data_delta = list_of_data_delta[i]
                        for ver_ in ["Est", "Loop"]:
                            for type_ in ["Pos", "Rot"]:
                                key_ = f"{ver_} {type_} Err ({device}) [{i}]"
                                if key_ not in data_sets_y:
                                    data_sets_y[f"{key_}"] = {}
                                data_sets_y[f"{key_}"][f"{label}"] = {'t': data_delta[ver_]['t'], 'y': data_delta[ver_][type_]}
                else:
                    for ver_ in ["Est", "Loop"]:
                        for type_ in ["Pos", "Rot"]:
                            key_ = f"{ver_} {type_} Err ({device}) "
                            if key_ not in data_sets_y:
                                data_sets_y[f"{key_}"] = {}
                            data_sets_y[f"{key_}"][f"{label}"] = {'t': data_delta[ver_]['t'], 'y': data_delta[ver_][type_]}
                            # data_sets_y[f"{ver_} {type_} Err ({device})"][f"{type_} {label}"] = {'t': [[]], 'y': [[]]}
                # data_sets_y[f"VINS_Loop-Vicon {device} ({label})"] = {'t': t, 'y': x}
            
            for title_, data_set_ in data_sets_y.items():
                fig,ax,mu,std,title = plot_time_series(DM, data_set_, title=title_, align_y=True, if_mu=True, figsize=FIGSIZE_ERR, if_label_bags=False)
                if title:
                    file_name = AM.save_fig(fig, title)
                    # report_generator.append_figname(bag_subset.name, title_, file_name)
                    report_generator.append_variance(bag_subset.name, title_, mu, std)
                else:
                    # report_generator.append_figname(bag_subset.name, title_, "N/A")
                    report_generator.append_variance(bag_subset.name, title_, None, None)
                ic(file_name)
                

# %% MAIN --------------------------------:
# - organize your replayed vins dataset in `uwarl_test_set.py`
# - run this script to generate plots

# -------------------------------- bag_test_set -------------------------------- #
# go through each test set:
for bag_test_case in [ 
        # DUAL_1108_BASICS_baseline_vs_decoupled,
        # DUAL_1108_DYNAMICS_baseline_vs_decoupled,
        # DUAL_1108_LONG_AM_baseline_vs_decoupled,
        # DUAL_1108_LONG_PM_baseline_vs_decoupled,
        # # DUAL_1115_BASICS_baseline_vs_decoupled,
        # # DUAL_1115_DYNAMICS_baseline_vs_decoupled,
        # DUAL_1122_BASIC_1,
        # DUAL_1122_BASIC_2,
        # DUAL_1122_BASIC_ROG,
        # DUAL_1122_LONG,
        # DUAL_1122_LONG_ROG,
        # DUAL_1127_DEG_EVE, 
        # DUAL_1127_DYN_EVE,
        # DUAL_1127_DEG_AM, 
        # DUAL_1127_LONG_PM,
        # DUAL_1127_DYN_AM, 
        # DEMO_1207_A, DEMO_1207_B, DEMO_1207_C, 
        # DEMO_1207_C_Occ1, DEMO_1207_C_Occ2, DEMO_1207_C_Occ3
        # DEMO_1207_A_v2,
        # DEMO_1207_A_v3,
        # DEMO_1207_B_v3, 
        # DEMO_1207_C_v3,
        DEMO_1213_A_STA,DEMO_1213_A_SPI,DEMO_1213_A_FWD,DEMO_1213_A_RVR,DEMO_1213_A_CIR,DEMO_1213_A_BEE,DEMO_1213_A_SQR_A,DEMO_1213_A_SQR_B,DEMO_1213_A_TRI,
        # DEMO_1213_B_STA,DEMO_1213_B_SPI,DEMO_1213_B_FWD,DEMO_1213_B_RVR,DEMO_1213_B_CIR,DEMO_1213_B_BEE,DEMO_1213_B_SQR,DEMO_1213_B_TRI,
        # DEMO_1213_C_ROG_1, DEMO_1213_C_ROG_2, DEMO_1213_C_LONG_SQR, DEMO_1213_C_SQR, DEMO_1213_C_ROG_3,
    ]:
    print("\n================================")
    print(f"\n==={bag_test_case}===")
    print("\n================================\n")
    N_args = len(sys.argv)
    folder_id = "all"
    bag_id = "all"
    option = "bagfiles"
    if (N_args >= 3):
        folder_id = sys.argv[1]
        bag_id = sys.argv[2]
        if (N_args == 4):
            option = sys.argv[3]
        print(f"Giving index @ {folder_id}:{bag_id} ~{option}")
    #TEST_SET_MONO_RGB_IMU_ACC_TIC, TEST_SET_MONO_RGB_IMU_INIT_GUESS_TIC]:
    #[TEST_SET_MONO_RGB_IMU, TEST_SET_MONO_IMU, TEST_SET_STEREO_IMU, TEST_SET_STEREO]:
    # go through all the bags set in each test set
    N = len(bag_test_case.TEST_SET.value)
    # [MAIN]:
    RG = ReportGenerator(bag_test_case, f"run_{folder_id}_{bag_id}_{option}")
    for test_index, bag_subset in enumerate(bag_test_case.TEST_SET.value):
        print("\n\n====== TEST [%d/%d] =====\n" % (test_index+1, N))
        # [DEV]: uncomment to skip n tests
        # if FEATURE_LOCAL_DEVELOPMENT and test_index < 5: # skip n tests
        #     continue
        
        if_exist = len(bag_subset.value) > 0
        if if_exist:
            # filter for the right bag
            attr = bag_subset.value[0].split('_')[0].split('-')
            if (attr[1] == folder_id or bag_id=="all") and (attr[2] == bag_id or bag_id == "all"): 
                # process specific folder at a specific child or all children
                print(f"Found index @ {folder_id}:{bag_id} with {option}")
            elif (attr[1] > folder_id and (option=="all" or option=="picke") and bag_id == "all"): 
                # process any folder after given folder_id
                print(f"Found index > {folder_id}:{bag_id} with {option}")
            else:
                continue # skip this rung
            # [REPORT]:
            print(f"> Generating report for {bag_subset.name}:{bag_subset.value}")
            generate_report(bag_test_case.__name__, bag_test_case.CONFIG.value, bag_subset, 
                            report_generator=RG, load_from_pickle=(bool)(option=="pickle"))
            RG.save_report_as_md()
        else:
            print(f"> WARNING, test subset is empty, skipping tests {bag_subset.name}")
        
        # # [DEV]: uncomment to only run the first one
        # break
            
# %%
