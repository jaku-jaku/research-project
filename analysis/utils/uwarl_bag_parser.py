#! /usr/bin/env python
""" `bag_parser.py`

    This script will provide parsing support for custom messages.
    This work is based on the work of @sikang, see https://github.com/sikang/bag_plot
    
    @author: 
"""
#===================================#
#  I M P O R T - L I B R A R I E S  #
#===================================#
# python libraries:
from __future__ import division
from fnmatch import translate
from ntpath import join

import copy
import threading

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Callable, Optional
from enum import Enum

# python 3rd party:
import numpy as np
import rosbag
import rospy
import yaml

# import subprocess
from tf.transformations import euler_from_quaternion
from icecream import ic

# ours:

#=======================#
#  D E F I N I T I O N  #
#=======================#
class TYPES_VAR(str, Enum):
    VELOCITY_LINEAR    = 'v_XYZ'
    VELOCITY_ANGULAR   = 'v_RPY'
    POSITION_XYZ       = 'p_XYZ'
    ACCERLATION_XYZ    = 'a_XYZ'
    GYRO_XYZ           = 'g_XYZ'
    ORIENTATION_XYZW   = 'q_ABCD'
    MAGNETOMETER_XYZ   = 'm_XYZ'
    JOINT_POSITION     = 'j_pos'
    JOINT_VELOCITY     = 'j_vel'
    JOINT_EFFORT       = 'j_eff'
    FORCE_TORQUE       = 'FT'
    BOOLEAN_STATES     = 'bool'
    TIME_STAMP_SEC     = 't'
    VOLTAGE            = 'V'
    MARKER_ARRAY       = 'marker_array'
    

### class ###
class BagParser:
    #===============================#
    #  I N I T I A L I Z A T I O N  #
    #===============================#
    # placeholder for the bag payload:
    _topic_types_lut: Dict[str, str] = None,
    
    _bag_data: rosbag.Bag = None,
    _bag_data_lock: threading.RLock = None,
    _info_dict: Dict[str, str] = None,
    _all_processed_bag: Dict[str, Dict[str, List[Union[float, int, str]]]] = None,
    _bag_parser_reg_map: Dict[str, Callable] = None,
    _bag_file_binded: str = None,
    
    def __init__(self, parser_map):
        self._bag_data_lock = threading.RLock()
        self._bag_parser_reg_map = parser_map
        # init placeholder:
        self.unbind_bagfile()
        
    #==================================#
    #  P U B L I C    F U N C T I O N  #
    #==================================#
    def bind_bagfile(self, bagfile)->None:
        with self._bag_data_lock:
            self._bag_data = rosbag.Bag(bagfile, 'r')
            self._bag_file_binded = bagfile

    def unbind_bagfile(self)->None:
        with self._bag_data_lock:
            self._topic_types_lut = {} 
            self._bag_data = {}
            self._info_dict = {}
            self._all_processed_bag = {}
            self._bag_samples = {}
            self._bag_file_binded = None

    def load_bag_topics(self)->None:
        assert self._bag_data is not None, "Load Bag Data Before Processing!"
        with self._bag_data_lock:
            self._info_dict = yaml.load(self._bag_data._get_yaml_info())
            for x in self._info_dict['topics']:
                self._topic_types_lut[x['topic']] = x['type']
                self._bag_samples[x['topic']] = None

    def get_bag_msgs(self, topics):
        payload = {}
        if len(topics) > 0:
            with self._bag_data_lock:
                for topic, msg, ros_time in self._bag_data.read_messages():
                    # topic based parsing:
                    if topic in self._bag_parser_reg_map and topic in topics:
                        payload_ = self._bag_parser_reg_map[topic](payload, topic, msg)
                        payload.update(payload_)
        return payload
    
    def process_all_bag_msgs(self):
        with self._bag_data_lock:
            for topic, msg, ros_time in self._bag_data.read_messages():
                if self._bag_samples[topic] is None:
                    self._bag_samples[topic] = msg
                # topic based parsing:
                if topic in self._bag_parser_reg_map:
                    payload_ = self._bag_parser_reg_map[topic](self._all_processed_bag, topic, msg)
                    self._all_processed_bag.update(payload_)

    def get_bag_samples_safe(self):
        payload = {}
        with self._bag_data_lock:
            payload = copy.deepcopy(self._bag_samples)
        return payload

    def get_processed_bag_safe(self):
        payload = {}
        with self._bag_data_lock:
            payload = copy.deepcopy(self._all_processed_bag)
        return payload
    
    def get_bag_topics_lut_safe(self)->Dict[str, str]:
        payload = {}
        with self._bag_data_lock:
            payload = copy.deepcopy(self._topic_types_lut)
        return payload
    
    def get_bag_info_safe(self)->Dict[str, str]:
        payload = {}
        with self._bag_data_lock:
            payload = copy.deepcopy(self._info_dict)
        return payload
    #====================================#
    #  P R I V A T E    F U N C T I O N  #
    #====================================#
    @staticmethod
    def _init_topical_dict(payload, topic, params):
        payload[topic] = {}
        for param in params:
            payload[topic][param] = []
        return payload
            
    @staticmethod
    def _xyz_to_array(data):
        return [data.x, data.y, data.z]
    
    @staticmethod
    def _xyzw_to_array(data):
        return [data.x, data.y, data.z, data.w]

    @staticmethod
    def _parse_vel(payload, topic, msg):
        if topic not in payload:
            BagParser._init_topical_dict(payload, topic, [  TYPES_VAR.TIME_STAMP_SEC, 
                                                            TYPES_VAR.VELOCITY_LINEAR, 
                                                            TYPES_VAR.VELOCITY_ANGULAR      ])
        payload[topic][TYPES_VAR.TIME_STAMP_SEC].append(msg.header.stamp.to_sec())
        payload[topic][TYPES_VAR.VELOCITY_LINEAR].append(BagParser._xyz_to_array(msg.transform.linear))
        payload[topic][TYPES_VAR.VELOCITY_ANGULAR].append(BagParser._xyz_to_array(msg.transform.angular))
        return payload
    
    @staticmethod
    def _parse_pose(payload, topic, msg):
        if topic not in payload:
            BagParser._init_topical_dict(payload, topic, [  TYPES_VAR.TIME_STAMP_SEC, 
                                                            TYPES_VAR.POSITION_XYZ, 
                                                            TYPES_VAR.ORIENTATION_XYZW      ])
        payload[topic][TYPES_VAR.TIME_STAMP_SEC].append(msg.header.stamp.to_sec())
        payload[topic][TYPES_VAR.POSITION_XYZ].append(BagParser._xyz_to_array(msg.pose.position))
        payload[topic][TYPES_VAR.ORIENTATION_XYZW].append(BagParser._xyzw_to_array(msg.pose.orientation))
        return payload
    
    @staticmethod
    def _parse_poses_at_index(payload, topic, msg, seq_indices=[0, 100, 200, 300, -1], seq_sample_T=100):
        # overriding till last index:
        if -1 in seq_indices:
            BagParser._init_topical_dict(payload, topic, [  TYPES_VAR.TIME_STAMP_SEC, 
                                                            TYPES_VAR.POSITION_XYZ, 
                                                            TYPES_VAR.ORIENTATION_XYZW      ])
            for pose_msg in msg.poses:
                payload[topic][TYPES_VAR.TIME_STAMP_SEC].append(pose_msg.header.stamp.to_sec())
                payload[topic][TYPES_VAR.POSITION_XYZ].append(BagParser._xyz_to_array(pose_msg.pose.position))
                payload[topic][TYPES_VAR.ORIENTATION_XYZW].append(BagParser._xyzw_to_array(pose_msg.pose.orientation))
        # sampling:
        if msg.header.seq in seq_indices:
            topic_new = "{}@{}".format(topic, msg.header.seq)
            BagParser._init_topical_dict(payload, topic_new, [  TYPES_VAR.TIME_STAMP_SEC, 
                                                                TYPES_VAR.POSITION_XYZ, 
                                                                TYPES_VAR.ORIENTATION_XYZW      ])
            for pose_msg in msg.poses:
                payload[topic_new][TYPES_VAR.TIME_STAMP_SEC].append(pose_msg.header.stamp.to_sec())
                payload[topic_new][TYPES_VAR.POSITION_XYZ].append(BagParser._xyz_to_array(pose_msg.pose.position))
                payload[topic_new][TYPES_VAR.ORIENTATION_XYZW].append(BagParser._xyzw_to_array(pose_msg.pose.orientation))
        
            # print("Parsed {} poses at index {}.".format(len(msg.poses), seq_index))
            # ic(payload[topic][TYPES_VAR.TIME_STAMP_SEC])
        return payload
    
    @staticmethod
    def _parse_transformation(payload, topic, msg):
        if topic not in payload:
            BagParser._init_topical_dict(payload, topic, [  TYPES_VAR.TIME_STAMP_SEC, 
                                                            TYPES_VAR.POSITION_XYZ, 
                                                            TYPES_VAR.ORIENTATION_XYZW      ])
        payload[topic][TYPES_VAR.TIME_STAMP_SEC].append(msg.header.stamp.to_sec())
        payload[topic][TYPES_VAR.POSITION_XYZ].append(BagParser._xyz_to_array(msg.transform.translation))
        payload[topic][TYPES_VAR.ORIENTATION_XYZW].append(BagParser._xyzw_to_array(msg.transform.rotation))
        return payload
    
    @staticmethod
    def _parse_imu(payload, topic, msg, tags):
        if topic not in payload:
            BagParser._init_topical_dict(payload, topic, [  TYPES_VAR.TIME_STAMP_SEC,
                                                            TYPES_VAR.ACCERLATION_XYZ, 
                                                            TYPES_VAR.GYRO_XYZ, 
                                                            TYPES_VAR.ORIENTATION_XYZW, 
                                                            TYPES_VAR.MAGNETOMETER_XYZ      ])
        payload[topic][TYPES_VAR.TIME_STAMP_SEC].append(msg.header.stamp.to_sec())
        if 'accel' in tags:
            payload[topic][TYPES_VAR.ACCERLATION_XYZ].append(BagParser._xyz_to_array(msg.linear_acceleration))
        if 'gyro' in tags:
            payload[topic][TYPES_VAR.GYRO_XYZ].append(BagParser._xyz_to_array(msg.angular_velocity))
        if 'orie' in tags:
            payload[topic][TYPES_VAR.TYPES_VAR.ORIENTATION_XYZW].append(BagParser._xyzw_to_array(msg.orientation))
        if 'mag' in tags:
            payload[topic][TYPES_VAR.MAGNETOMETER_XYZ].append(BagParser._xyz_to_array(msg.magnetic_field))
        else:
            rospy.logwarn("[!] unknown imu messages [{}]".format(topic))
        return payload
    
    @staticmethod
    def _parse_joint_states(payload, topic, msg):
        if topic not in payload:
            BagParser._init_topical_dict(payload, topic, [  TYPES_VAR.TIME_STAMP_SEC,
                                                            TYPES_VAR.TIME_STAMP_SEC,
                                                            TYPES_VAR.JOINT_POSITION,
                                                            TYPES_VAR.JOINT_VELOCITY,
                                                            TYPES_VAR.JOINT_EFFORT     ])
        #data
        payload[topic][TYPES_VAR.TIME_STAMP_SEC].append(msg.header.stamp.to_sec())
        payload[topic][TYPES_VAR.JOINT_POSITION].append(msg.position)
        payload[topic][TYPES_VAR.JOINT_VELOCITY].append(msg.velocity)
        payload[topic][TYPES_VAR.JOINT_EFFORT  ].append(msg.effort)
        return payload
    
    @staticmethod
    def _parse_force_torque(payload, topic, msg):
        if topic not in payload:
            BagParser._init_topical_dict(payload, topic, [TYPES_VAR.FORCE_TORQUE])
        # data:
        payload[topic][TYPES_VAR.FORCE_TORQUE].append(
            np.array([BagParser._xyz_to_array(msg.force), BagParser._xyz_to_array(msg.torque)]))
        return payload
    
    @staticmethod
    def _parse_boolean_states(payload, topic, msg):
        if topic not in payload:
            BagParser._init_topical_dict(payload, topic, [   TYPES_VAR.BOOLEAN_STATES   ])
        # data:
        payload[topic][TYPES_VAR.BOOLEAN_STATES].append(msg.data)
        return payload

    #=================================================#
    #  P U B L I C    S T A T I C    F U N C T I O N  #
    #=================================================#
    @staticmethod
    def parse_voltage(payload, topic, msg):
        if topic not in payload:
            BagParser._init_topical_dict(payload, topic, [   TYPES_VAR.VOLTAGE   ])
        # data:
        payload[topic][TYPES_VAR.VOLTAGE].append(msg.data)
        return payload
        
    @staticmethod
    def parse_l515(payload, topic, msg, node_name):
        tags = []
        tags = ['accel'] if 'accel/sample' in topic else tags
        tags = ['gyro'] if 'gyro/sample' in topic else tags
        rectify_topic = f'/{node_name}/imu'
        payload.update(BagParser._parse_imu(payload, rectify_topic, msg, tags))
        return payload
        
    @staticmethod
    def parse_summit(payload, topic, msg):
        if topic == '/uwarl/joint_states':
            payload.update(BagParser._parse_joint_states(payload, f'/summit/joint_states', msg))
            # ---
            #     header: 
            #     seq: 518575
            #     stamp: 
            #         secs: 1672867347
            #         nsecs: 921571138
            #     frame_id: ''
            #     name: 
            #     - back_left_wheel_joint
            #     - back_right_wheel_joint
            #     - front_left_wheel_joint
            #     - front_right_wheel_joint
            #     position: [-87.0231023598725, 484.44130971778867, -72.59182188054238, 496.4018721672009]
            #     velocity: [0.4462175863091867, -0.619777692265965, 0.024557796087902966, -0.37186369779270734]
            #     effort: [0.69921875, 1.060546875, 2.1220703125, 1.0458984375]
            # ---
            pass
        elif topic == '/uwarl/mavros/imu/payload':
            payload.update(BagParser._parse_imu(payload, f'/summit/imu', msg, ['accel', 'gyro', 'orie']))
            # ---
            #     header: 
            #       seq: 259328
            #       stamp: 
            #         secs: 1672867348
            #         nsecs: 526021887
            #       frame_id: "fcu"
            #     orientation: 
            #       x: -0.8879434824002388
            #       y: 0.45985819495617924
            #       z: -0.008544388781037316
            #       w: -0.0037254386359466536
            #     orientation_covariance: [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
            #     angular_velocity: 
            #       x: 0.0006416797987185419
            #       y: 0.003224233631044626
            #       z: -0.0023241967428475623
            #     angular_velocity_covariance: [1.2184696791468346e-07, 0.0, 0.0, 0.0, 1.2184696791468346e-07, 0.0, 0.0, 0.0, 1.2184696791468346e-07]
            #     linear_acceleration: 
            #       x: 0.2887013256549835
            #       y: 0.04129822552204009
            #       z: -10.02697467803955
            #     linear_acceleration_covariance: [8.999999999999999e-08, 0.0, 0.0, 0.0, 8.999999999999999e-08, 0.0, 0.0, 0.0, 8.999999999999999e-08]
            # ---
            pass
        elif topic == '/uwarl/mavros/imu/mag':
            payload.update(BagParser._parse_imu(payload, f'/summit/imu', msg, ['mag']))
            # ---
            #     header: 
            #     seq: 259357
            #     stamp: 
            #         secs: 1672867349
            #         nsecs: 122228014
            #     frame_id: "fcu"
            #     magnetic_field: 
            #     x: -3.6914563179016117e-05
            #     y: -1.4663988351821905e-05
            #     z: -3.579270243644714e-05
            #     magnetic_field_covariance: [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            # ---
            pass
        elif topic ==  '/uwarl/robonik_base_control/odom':
            payload.update(BagParser._parse_pose(payload, f'/summit/pose', msg.pose.pose))
            payload.update(BagParser._parse_vel(payload, f'/summit/twsit', msg.twist.twist))
            # ---
            #     header: 
            #     seq: 388810
            #     stamp: 
            #         secs: 1672867352
            #         nsecs: 281897764
            #     frame_id: "uwarl_odom"
            #     child_frame_id: "uwarl_base_footprint"
            #     pose: 
            #     pose: 
            #         position: 
            #         x: -1.0668697062835941
            #         y: -0.002397378800019931
            #         z: 0.0
            #         orientation: 
            #         x: 0.0
            #         y: -0.0
            #         z: -0.896164425263616
            #         w: -0.4437221235096723
            #     covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            #     twist: 
            #     twist: 
            #         linear: 
            #         x: 0.014454459044454693
            #         y: 0.0
            #         z: 0.0
            #         angular: 
            #         x: 0.0
            #         y: 0.0
            #         z: 0.9287372324913243
            #     covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            # ---
            pass
        return payload
    
    @staticmethod
    def parse_vio(payload, topic, msg):
        if topic in [
            '/vins_estimator/path',
            '/loop_fusion/pose_graph_path', 
        ]:
            data = BagParser._parse_poses_at_index(payload, topic, msg)
            payload.update(data)
            pass
        else:
            rospy.logwarn('Topic {} not implemented'.format(topic))
            payload[topic] = {}
        return payload
    
    @staticmethod
    def parse_vicon(payload, topic, msg):
        if topic in [
            '/vicon/cam_ee/cam_ee',
            '/vicon/summit_base/summit_base', 
            '/vicon/wam_base/wam_base',
            '/vicon/wam_ee/wam_ee',
            '/vicon/wam_EE/wam_EE',
        ]:
            data = BagParser._parse_transformation(payload, topic, msg)
            payload.update(data)
            # ---
            #     header: 
            #     seq: 241609
            #     stamp: 
            #         secs: 1672867352
            #         nsecs: 989432805
            #     frame_id: "/vicon/world"
            #     child_frame_id: "vicon/cam_ee/cam_ee"
            #     transform: 
            #     translation: 
            #         x: -0.1872015708455022
            #         y: 0.9491721395971313
            #         z: 1.668968041592301
            #     rotation: 
            #         x: -0.4179218927397328
            #         y: 0.9000888916852219
            #         z: 0.07114474444668589
            #         w: -0.10059673936725771
            # ---
            pass
        else:
            rospy.logwarn('Topic {} not implemented'.format(topic))
            payload[topic] = {}
        return payload

    @staticmethod
    def parse_wam(payload, topic, msg):
        if topic ==  '/wam/fts/fts_states':
            payload.update(BagParser._parse_force_torque(payload, '/wam/fts', msg))
            # ---
            #     force: 
            #     x: 1.69921875
            #     y: 1.671875
            #     z: 1.76171875
            #     torque: 
            #     x: -0.11572265625
            #     y: 0.09130859375
            #     z: 0.04150390625
            # ---
            pass
        elif topic ==  '/wam/joint_states':
            payload.update(BagParser._parse_joint_states(payload, topic, msg))
            # ---
            #     header: 
            #     seq: 398997
            #     stamp: 
            #         secs: 1672867354
            #         nsecs: 239842059
            #     frame_id: ''
            #     name: 
            #     - wam_j1
            #     - wam_j2
            #     - wam_j3
            #     - wam_j4
            #     - wam_j5
            #     - wam_j6
            #     - wam_j7
            #     position: [0.0017531209004407325, 0.0, 0.0012771390104605262, -0.0015339807878856412, 0.002134921715098573, 0.014786309656423451, 1.5015134115311966]
            #     velocity: [0.0, 0.013568267087021354, -0.022794656430576182, 0.0, -0.03951582940292288, -0.03951582940292288, 0.05134675756305247]
            #     effort: [-1.939468227331002, -0.4586723801864262, -0.14020420718877055, 2.04306090814097, 0.059240260072469034, -0.12673082653694392, 0.003749381320776319]
            # ---
            pass
        
        elif topic ==  '/wam/move_is_done':
            payload.update(BagParser._parse_boolean_states(payload, topic, msg))
            # ---
            #     data: True
            # ---
            pass
        elif topic ==  '/wam/pose':
            payload.update(BagParser._parse_pose(payload, topic, msg))
            # ---
            #     header: 
            #     seq: 399348
            #     stamp: 
            #         secs: 1672867354
            #         nsecs: 941975025
            #     frame_id: ''
            #     pose: 
            #     position: 
            #         x: 0.00036680640533616243
            #         y: 3.04728118423608e-06
            #         z: 0.91082532424474
            #     orientation: 
            #         x: -0.0044890555263752295
            #         y: -0.004838436306216975
            #         z: -0.684113043702621
            #         w: 0.7293461327453018
            # ---
            pass
        else:
            rospy.logwarn('Topic {} not implemented'.format(topic))
        
        return payload 
    
