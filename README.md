# nexgrc_experimental
NexGRC Experimental

nexgrc_clinet node provide ros service to talk with socket (and send command to GRC Controller)
```
nexgrc_clien/StringCommand
string command
string parameters
---
int32 error_code
string response
```

## How to Build [Indigo]:
Go to your ROS workspace directory, then
``` bash
# remove old compiled file (if exist) and rebuild
catkin clean
catkin build
source devel/setup.bash
```

## Usage:
### Run with real Robot arm:
Currently, Only use `StringCommand` to communicate with GRC controller through tcpip.
``` bash
# After build, run the following command
roslaunch nexgrc_client start.launch
# Then, client node will wait for connecting NexGRC controller

# run with rviz (will need to specified urdf file)
roslaunch nexgrc_client start_rviz_demo.launch model:=`rospack find pmc6r_support`/urdf/pmc6r.urdf.xacro gui:=true
```

For testing, open another terminal
``` bash
# Go to you ROS worksace, and source nexgrc_client package
source devel/setup.bash
# ask robot to do ptp move.
rosservice call /grc_telnet 'ptp' ' -35 130 -15 45 90 -115'
# get joint position
rosservice call /grc_telnet 'get joint position' ''
# get flange frame
rosservice call /grc_telnet 'get flange frame' ''
# check if motion finish
rosservice call /grc_telnet 'get state' ''
# ask robot to stop while executing ptp command
rosservice call /grc_telnet 'halt' ''
```

### Work with Gazebo and control with ros_control
Run the following command in order.
``` bash
# To display in Gazebo Simulation.
roslaunch pmc6r_gazebo pmc6r_world.launch
# Connect with ros control
roslaunch pmc6r_control pmc6r_control.launch
# a function publish joint control message
rosrun pmc6r_control simple_mover
```

Note: In GRC Controller socket server part
You need to set Inbouad rule of port (1688) for tcp connection (Windows Firewall --> Advanced Setting)

