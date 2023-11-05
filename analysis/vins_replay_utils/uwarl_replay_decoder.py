from typing import Dict, List, Tuple, Union, Callable, Optional
from datetime import datetime
import json

from utils.uwarl_bag_parser import BagParser
from icecream import ic # DEBUG ONLY

def decode_replayed_vins_bag_file_name(_bag_path:str):
    prefix = _bag_path.split("_vins-replay")[0]
    unique_id, demo_id = prefix.split("_")
    tag, session_id, run_id = unique_id.split("-")
    _, demo_id_int = demo_id.split("-")
    description = {
        "cam-session-run": unique_id,
        "tag": tag,
        "session_id": session_id,
        "dt": "NA",
        "demo": demo_id_int,
        "run_id": run_id,
    }
    return description

def auto_generate_labels_from_bag_file_name_with_json_config(
    list_of_bag_path:List[str], json_map_file_name: str
):
    # TODO: this is not scalable, depending on the demo code
    # auto generate labels based on demo id
    dict_map = {}
    with open(f"{json_map_file_name}", "r") as data:
        dict_map = json.load(data)
    # ic(dict_map, list_of_bag_path)
    _bag_dict = dict()
    for path in list_of_bag_path:
        description = decode_replayed_vins_bag_file_name(path)
        demo = dict_map[description["demo"]]
        tag = description["tag"]
        session_id = description["session_id"]
        run_id = description["run_id"]
        bag_label = f"{tag}-{demo}-s{session_id}-i{run_id}"
        _bag_dict[bag_label] = path
    return _bag_dict

def auto_generate_labels_from_bag_file_name(
    list_of_bag_path:List[str], 
):
    # TODO: this is not scalable, depending on the demo code
    # auto generate labels based on demo id
    id_list = ["NULL"]
    for konfig_base in ["FIX", "SPI", "FWD", "RVR", "CIR", "88"]:
        for kongig_arm in ["Ext-F", "Pt-F", "Pt-U", "Pt-D", "Pt-LR", "Pt-UD"]:
            id_list.append(f"{konfig_base}-{kongig_arm}")
        
    _bag_dict = dict()
    for path in list_of_bag_path:
        description = decode_replayed_vins_bag_file_name(path)
        demo = id_list[int(description["demo"])]
        tag = description["tag"]
        session_id = description["session_id"]
        run_id = description["run_id"]
        bag_label = f"{tag}-{demo}-s{session_id}-i{run_id}"
        _bag_dict[bag_label] = path
    return _bag_dict

# Processed Data Object Placeholder
class ProcessedData:
    """ Placeholder for processed data
        - bag files will be loaded with BagParser and processed in batch
        - processed data will be cached in this class
    """
    _bag_path: str=""
    bag_info: Dict[str, Union[str, float]]
    bag_topics: Dict[str, List[str]]
    bag_data: Dict[str, Union[str, float]]
    bag_samples: Dict[str, Union[str, float]]
    T0: float = 0.0
    T1: float = 0.0
    dT: float = 0.0
    description: Dict[str, Union[str, float]]
    bag_exist:bool = False

    def __init__(self, BP:BagParser, directory, bag_path, T_LAST_S=-1):
        self._reset_cache()
        self._bag_path = bag_path
        # load bag file:
        BP.bind_bagfile(bagfile=f"{directory}/{bag_path}")
        BP.load_bag_topics()
        self.bag_info = BP.get_bag_info_safe()
        self.bag_topics = BP.get_bag_topics_lut_safe()
        if T_LAST_S > 0:
            self.bag_exist = BP.process_only_last_bag_msgs(T_SPAN_SECONDS=T_LAST_S) # TODO: very time consuming!!
        else:    
            BP.process_all_bag_msgs() # TODO: very time consuming!!

        if self.bag_exist:
            self.bag_data = BP.get_processed_bag_safe()
            self.bag_samples = BP.get_bag_samples_safe()
            # self._bag = BP._bag_data # DEBUG: debug purpose
            # unbind toolchain
            BP.unbind_bagfile()
            self._init_process()
    
    def _reset_cache(self):
        self.bag_info = dict()
        self.bag_topics = dict()
        self.bag_data = dict()
        self.bag_samples = dict()
        self.description = dict()
        self.T0 = 0.0
        self.T1 = 0.0
        self.dT = 0.0
        self._bag_path = ""

    def _init_process(self):
        self.T0=datetime.fromtimestamp(self.bag_info["start"])
        self.T1=datetime.fromtimestamp(self.bag_info["end"])
        self.dT = (self.T1 - self.T0).total_seconds()
        self.description = decode_replayed_vins_bag_file_name(self._bag_path)
        ic(self.description)
