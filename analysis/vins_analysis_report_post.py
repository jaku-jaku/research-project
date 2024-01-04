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
import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# 3rd party util
from icecream import ic

# %% 
# -------------------------------- Import Our Lib -------------------------------- %% #
# ours:
from vins_replay_utils.uwarl_reporter import ReportGenerator, AnalysisManager

# data labels:
from configs.uwarl_test_set_d455_Dec13_v2 import (
    TEST_SET_TITLE,
    DEMO_1213_A_SQR,DEMO_1213_A_SPI,DEMO_1213_A_FWD,DEMO_1213_A_RVR,DEMO_1213_A_CIR,DEMO_1213_A_BEE,DEMO_1213_A_SQR_A,DEMO_1213_A_SQR_B,DEMO_1213_A_TRI,
)

# %% -------------------------------- Config -------------------------------- %% #
CONFIG_LOCAL_DIR = "/Users/jaku/Downloads/run_2023-12-20/[DEV]D455_v2"
ALL_TEST_SETS = [DEMO_1213_A_SPI,DEMO_1213_A_FWD,DEMO_1213_A_RVR,DEMO_1213_A_CIR,DEMO_1213_A_BEE,DEMO_1213_A_SQR,DEMO_1213_A_TRI]
FIG_OUT_DIR = CONFIG_LOCAL_DIR # same as local

Q_CORR_W2C = np.array([[1,0,0],[0,0,1],[0,-1,0]])


## time alignment:
DEVICES     = ["Base", "EE"]
RUN_LABELS  = ["baseline", "coupled (ours)"]
ERROR_KEYS  = ["est_pe", "est_qe", "loop_pe", "loop_qe"]

## user:
FEATURE_PLOT_ERROR_PER_TEST_SET = False
FEATURE_GENERATE_SUMMARY        = True
BAR_PLOT_SIZE_ERROR_SUMMARY     = (10,2)
BAR_PLOT_SIZE_ERROR_TEST_SET    = (12,4)
FEATURE_ZERO_ORIENTATION_WRT_INIT = False # NOT needed for ATE, for sanity check only
# %% -------------------------------- REPORT -------------------------------- %% #
# 0. init report generator:
date = datetime.now().strftime("%Y-%m-%d")
RG = ReportGenerator(title="Summary (post-run)", tag=f"run_{date}")
AM = AnalysisManager(
    output_dir=FIG_OUT_DIR,
    run_name=f"SUMMARY_(post-run)", 
    test_set_name=f"post-run_{date}",
    prefix=TEST_SET_TITLE, # Unused
    auto_save=True,
    auto_close=True,
)
RG.bind_output_dir(output_dir=AM._output_dir)

# %% 1. Table Result Expected:
TARGET_EE_MOTIONS = ["LR-EE", "LR-Base", "UD-EE", "UD-Base"]
TABULAR_RESULT = {}
TABULAR_PLOT_DATA = {}
for key in ERROR_KEYS:
    TABULAR_RESULT[key] = {}
    TABULAR_PLOT_DATA[key] = {}
    for label in RUN_LABELS:
        TABULAR_RESULT[key][label] = {}
        TABULAR_PLOT_DATA[key][label] = {}
        for ee_motion in TARGET_EE_MOTIONS:
            TABULAR_RESULT[key][label][ee_motion] = {}
            TABULAR_PLOT_DATA[key][label][ee_motion] = {}
            for base_motion in ["SPI", "FWD", "RVR", "CIR", "SQR","BEE", "TRI"]:
                TABULAR_RESULT[key][label][ee_motion][base_motion] = 0.0
                TABULAR_PLOT_DATA[key][label][ee_motion][base_motion] = []

# %% 2. gather pickles:
test_error_dict = {} # DEBUG
for test_set in ALL_TEST_SETS:
    TEST_SET_DIR = os.path.join(CONFIG_LOCAL_DIR, test_set.__name__)
    print(f"# Processing {test_set}@{TEST_SET_DIR}")
    
    test_error_dict = {}
    for key in ERROR_KEYS:
        test_error_dict[key] = {}
    for test in test_set.TEST_SET:
        TEST_TAG = test.name
        TEST_PICKLE = f"{TEST_TAG}_data_sets_3d"
        print(f"  > Indexing {test:8s}:{TEST_PICKLE}")
        # ---- LOAD DATA ---- #
        ## load data:
        data_ = AM.load_dict_from_pickle(file_name=TEST_PICKLE, input_path=TEST_SET_DIR)
        ## create output folder:
        path_ = RG.create_subfolder(folder_name=f"{test_set.__name__}/{test}")
        # ---- RAW DATA ---- #
        ## convert to csv files in a folder:
        for key_ in data_.keys():
            file_name = f"{path_}/[raw] {key_}.csv"
            # restructure:
            data_sub = {}
            t0_ = data_[key_]['t0']
            is_valid_ = (bool)(len(t0_) and t0_[0] > 0)
            if is_valid_:
                t_R1 = data_[key_]['t'][0]
                y_R3 = np.array(data_[key_]['y'][0])
                r_R4 = np.array(data_[key_]['r'][0])
                data_sub['t0']  = t0_[0]
                data_sub['t']   = t_R1
                data_sub['p_x'] = y_R3[:,0]
                data_sub['p_y'] = y_R3[:,1]
                data_sub['p_z'] = y_R3[:,2]
                data_sub['q_x'] = r_R4[:,0]
                data_sub['q_y'] = r_R4[:,1]
                data_sub['q_z'] = r_R4[:,2]
                data_sub['q_w'] = r_R4[:,3]
            pd.DataFrame(data_sub).to_csv(file_name, index = False)
            print(f"       - {file_name}")
            
        # ---- ALIGNED DATA ---- #
        # ic(data_.keys())
        for device in DEVICES:
            for key in ERROR_KEYS:
                if device not in test_error_dict[key]:
                    test_error_dict[key][device] = {}
            for label in RUN_LABELS:
                for key in ERROR_KEYS:
                    if label not in test_error_dict[key][device]:
                        test_error_dict[key][device][label] = {}
                data_ref  = data_[f"Vicon Cam {device} ({label})"]
                data_est  = data_[f"{label} VINS Est {device}"]
                data_loop = data_[f"{label} VINS Loop {device}"]
                
                is_valid_ = (bool)(len(data_ref['t0']) == 1 and data_ref['t0'][0] > 0) # should be one bag only and positive
                if is_valid_:
                    t0_ref = data_ref['t0'][0]
                    t_ref  = data_ref['t'][0]
                    q_ref  = np.array(data_ref['r'][0])
                    p_ref  = np.array(data_ref['y'][0])
                    N_ref  = len(t_ref)
                    
                    # Align Data wrt Est/Loop:
                    def _get_aligned_data(data_pred): # align time to estimation
                        is_valid_ = (bool)(len(data_pred['t0']) == 1 and data_pred['t0'][0] > 0)
                        if not is_valid_: 
                            return {}
                        # data exists:
                        t0_pred = data_pred['t0'][0]
                        t_pred  = data_pred['t'][0]
                        q_pred  = np.array(data_pred['r'][0])
                        p_pred  = np.array(data_pred['y'][0])
                        N_pred  = len(t_pred)
                    
                        delta_t = (t0_pred)-(t0_ref+t_ref[0]) # compute how late estimation is
                        print(f"\t\t>> T_pred(0)):{t0_pred}, T_ref(0): {t0_ref}, estimation is late for {delta_t}")
                        
                        selected_k = 0
                        if delta_t < 0:
                            assert(delta_t < 0), "OOps, Estimation is earlier than reference"
                        else:
                            for k in range(N_ref):
                                if (t_ref[k]) > delta_t:
                                    if (t_ref[k]-delta_t) < (delta_t-t_ref[k-1]):
                                        selected_k = k # cache last index if its closer
                                    break
                                selected_k = k # cache index
                        # filter index:
                        k_max = min(selected_k + N_pred, N_ref-1)
                        k_max_est = min(N_pred-1, (k_max - selected_k)) # in case estimator ran shorter
                        k_max = selected_k + k_max_est
                        # ic(k_max_est, k_max, np.shape(t_pred), np.shape(t_ref))
                        # offset prediction time:
                        t_pred = np.array(t_pred) + delta_t
                        d_t0 = t_pred[0]-t_ref[selected_k]
                        d_t1 = t_pred[k_max_est]-t_ref[k_max]
                        print(f"\t\t\t>> compensated for: {delta_t}, start_delta: {d_t0}, end_delta: {d_t1}")
                        
                        aligned_data_ = {
                            't0': t0_pred,
                            't':  t_pred[0:k_max_est],
                            'q':  q_pred[0:k_max_est,:],
                            'p':  p_pred[0:k_max_est,:],
                            'tr': t_ref[selected_k:k_max],
                            'qr': q_ref[selected_k:k_max,:],
                            'pr': p_ref[selected_k:k_max,:],
                        }
                        return aligned_data_
                    
                    # - alignment:
                    aligned_data_est  = _get_aligned_data(data_est)
                    aligned_data_loop = _get_aligned_data(data_loop)
                    
                    # Parse aligned data:
                    def parse_aligned_data(aligned_data):
                        if aligned_data:
                            ## DEBUG:
                            # ic(
                            #     np.shape(aligned_data['t0']),
                            #     np.shape(aligned_data['t']),
                            #     np.shape(aligned_data['q']),
                            #     np.shape(aligned_data['p']),
                            #     np.shape(aligned_data['tr']),
                            #     np.shape(aligned_data['qr']),
                            #     np.shape(aligned_data['pr'])
                            # )
                            parsed_data = {
                                't0':   aligned_data['t0'],
                                't':    aligned_data['t'][:],
                                'q_x':  aligned_data['qr'][:,0],
                                'q_y':  aligned_data['qr'][:,1],
                                'q_z':  aligned_data['qr'][:,2],
                                'q_w':  aligned_data['qr'][:,3],
                                'p_x':  aligned_data['pr'][:,0],
                                'p_y':  aligned_data['pr'][:,1],
                                'p_z':  aligned_data['pr'][:,2],
                                'tr':   aligned_data['tr'][:],
                                'qr_x': aligned_data['qr'][:,0],
                                'qr_y': aligned_data['qr'][:,1],
                                'qr_z': aligned_data['qr'][:,2],
                                'qr_w': aligned_data['qr'][:,3],
                                'pr_x': aligned_data['pr'][:,0],
                                'pr_y': aligned_data['pr'][:,1],
                                'pr_z': aligned_data['pr'][:,2],
                            }
                            return parsed_data
                        else:
                            return None
                    
                    # - parse
                    parsed_data_est  = parse_aligned_data(aligned_data_est)
                    parsed_data_loop = parse_aligned_data(aligned_data_loop)
                    
                    # save to csv:
                    pd.DataFrame(parsed_data_est ).to_csv(f"{path_}/[aligned] Est--vs-GT {device} ({label}).csv", index = False)
                    pd.DataFrame(parsed_data_loop).to_csv(f"{path_}/[aligned] Loop-vs-GT {device} ({label}).csv", index = False)
        
                    # ---- COMPUTE ERROR ---- #
                    def process_aligned_data_global_error(aligned_data):
                        if aligned_data:
                            # convert to numpy array:
                            t0_ = aligned_data['t0']
                            t_  = np.array(aligned_data['t'])
                            q_  = np.array(aligned_data['q'])
                            p_  = np.array(aligned_data['p'])
                            tr_ = np.array(aligned_data['tr'])
                            qr_ = np.array(aligned_data['qr'])
                            pr_ = np.array(aligned_data['pr'])
                            # compute error:
                            N_ = len(t_)
                            # global metrics:
                            e_metric = np.zeros((N_, 2))
                            e_metric[:,0] = np.linalg.norm(p_ - pr_, axis=1)
                            
                            if FEATURE_ZERO_ORIENTATION_WRT_INIT:
                                Rz0 = SO3.from_quat(q_[0,:]).as_matrix()
                                Rr0_T = SO3.from_quat(qr_[0,:]).as_matrix().transpose()
                                # zeroing orientation wrt itself.
                                for z in range(N_):
                                    RzT_ = SO3.from_quat(q_[z,:]).as_matrix().transpose() * Rz0
                                    Rzr_ = Rr0_T * SO3.from_quat(qr_[z,:]).as_matrix()
                                    e_metric[z,1] = np.linalg.norm(np.matmul(RzT_, Rzr_) - np.eye(3), ord='fro')
                            else: # direct metric:
                                for z in range(N_):
                                    RzT_ = SO3.from_quat(q_[z,:]).as_matrix().transpose()
                                    Rzr_ = SO3.from_quat(qr_[z,:]).as_matrix()
                                    if device == "Base":
                                        Rzr_ =  Rzr_ @ Q_CORR_W2C # world to camera axis
                                    e_metric[z,1] = np.linalg.norm(np.matmul(RzT_, Rzr_) - np.eye(3), ord='fro')
                                
                            return e_metric
                        else:
                            return None
                    
                    e_metric_est  = process_aligned_data_global_error(aligned_data_est )
                    e_metric_loop = process_aligned_data_global_error(aligned_data_loop)
                    
                    # update and save to csv:
                    if parsed_data_est:
                        parsed_data_est.update({'pe': e_metric_est[:,0],'qe': e_metric_est[:,1]})
                        pd.DataFrame(parsed_data_est ).to_csv(f"{path_}/[error] Est--vs-GT {device} ({label}).csv", index = False)
                    if parsed_data_loop:
                        parsed_data_loop.update({'pe': e_metric_loop[:,0],'qe': e_metric_loop[:,1]})
                        pd.DataFrame(parsed_data_loop).to_csv(f"{path_}/[error] Loop-vs-GT {device} ({label}).csv", index = False)
                    
                    # cache for report:
                    if FEATURE_PLOT_ERROR_PER_TEST_SET:
                        if parsed_data_est:
                            test_error_dict["est_pe"][device][label][TEST_TAG] = e_metric_est[:,0]
                            test_error_dict["est_qe"][device][label][TEST_TAG] = e_metric_est[:,1]
                        if parsed_data_loop:
                            test_error_dict["loop_pe"][device][label][TEST_TAG] = e_metric_loop[:,0]
                            test_error_dict["loop_qe"][device][label][TEST_TAG] = e_metric_loop[:,1]
                    
                    # cache for greater table result:
                    if FEATURE_GENERATE_SUMMARY:
                        try:
                            TABULAR_RESULT["est_pe"][label][f"{TEST_TAG}-{device}"][f"{test_set.TEST_SET.__name__}"] = np.mean(e_metric_est[:,0] )
                            TABULAR_RESULT["est_qe"][label][f"{TEST_TAG}-{device}"][f"{test_set.TEST_SET.__name__}"] = np.mean(e_metric_est[:,1] )
                            TABULAR_PLOT_DATA["est_pe"][label][f"{TEST_TAG}-{device}"][f"{test_set.TEST_SET.__name__}"] = e_metric_est[:,0] 
                            TABULAR_PLOT_DATA["est_qe"][label][f"{TEST_TAG}-{device}"][f"{test_set.TEST_SET.__name__}"] = e_metric_est[:,1] 
                            if parsed_data_loop:
                                TABULAR_RESULT["loop_pe"][label][f"{TEST_TAG}-{device}"][f"{test_set.TEST_SET.__name__}"] = np.mean(e_metric_loop[:,0])
                                TABULAR_RESULT["loop_qe"][label][f"{TEST_TAG}-{device}"][f"{test_set.TEST_SET.__name__}"] = np.mean(e_metric_loop[:,1])
                                TABULAR_PLOT_DATA["loop_pe"][label][f"{TEST_TAG}-{device}"][f"{test_set.TEST_SET.__name__}"] = e_metric_loop[:,0]
                                TABULAR_PLOT_DATA["loop_qe"][label][f"{TEST_TAG}-{device}"][f"{test_set.TEST_SET.__name__}"] = e_metric_loop[:,1]
                        except KeyError:
                            pass
                    
                    # e_metric_mu = np.mean(e_metric, axis=0)
                    # e_metric_std = np.std(e_metric, axis=0)
                    
                
    # ---- PLOT PER SET of TESTs ---- #
    # plot error bar:
    if FEATURE_PLOT_ERROR_PER_TEST_SET:
        for key_ in ERROR_KEYS:
            for dev_ in DEVICES:
                fig, axes = plt.subplots(nrows=1, ncols=2, 
                    figsize=BAR_PLOT_SIZE_ERROR_TEST_SET, facecolor='white', 
                    sharey=True, gridspec_kw={'wspace': 0})
                # iterate over labels:
                for i_, label_ in enumerate(RUN_LABELS):
                    err_ = test_error_dict[key_][dev_][label_]
                    pd_ = pd.DataFrame.from_dict(err_, orient='index').transpose()
                    # plot if not empty:
                    if len(pd_):
                        sns.boxplot(data=pd_, palette="Set3", ax=axes[i_])
                        axes[i_].set_title(f"{label_}")
                        # pe_pd.boxplot()
                file_name = AM.save_fig(fig, f"{dev_}_{key_}_boxplot", subdir=f"{test_set.__name__}")
    # break
    # break
# %% ---- Tabulate OVERALL ---- #
if FEATURE_GENERATE_SUMMARY:
    # tabluate result:
    for key_ in ERROR_KEYS:
        for label_ in RUN_LABELS:
            rmse_ = TABULAR_RESULT[key_][label_]
            pd_ = pd.DataFrame.from_dict(rmse_)
            print(f"Table {label_} @ {key_}")
            print(pd_)
            print("=====================================\n")
            pd_.to_csv(f"{AM._output_dir}/[overall]_{key_}_{label_}.csv", index = False)
# %% ---- PLOT OVERALL ---- #
if FEATURE_GENERATE_SUMMARY:
    # plot error bar:
    for key_ in ERROR_KEYS:
        for test_ in TARGET_EE_MOTIONS:
            print(f"Plotting {test_} @ {key_}")
            fig, axes = plt.subplots(nrows=1, ncols=2, 
                figsize=BAR_PLOT_SIZE_ERROR_SUMMARY, facecolor='white', 
                sharey=True, gridspec_kw={'wspace': 0})
            # iterate over labels:        
            for i_, label_ in enumerate(RUN_LABELS):
                err_ = TABULAR_PLOT_DATA[key_][label_][test_]
                pd_ = pd.DataFrame.from_dict(err_, orient='index').transpose()
                # plot if not empty:
                if len(pd_):
                    sns.boxplot(data=pd_, palette="Set3", ax=axes[i_])
                    axes[i_].set_title(f"{label_}")
                    # pe_pd.boxplot()
            if 'pe' in key_:
                btm_, top_ = axes[0].get_ylim()
                axes[0].set_ybound(max(btm_, 0), min(top_, 4))
                axes[0].set_ylabel("$\|\Delta P_{R^3}\|_2 \,[m]$")
            else:
                # axes[0].set_ybound(max(btm_, 0), min(top_, 1))
                axes[0].set_ylabel("$\|\Delta R_{SE(3)} \|_F$")
                
                
            # output:
            file_name = AM.save_fig(fig, f"overall_{key_}_{test_}_boxplot")

# %% -------------------------------- REPORT -------------------------------- %% #


