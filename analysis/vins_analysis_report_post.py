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
# %% -------------------------------- REPORT -------------------------------- %% #
# 0. init report generator:
date = datetime.now().strftime("%Y-%m-%d")
RG = ReportGenerator("Summary (post-run)", f"run_{date}")
AM = AnalysisManager(
    output_dir=FIG_OUT_DIR,
    run_name=f"SUMMARY_(post-run)", 
    test_set_name=f"run_{date}",
    prefix=TEST_SET_TITLE, # Unused
    auto_save=True,
    auto_close=True,
)
RG.bind_output_dir(AM._output_dir)

# %% 2. gather pickles:
