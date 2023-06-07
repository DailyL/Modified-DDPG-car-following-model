execute_process(COMMAND "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ackermann_control/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ackermann_control/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
