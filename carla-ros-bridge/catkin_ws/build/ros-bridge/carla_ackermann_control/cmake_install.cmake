# Install script for directory: /home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ackermann_control

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
  include("/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ackermann_control/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/carla_ackermann_control" TYPE FILE FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/devel/include/carla_ackermann_control/EgoVehicleControlParameterConfig.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/dianzhaoli/carla-ros-bridge/catkin_ws/devel/lib/python3/dist-packages/carla_ackermann_control/cfg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages/carla_ackermann_control" TYPE DIRECTORY FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/devel/lib/python3/dist-packages/carla_ackermann_control/cfg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ackermann_control/catkin_generated/installspace/carla_ackermann_control.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_ackermann_control/cmake" TYPE FILE FILES
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ackermann_control/catkin_generated/installspace/carla_ackermann_controlConfig.cmake"
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/build/ros-bridge/carla_ackermann_control/catkin_generated/installspace/carla_ackermann_controlConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_ackermann_control" TYPE FILE FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ackermann_control/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/carla_ackermann_control" TYPE PROGRAM FILES
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ackermann_control/src/carla_ackermann_control/carla_ackermann_control_node.py"
    "/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ackermann_control/src/carla_ackermann_control/carla_control_physics.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_ackermann_control/launch" TYPE DIRECTORY FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ackermann_control/launch/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/carla_ackermann_control/config" TYPE DIRECTORY FILES "/home/dianzhaoli/carla-ros-bridge/catkin_ws/src/ros-bridge/carla_ackermann_control/config/")
endif()

