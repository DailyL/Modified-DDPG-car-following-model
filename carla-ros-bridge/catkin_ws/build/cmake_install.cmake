# Install script for directory: /home/dianzhaoli/carla-ros-bridge/catkin_ws/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/_setup_util.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install" TYPE PROGRAM FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/_setup_util.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/env.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install" TYPE PROGRAM FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/env.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/setup.bash;/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/local_setup.bash")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install" TYPE FILE FILES
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/setup.bash"
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/local_setup.bash"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/setup.sh;/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/local_setup.sh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install" TYPE FILE FILES
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/setup.sh"
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/local_setup.sh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/setup.zsh;/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/local_setup.zsh")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install" TYPE FILE FILES
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/setup.zsh"
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/local_setup.zsh"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install/.rosinstall")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/dianzhaoli/carla-ros-bridge/catkin_ws/install" TYPE FILE FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/catkin_generated/installspace/.rosinstall")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/gtest/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ad_demo/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_common/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_msgs/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ackermann_msgs/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ros_scenario_runner_types/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_waypoint_types/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/ros_compatibility/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ackermann_control/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ad_agent/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_manual_control/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ros_bridge/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ros_scenario_runner/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_spawn_objects/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_twist_to_control/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_walker_agent/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_waypoint_publisher/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/rqt_carla_control/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/bc_with_napoli/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/clone_follower/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/off_policy_ddpg/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/rl_agent/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/rl_agent_per/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/rl_carla/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/td3_agent/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/pcl_recorder/cmake_install.cmake")
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/rviz_carla_plugin/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
