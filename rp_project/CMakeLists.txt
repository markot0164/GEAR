cmake_minimum_required(VERSION 3.0.2)
project(rp_project)

## finding macro and catkin libraries
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  visualization_msgs
  message_generation
)

## message when the robot collide with the camera field of view
add_message_files(
  FILES
  Collision.msg
)

## adding service that reset the robot position and the service that check if the robot reach the goal
add_service_files(
  FILES
  ResetPosition.srv
  CheckGoal.srv
)

## Generate massage and services
generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

## catkin configuration
catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs geometry_msgs visualization_msgs
)

## Installing Python scripts
catkin_install_python(PROGRAMS
  scripts/sphere_control_node.py
  scripts/rviz_map.py
  scripts/keyboard_controller.py
  scripts/camera_detection.py
  scripts/reset_position.py
  scripts/check_goal.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

## Installing the rviz map
install(PROGRAMS
  scripts/rviz_map.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

install(DIRECTORY meshes/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/meshes
)