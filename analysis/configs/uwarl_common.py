from uwarl_bag_utils.bag_parser import BagParser
### common ###
PARSER_TYPE_GROUP = {
    'accel'     : ['/cam_EE/accel/sample', '/cam_base/accel/sample'],
    'gyro'      : ['/cam_EE/gyro/sample', '/cam_base/gyro/sample'],
    'vicon'     : ['/vicon/cam_ee/cam_ee', '/vicon/wam_EE/wam_EE', '/vicon/summit_base/summit_base', '/vicon/wam_base/wam_base', '/vicon/wam_ee/wam_ee'],
    'vins-mono' : ['/vins_estimator/path', '/loop_fusion/pose_graph_path'],
    'system'    : ['/uwarl/robotnik_base_hw/voltage'],
}

PARSER_CALLBACKS ={

    # '/vicon/markers'                 
    # /vicon/summit_base/summit_base: geometry_msgs/TransformStamped
    '/vicon/summit_base/summit_base'         : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    # /vicon/wam_EE/wam_EE: geometry_msgs/TransformStamped
    '/vicon/wam_EE/wam_EE'                   : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    # /vicon/wam_base/wam_base: geometry_msgs/TransformStamped
    '/vicon/wam_base/wam_base'               : lambda data,topic,msg: BagParser.parse_vicon(data,topic,msg),
    
    # '/wam/fts/fts_states'                    : lambda data,topic,msg: BagParser.parse_wam(data,topic,msg),
    '/wam/joint_states'                      : lambda data,topic,msg: BagParser.parse_wam(data,topic,msg),
    # '/wam/move_is_done'                      : lambda data,topic,msg: BagParser.parse_wam(data,topic,msg),
    '/wam/pose'                              : lambda data,topic,msg: BagParser.parse_wam(data,topic,msg),
    
    # [VIO: Vins-Mono]:
    # /loop_fusion/base_path: nav_msgs/Path
    # /loop_fusion/camera_pose_visual: visualization_msgs/MarkerArray
    # /loop_fusion/margin_cloud_loop_rect: sensor_msgs/PointCloud
    # /loop_fusion/odometry_rect: nav_msgs/Odometry
    # /loop_fusion/path_1: nav_msgs/Path
    # /loop_fusion/point_cloud_loop_rect: sensor_msgs/PointCloud
    # /loop_fusion/pose_graph: visualization_msgs/MarkerArray
    # /loop_fusion/pose_graph_path: nav_msgs/Path
    '/loop_fusion/pose_graph_path'    : lambda data,topic,msg: BagParser.parse_vio(data,topic,msg),

    # /vins_estimator/camera_pose: nav_msgs/Odometry
    # /vins_estimator/camera_pose_visual: visualization_msgs/MarkerArray
    # /vins_estimator/extrinsic: nav_msgs/Odometry
    # /vins_estimator/imu_propagate: nav_msgs/Odometry
    # /vins_estimator/key_poses: visualization_msgs/Marker
    # /vins_estimator/keyframe_point: sensor_msgs/PointCloud
    # /vins_estimator/keyframe_pose: nav_msgs/Odometry
    # /vins_estimator/margin_cloud: sensor_msgs/PointCloud
    # /vins_estimator/odometry: nav_msgs/Odometry
    # /vins_estimator/path: nav_msgs/Path
    '/vins_estimator/path'            : lambda data,topic,msg: BagParser.parse_vio(data,topic,msg),
    # /vins_estimator/point_cloud: sensor_msgs/PointCloud
    
    # [SYSTEM: voltage]:
    # /uwarl/robotnik_base_hw/voltage: std_msgs/Float32
    '/uwarl/robotnik_base_hw/voltage' : lambda data,topic,msg: BagParser.parse_voltage(data,topic,msg),
    # /uwarl/joint_states: sensor_msgs/JointState
    # /uwarl/joy: sensor_msgs/Joy
    # /uwarl/mavros/imu/data: sensor_msgs/Imu
    # /uwarl/mavros/imu/mag: sensor_msgs/MagneticField
    # /uwarl/robotnik_base_control/cmd_vel: geometry_msgs/Twist
    # /uwarl/robotnik_base_control/odom: nav_msgs/Odometry
    # /uwarl/robotnik_base_hw/emergency_stop: std_msgs/Bool
    # /uwarl/robotnik_base_hw/io: robotnik_msgs/inputs_outputs
    # /uwarl/robotnik_base_hw/state: robotnik_msgs/State
    # /uwarl/robotnik_base_hw/status: robotnik_msgs/RobotnikMotorsStatus
    
    # '/uwarl/cmd_vel': 'geometry_msgs/Twist',
    # '/uwarl/joint_states': 'sensor_msgs/JointState',
    # '/uwarl/joy': 'sensor_msgs/Joy',
    # '/uwarl/mavros/imu/data': 'sensor_msgs/Imu',
    # '/uwarl/mavros/imu/mag': 'sensor_msgs/MagneticField',
    # '/uwarl/robotnik_base_control/cmd_vel': 'geometry_msgs/Twist',
    # '/uwarl/robotnik_base_control/odom': 'nav_msgs/Odometry',
    # '/uwarl/robotnik_base_hw/emergency_stop': 'std_msgs/Bool',
    # '/uwarl/robotnik_base_hw/io': 'robotnik_msgs/inputs_outputs',
    # '/uwarl/robotnik_base_hw/state': 'robotnik_msgs/State',
    # '/uwarl/robotnik_base_hw/status': 'robotnik_msgs/RobotnikMotorsStatus',
    # '/uwarl/robotnik_base_hw/voltage': 'std_msgs/Float32',
    
    # '/vicon/summit_base/summit_base': 'geometry_msgs/TransformStamped',
    # '/vicon/wam_EE/wam_EE': 'geometry_msgs/TransformStamped',
    # '/vicon/wam_base/wam_base': 'geometry_msgs/TransformStamped',
    
    # '/wam/fts/fts_states': 'geometry_msgs/Wrench',
    # '/wam/joint_states': 'sensor_msgs/JointState',
    # '/wam/move_is_done': 'std_msgs/Bool',
    # '/wam/pose': 'geometry_msgs/PoseStamped'}
    
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
