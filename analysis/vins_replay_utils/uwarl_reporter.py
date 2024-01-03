import yaml
import matplotlib.pyplot as plt

from utils.uwarl_util import create_all_folders
from typing import Dict, List, Tuple, Union, Callable, Optional

from icecream import ic
from datetime import datetime
import pickle
import os

DEFAULT_FIGSIZE = (5, 5)
class ReportGenerator:
    _generated_figs_name:dict()={}
    _tag:str=""
    _output_dir=None
    _table_of_var:dict()={}
    
    def __init__(self, title, tag):
        self._tag = tag
        self._title = title
        self._table_of_var = {"mu":{}, "std":{}}
    
    def bind_output_dir(self, output_dir):
        self._output_dir = output_dir
        
    def append_figname(self, case, key, file_name):
        file_dir_, file_name_ = os.path.split(file_name) 
        if self._output_dir:
            self.bind_output_dir(file_dir_)
        if case in self._generated_figs_name:
            self._generated_figs_name[case][key] = file_name_
        else: # init entries:
            self._generated_figs_name[case] = {key: file_name_}

    def append_variance(self, case, title, mu, std):
        if mu and std:
            for entry in mu:
                token = f"{title} - {entry}"
                if token not in self._table_of_var["mu"]:
                    self._table_of_var["mu"][token] = {}
                    self._table_of_var["std"][token] = {}
                
                self._table_of_var["mu"][token][case] = mu[entry] if mu else "N/A"
                self._table_of_var["std"][token][case] = std[entry] if std else "N/A"
        else:
            print(">>> Not valid mu and std!")
            
    def save_report_as_md(self):
        date_time_stub_hourly = datetime.now().strftime("%H")
        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_path=self._output_dir
        if output_path:
            file_name=f"{output_path}/APPENDIX_{self._tag.replace(' ', '_')}_[{date_time_stub_hourly}].md"
            print(f">>> Generating report as markdown ... @ {file_name}")
            with open(file_name, "w") as f:
                f.write(f"# Report {self._title} \n**[Auto-gen on {date_time}]** \n")
                for ver in self._table_of_var:
                    f.write(f"## Entry: {ver}\n")
                    ic(self._table_of_var[ver])
                    for i_, token in enumerate(self._table_of_var[ver]):
                        if i_ == 0:
                            f.write("|   "+"|{}|\n".format(" |".join(self._table_of_var[ver][token].keys())))
                            f.write("|---"+"|{}|\n".format(" |".join(["---" for i in range(len(self._table_of_var[ver][token]))])))
                        f.write("|{} |{}|\n".format(token, " | ".join([f"{val:.3f}" for val in self._table_of_var[ver][token].values()])))
                    f.write("\n")
                f.write("\n---\n")
                
            with open(file_name, "a") as f:
                for section, fig_names in self._generated_figs_name.items():
                    f.write(f"## Base Motion: {section} \n")
                    N_len = len(fig_names)
                    ic(fig_names)
                    f.write("|{}|\n".format(" | ".join(fig_names.keys())))
                    f.write("|{}|\n".format("|".join(["---" for i in range(N_len)])))
                    f.write("|{}|\n".format(" | ".join(["![{0}]({0})".format(val) for val in fig_names.values()])))
                    f.write("\n\n")
            print(f"[x]---> md report generated @ {file_name}")
        else:
            print(">>> No output path specified! HINT: please bind with `bind_output_dir`")
    
    def create_subfolder(self, folder_name):
        path = f"{self._output_dir}/{folder_name}"
        create_all_folders(path)
        return path
        
    # def append_errors(self, error_list):
        
            
class AnalysisManager:
    """ Analysis Manager 
        - handle global settings and keep consistency
        - manage output folder
    """
    _auto_save  :bool 
    _auto_close :bool 
    _verbose    :bool 
    _output_dir :str 
    _prefix     :str 
    
    def __init__(self, 
            output_dir: str="", 
            run_name: str="vins_analysis", 
            test_set_name: str="default",
            prefix: str="",
            auto_save: bool=True,
            auto_close: bool=False,
            verbose: bool = False,
        ):
        self._auto_close = auto_close
        self._auto_save = auto_save
        self._prefix = prefix
        self._verbose = verbose
        # create output folder
        self._create_dir(output_dir, run_name, test_set_name)
    
    def _create_dir(self, output_dir: str, run_name: str, test_set_name):
        self._output_dir = f"{output_dir}/{run_name}/{test_set_name}"
        create_all_folders(self._output_dir)

    def save_fig(self, fig, tag, title=None, dpi=600, subdir=None):
        if fig is None:
            return None
        file_name = None
        if title:
            plt.title(title)
        if self._auto_save:
            output_path=self._output_dir
            if subdir:
                output_path = f"{output_path}/{subdir}"
            file_name=f"{output_path}/plot_{tag.replace(' ', '_')}.png"
            fig.savefig(file_name, bbox_inches = 'tight', dpi=dpi)
            if self._verbose:
                print(f"Saved figure to {file_name}")
        if self._auto_close:
            plt.show(block=False)
            plt.close(fig)
        else:
            plt.show(block=True)
        return file_name
    
    def save_dict(self, data, file_name):
        output_path=self._output_dir
        with open(f"{output_path}{file_name}.yaml", "w") as f:
            yaml.dump(data, f)
    
    def load_dict(self, data, file_name):
        data = {}
        output_path=self._output_dir
        with open(f"{output_path}{file_name}.yaml", "r") as f:
            data = yaml.load(f)
        return data

    def save_dict_as_pickle(self, data, file_name="data", output_path=None):
        if output_path is None:
            output_path = self._output_dir
        with open(f"{output_path}{file_name}.pickle", "wb") as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load_dict_from_pickle(self, file_name="data", input_path=None):
        data = {}
        if input_path is None:
            input_path = self._output_dir
        else:
            input_path = f"{input_path}/"
        with open(f"{input_path}{file_name}.pickle", "rb") as f:
            data = pickle.load(f)
        return data

    def output_path(self):
        return self._output_dir