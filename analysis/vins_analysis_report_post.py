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

# 3rd party util
from icecream import ic

# %% 
# -------------------------------- Import Our Lib -------------------------------- %% #
# ours:
from vins_replay_utils.uwarl_reporter import ReportGenerator, AnalysisManager

# data labels:
from configs.uwarl_test_set_d455_Dec13_v2 import (
    TEST_SET_TITLE,
    DEMO_1213_A_STA,DEMO_1213_A_SPI,DEMO_1213_A_FWD,DEMO_1213_A_RVR,DEMO_1213_A_CIR,DEMO_1213_A_BEE,DEMO_1213_A_SQR_A,DEMO_1213_A_SQR_B,DEMO_1213_A_TRI,
)

# %% -------------------------------- Config -------------------------------- %% #
CONFIG_LOCAL_DIR = "/Users/jaku/Downloads/run_2023-12-20/[DEV]D455_v2"
ALL_TEST_SETS = [DEMO_1213_A_STA,DEMO_1213_A_SPI,DEMO_1213_A_FWD,DEMO_1213_A_RVR,DEMO_1213_A_CIR,DEMO_1213_A_BEE,DEMO_1213_A_SQR_A,DEMO_1213_A_SQR_B,DEMO_1213_A_TRI]
FIG_OUT_DIR = CONFIG_LOCAL_DIR # same as local

Q_CORR_W2C = np.array([[1,0,0],[0,0,1],[0,-1,0]])

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

# %% 2. gather pickles:
for test_set in ALL_TEST_SETS:
    TEST_SET_DIR = os.path.join(CONFIG_LOCAL_DIR, test_set.__name__)
    print(f"# Processing {test_set}@{TEST_SET_DIR}")
    for test in test_set.TEST_SET.value:
        TEST_TAG = test.name
        TEST_PICKLE = f"{TEST_TAG}_data_sets_3d"
        print(f"  > Indexing {test:8s}:{TEST_PICKLE}")
        
        ## load data:
        data_ = AM.load_dict_from_pickle(file_name=TEST_PICKLE,input_path=TEST_SET_DIR)
        ## create output folder:
        path_ = RG.create_subfolder(folder_name=f"{test_set.__name__}/{test}")
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
                data_sub['t0'] = t0_[0]
                data_sub['t'] = t_R1
                data_sub['p_x'] = y_R3[:,0]
                data_sub['p_y'] = y_R3[:,1]
                data_sub['p_z'] = y_R3[:,2]
                data_sub['q_x'] = r_R4[:,0]
                data_sub['q_y'] = r_R4[:,1]
                data_sub['q_z'] = r_R4[:,2]
                data_sub['q_w'] = r_R4[:,3]
            pd.DataFrame(data_sub).to_csv(file_name, index = False)
            print(f"       - {file_name}")
            
        ## time alignment:
        DEVICES     = ["Base", "EE"]
        RUN_LABELS  = ["baseline", "coupled (ours)"]
        # ic(data_.keys())
        for device in DEVICES:
            for label in RUN_LABELS:
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
                    
                    # Alignment details:
                    def _get_aligned_data(data_pred): # align time to estimation
                        is_valid_ = (bool)(len(data_pred['t0']) == 1 and data_pred['t0'][0] > 0)
                        if not is_valid_: 
                            return None
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
                    
                    # Apply alignment:
                    aligned_data_est  = _get_aligned_data(data_est)
                    aligned_data_loop = _get_aligned_data(data_loop)
                    
                    # save aligned data:
                    def parse_aligned_data(aligned_data):
                        if not aligned_data:
                            return None
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
                    
                    parsed_data_est  = parse_aligned_data(aligned_data_est)
                    parsed_data_loop = parse_aligned_data(aligned_data_loop)
                    
                    # save to csv:
                    pd.DataFrame(parsed_data_est ).to_csv(f"{path_}/[aligned] Est--vs-GT {device} ({label}).csv", index = False)
                    pd.DataFrame(parsed_data_loop).to_csv(f"{path_}/[aligned] Loop-vs-GT {device} ({label}).csv", index = False)
        
        ## process data:
        # ic(data_.keys())
        # ic(data_['Vicon Cam Base (coupled (ours))'].keys())
        # ic(np.shape(np.array(data_['Vicon Cam Base (coupled (ours))']['r'])))
    #     break
    # break

# %% -------------------------------- REPORT -------------------------------- %% #