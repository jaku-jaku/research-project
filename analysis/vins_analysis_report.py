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
from configs.uwarl_test_set_d455_Nov22 import (
    TEST_SET_TITLE,
    DUAL_1122_BASIC_1,
    DUAL_1122_BASIC_2,
    DUAL_1122_BASIC_ROG,
    DUAL_1122_LONG,
    DUAL_1122_LONG_ROG,
)

from vins_replay_utils.uwarl_replay_decoder import auto_generate_labels_from_bag_file_name_with_json_config, ProcessedData
from vins_replay_utils.uwarl_analysis_plot import ReportGenerator, AnalysisManager, MultiBagsDataManager, plot_time_parallel, plot_time_series, plot_spatial

from vins_replay_utils.uwarl_camera import MultiSensor_Camera_Node

# -------------------------------- Files Automation -------------------------------- %% #
# # 1. Pre-Config
FIG_OUT_DIR = f"{Path.home()}/UWARL_catkin_ws/src/vins-research-pkg/research-project/output/vins_analysis"
FEATURE_LOCAL_DEVELOPMENT  = True

FEATURE_ONLY_LAST                   = -1 #seconds

SPLIT_MAP = None
SPLIT_MAP = {1:"Base", 0:"EE"}

FEATURE_AUTO_SAVE                   = True
FEATURE_AUTO_CLOSE_FIGS             = True
FEATURE_OUTPUT_BAG_META             = False

FEATURE_PLOT_VOLTAGE_JOINT_EFFORTS  = False
FEATURE_PLOT_3D_TRAJECTORIES        = True
FEATURE_PLOT_ERROR_METRICS          = True
FEATURE_PLOT_CAMERAS                = True
FEATURE_PLOT_CAM_CONFIGS            = False
FEATURE_OUTPUT_EXTRACTED_DATASET    = True

FIGSIZE_ERR = (3,3)
PLOT_FEATURE_VIEW_ANGLES            = [(30,10),(70,45),(10,10)]#[(30,10),(70,45),(10,10)]
PLOT_FEATURE_VIEW_ANGLES_SEPARATED  = True
PLOT_FEATURE_ODOM_ONLY              = True
PLOT_FEATURE_AXIS_BOUNDARY_MAX      = [5,5,2] # <--- for whole floor rungs, we need to change this
PLOT_CONFIGS = {
    "line" : {
        "figsize":(4,4),
        "scatter_or_line":"line",
        "orientation_group": [],
    },
    "scatter" : {
        "figsize": (8,8),
        "scatter_or_line": "scatter",
        "orientation_group": ["Est"],
    },
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
def generate_report(bag_test_case_name, bag_test_case_config, bag_subset, report_generator=None):
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
        BP = BagParser(parser_callbacks_)
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
        # prep:
        angle_v = [[x] for x in PLOT_FEATURE_VIEW_ANGLES] if PLOT_FEATURE_VIEW_ANGLES_SEPARATED else [PLOT_FEATURE_VIEW_ANGLES]
        label_filters = {"unified":[]} if not PLOT_FEATURE_ODOM_ONLY else {"odom":["Loop"], "loop":["Est"]}
        plot_boundary_max = bag_test_case_config["AXIS_BOUNDARY_MAX"] if "AXIS_BOUNDARY_MAX" in bag_test_case_config else PLOT_FEATURE_AXIS_BOUNDARY_MAX
        # plot:
        for name_lf, label_filter in label_filters.items():         # (separate loop and odom)
            for j, angles in enumerate(angle_v):                    # (separate view_angles)
                for config_name, config in PLOT_CONFIGS.items():    # (different plots)
                    fig, axs, title = plot_spatial(
                        bag_manager         =DM, 
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
                    # append to report
                    if report_generator and file_name:
                        report_generator.append_figname(file_name)
    
    if FEATURE_OUTPUT_EXTRACTED_DATASET:
        # df = pd.DataFrame(data_sets_3d)
        print("> Data saving!")
        AM.save_dict_as_pickle(data_sets_3d, "data_sets_3d")
        # AM.save_dict(data_sets_3d, "data_sets_3d")
        print("> Data saved!")
        
    if FEATURE_PLOT_ERROR_METRICS and FEATURE_PLOT_3D_TRAJECTORIES:
        # 1. compute error metrics and plot:
        for device in ["Base", "EE"]:
            data_sets_y1 = dict() 
            data_sets_y2 = dict() 
            data_sets_y3 = dict() 
            data_sets_y4 = dict() 
            for label, DM in DMs.items():
                data_ref  = data_sets_3d[f"Vicon Cam {device} ({label})"]
                data_est  = data_sets_3d[f"{label} VINS Est {device}"]
                data_loop = data_sets_3d[f"{label} VINS Loop {device}"]
                
                N_sub = len(data_ref['t'])
                t1 = []
                x1 = []
                x2 = []
                t2 = []
                x3 = []
                x4 = []
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
                        R_ref = np.array(SO3.from_quat(q_ref).as_matrix() @ q_corr_w2c) 
                    else:
                        R_ref = np.array(SO3.from_quat(q_ref).as_matrix())
    
                    ic(np.shape(R_ref))
                    
                    def _get_delta(data):
                        N_est = len(data['t'][i])
                        t_  = np.array([])
                        x1_ = np.array([])
                        x2_ = np.array([])
                        if (N_est > 0): # data exists
                            t_est  = data['t'][i]
                            t0_est = data['t0'][i]
                            q_est  = np.array(data['r'][i])
                            p_est  = data['y'][i]
                            
                            R_est = np.array(SO3.from_quat(q_est).as_matrix())
                           
                            delta_t = t0_est - t0_ref # compute how late estimation is
                            print(f">> T_est(0)):{t0_est}, T_ref(0): {t0_ref}, estimation is late for {delta_t}")
                            
                            # time alignment with tol 0.01s: 
                            selected_k = 0
                            if delta_t < 0:
                                assert(delta_t < 0), "OOps, Estimation is earlier than reference"
                            else:
                                for k in range(N_ref):
                                    if (delta_t - t_ref[k]) > 0.01:
                                        break
                                    selected_k = k # cache index

                            d_t = t_est[-1]-t_ref[selected_k+N_est]
                            k_max = min(selected_k+N_est, N_ref)
                            print(f">> T_est(-1)={t_est[-1]}, T_ref(-1)={t_ref[k_max]}, delta: {d_t}")
                            
                            t_ = np.array(t_est) + delta_t
                            delta_p = np.array(p_est) - p_ref[selected_k:k_max, :]
                            x1_ = np.linalg.norm(delta_p, axis=1)
                            # || q.T * q ||_2  : frobenius norm
                            # err_R = [np.linalg.norm((SO3.from_quat(q_ref[z+selected_k, :]).inv() * SO3.from_quat(q_est[z,:])).as_quat()) - 1 for z in range(N_est)] 
                            err_R = [np.linalg.norm(R_est[z, :].T @ R_ref[z+selected_k, :] - np.eye(3)) for z in range(N_est)]
                            ic(np.shape(err_R))
                            x2_ = np.array(err_R)
                            # delta_RPY = RPY_est - RPY_ref[selected_k:k_max, :]
                            # x2_ = delta_RPY[:, 2]
                            # print("np.shape(delta_R):", np.shape(delta_R))
                            # print("np.shape(x2_)", np.shape(x2_))

                        return t_, x1_, x2_

                    t_, x1_, x2_ = _get_delta(data_est)
                    t2_, x3_, x4_ = _get_delta(data_loop)
                    t1.append(t_.tolist())
                    x1.append(x1_.tolist())
                    x2.append(x2_.tolist())
                    t2.append(t2_.tolist())
                    x3.append(x3_.tolist())
                    x4.append(x4_.tolist())

                data_sets_y1[f"VINS_Est {label}"] = {'t': t1, 'y': x1}
                data_sets_y2[f"VINS_Est {label}"] = {'t': t1, 'y': x2}
                data_sets_y3[f"VINS_Loop {label}"] = {'t': t2, 'y': x3}
                data_sets_y4[f"VINS_Loop {label}"] = {'t': t2, 'y': x4}
                
                # data_sets_y[f"VINS_Loop-Vicon {device} ({label})"] = {'t': t, 'y': x}
            fig,ax,title = plot_time_series(DM, data_sets_y1, title=f"Est Pos Err ({device})", align_y=True, if_mu=True, figsize=FIGSIZE_ERR)
            file_name = AM.save_fig(fig, title)
            fig,ax,title = plot_time_series(DM, data_sets_y2, title=f"Est Rot Err ({device})", align_y=True, if_mu=True, figsize=FIGSIZE_ERR)
            file_name = AM.save_fig(fig, title)
            fig,ax,title = plot_time_series(DM, data_sets_y3, title=f"Loop Pos Err ({device})", align_y=True, if_mu=True, figsize=FIGSIZE_ERR)
            file_name = AM.save_fig(fig, title)
            fig,ax,title = plot_time_series(DM, data_sets_y4, title=f"Loop Rot Err ({device})", align_y=True, if_mu=True, figsize=FIGSIZE_ERR)
            file_name = AM.save_fig(fig, title)
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
        DUAL_1122_BASIC_1,
        DUAL_1122_BASIC_2,
        DUAL_1122_BASIC_ROG,
        DUAL_1122_LONG,
        DUAL_1122_LONG_ROG,
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
        RG = ReportGenerator("temp" if N_args == 3 else "Overall")
        if_exist = len(bag_subset.value) > 0
        if if_exist:
            # filter for the right bag
            if (N_args == 3):
                attr = bag_subset.value[0].split('_')[0].split('-')
                if attr[1] == folder_id and attr[2] == bag_id:
                    print(f"Found index @ {folder_id}:{bag_id}")
                else:
                    continue # skip this rung
            # [REPORT]:
            print(f"> Generating report for {bag_subset.name}:{bag_subset.value}")
            generate_report(bag_test_case.__name__, bag_test_case.CONFIG.value, bag_subset, report_generator=RG)
            RG.save_report_as_md()
        else:
            print(f"> WARNING, test subset is empty, skipping tests {bag_subset.name}")
        
        # # [DEV]: uncomment to only run the first one
        # break
            
# %%
