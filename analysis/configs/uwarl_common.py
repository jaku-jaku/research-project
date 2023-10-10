from uwarl_bag_utils.bag_parser import BagParser
### common ###
PARSER_TYPE_GROUP = {
    # 'accel'     : ['/cam_EE/accel/sample', '/cam_base/accel/sample'],
    # 'gyro'      : ['/cam_EE/gyro/sample', '/cam_base/gyro/sample'],
    # 'vicon'     : ['/vicon/cam_ee/cam_ee', '/vicon/wam_EE/wam_EE', '/vicon/summit_base/summit_base', '/vicon/wam_base/wam_base', '/vicon/wam_ee/wam_ee'],
    # 'system'    : ['/uwarl/robotnik_base_hw/voltage'],
    ### [Dual Vins-Mono] Topics:
    'vins-GT'   : ['/vins_estimator/base/vicon/path', '/vins_estimator/EE/vicon/path'],
    'vins-est'  : ['/vins_estimator/base/path', '/vins_estimator/EE/path'],
    'vins-loop' : ['/loop_fusion/base/pose_graph_path', '/loop_fusion/EE/pose_graph_path'],
}

PARSER_CALLBACKS ={
    # '/cam_EE/accel/sample'                   : lambda data,topic,msg: BagParser.parse_l515(data,topic,msg),
    # '/cam_EE/gyro/sample'                    : lambda data,topic,msg: BagParser.parse_l515(data,topic,msg),
    # '/cam_base/accel/sample'                 : lambda data,topic,msg: BagParser.parse_l515(data,topic,msg),
    # '/cam_base/gyro/sample'                  : lambda data,topic,msg: BagParser.parse_l515(data,topic,msg),
    # '/uwarl/cmd_vel'                         : lambda data,topic,msg: BagParser.parse_summit(data,topic,msg),
    # '/uwarl/joint_states'                    : lambda data,topic,msg: BagParser.parse_summit(data,topic,msg),
    # '/uwarl/mavros/imu/data'                 : lambda data,topic,msg: BagParser.parse_summit(data,topic,msg),
    # '/uwarl/mavros/imu/mag'                  : lambda data,topic,msg: BagParser.parse_summit(data,topic,msg),
    # '/uwarl/pad_teleop/cmd_vel'              : lambda data,topic,msg: BagParser.parse_summit(data,topic,msg),
    # '/uwarl/robotnik_base_control/cmd_vel'   : lambda data,topic,msg: BagParser.parse_summit(data,topic,msg),
    # '/uwarl/robotnik_base_control/odom'      : lambda data,topic,msg: BagParser.parse_summit(data,topic,msg),
    
    # '/vicon/cam_ee/cam_ee'                   : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    # '/vicon/markers'                         : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    # '/vicon/summit_base/summit_base'         : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    # '/vicon/wam_base/wam_base'               : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    # '/vicon/wam_ee/wam_ee'                   : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    # '/vicon/wam_EE/wam_EE'                   : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    
    # '/wam/fts/fts_states'                    : lambda data,topic,msg: BagParser.parse_wam(data,topic,msg),
    '/wam/joint_states'                      : lambda data,topic,msg: BagParser.parse_wam(data,topic,msg),
    # '/wam/move_is_done'                      : lambda data,topic,msg: BagParser.parse_wam(data,topic,msg),
    '/wam/pose'                              : lambda data,topic,msg: BagParser.parse_wam(data,topic,msg),
    
    # [VIO: Vins-Mono]:
    '/vins_estimator/base/vicon/path'      : lambda data,topic,msg: BagParser.parse_vio(data,topic,msg),
    '/vins_estimator/EE/vicon/path'        : lambda data,topic,msg: BagParser.parse_vio(data,topic,msg),
    
    '/vins_estimator/base/path'            : lambda data,topic,msg: BagParser.parse_vio(data,topic,msg),
    '/vins_estimator/EE/path'              : lambda data,topic,msg: BagParser.parse_vio(data,topic,msg),
    
    '/loop_fusion/base/pose_graph_path'    : lambda data,topic,msg: BagParser.parse_vio(data,topic,msg),
    '/loop_fusion/EE/pose_graph_path'      : lambda data,topic,msg: BagParser.parse_vio(data,topic,msg),
    
    # [SYSTEM: voltage]: to analyze the battery performance @ `waterloo_steel/waterloo_steel_demo/waterloo_steel_analyzer/jupyter/battery_test.ipynb`
    # '/uwarl/robotnik_base_hw/voltage' : lambda data,topic,msg: BagParser.parse_voltage(data,topic,msg),
    
    ### [UNUSED]:
    # /cam_EE/accel/imu_info
    # /cam_EE/color/camera_info
    # /cam_EE/color/image_raw
    # /cam_EE/color/metadata
    # /cam_EE/depth/camera_info
    # /cam_EE/depth/image_rect_raw
    # /cam_EE/depth/metadata
    # /cam_EE/extrinsics/depth_to_color
    # /cam_EE/gyro/imu_info
    # /cam_EE/gyro/metadata
    # /cam_EE/l500_depth_sensor/parameter_descriptions
    # /cam_EE/l500_depth_sensor/parameter_updates
    # /cam_EE/motion_module/parameter_descriptions
    # /cam_EE/motion_module/parameter_updates
    # /cam_EE/realsense2_camera_manager/bond
    # /cam_EE/rgb_camera/parameter_descriptions
    # /cam_EE/rgb_camera/parameter_updates
    # /cam_base/accel/imu_info
    # /cam_base/accel/metadata
    # /cam_base/accel/sample
    # /cam_base/color/camera_info
    # /cam_base/color/image_raw
    # /cam_base/color/metadata
    # /cam_base/depth/camera_info
    # /cam_base/depth/image_rect_raw
    # /cam_base/depth/metadata
    # /cam_base/extrinsics/depth_to_color
    # /cam_base/gyro/imu_info
    # /cam_base/gyro/metadata
    # /cam_base/gyro/sample
    # /cam_base/l500_depth_sensor/parameter_descriptions
    # /cam_base/l500_depth_sensor/parameter_updates
    # /cam_base/motion_module/parameter_descriptions
    # /cam_base/motion_module/parameter_updates
    # /cam_base/realsense2_camera_manager/bond
    # /cam_base/rgb_camera/parameter_descriptions
    # /cam_base/rgb_camera/parameter_updates
    # /clock
    # /diagnostics
    # /rosout
    # /rosout_agg
    # /tf
    # /tf_static
    # /uwarl/cmd_vel
    # /uwarl/joint_states
    # /uwarl/joy
    # /uwarl/mavlink/from
    # /uwarl/mavros/altitude
    # /uwarl/mavros/imu/data
    # /uwarl/mavros/imu/data_raw
    # /uwarl/mavros/imu/mag
    # /uwarl/mavros/imu/static_pressure
    # /uwarl/mavros/imu/temperature_imu
    # /uwarl/mavros/target_actuator_control
    # /uwarl/mavros/vfr_hud
    # /uwarl/mavros/wind_estimation
    # /uwarl/pad_teleop/cmd_vel
    # /uwarl/robotnik_base_control/cmd_vel
    # /uwarl/robotnik_base_control/odom
    # /uwarl/robotnik_base_hw/emergency_stop
    # /uwarl/robotnik_base_hw/io
    # /uwarl/robotnik_base_hw/state
    # /uwarl/robotnik_base_hw/status
    # /uwarl/robotnik_base_hw/voltage
    # /uwarl/scan
    # /uwarl/system_monitor/diagnostics
    # /uwarl/twist_marker
    # /uwarl/uwarl_front_laser_link_nodelet_manager/bond
    # /uwarl/uwarl_front_laser_link_nodelet_manager_cloud/parameter_descriptions
    # /uwarl/uwarl_front_laser_link_nodelet_manager_cloud/parameter_updates
    # /uwarl/uwarl_front_laser_link_nodelet_manager_driver/parameter_descriptions
    # /uwarl/uwarl_front_laser_link_nodelet_manager_driver/parameter_updates
    # /uwarl/uwarl_front_laser_link_nodelet_manager_laserscan/parameter_descriptions
    # /uwarl/uwarl_front_laser_link_nodelet_manager_laserscan/parameter_updates
    # /uwarl/velodyne_packets
    # /uwarl/velodyne_points
}
