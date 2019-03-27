#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2019 NexCOBOT Inc.
# Author: Robin Chen
#
# TODO: Add Licensed before release
#
# -----------------------------------------------------------------------------
# This node manages the joint_path_command interface defined in
# http://wiki.ros.org/Industrial/Industrial_Robot_Driver_Spec
# -----------------------------------------------------------------------------

import rospy
import thread
import math

from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from nexgrc_client.srv import *

# User editable configuration
conf_rate                   = 100 # Hz
conf_com_node               = 'grc_telnet'
conf_joints_topic           = 'joint_states'
conf_base_name              = 'base_link'
conf_node_name              = 'grc_driver'
conf_trajectory_path_name   = 'joint_path_command'

# ---------------------------------------------------------------------------------------
# Robot specs
# ---------------------------------------------------------------------------------------
conf_joint_names  = ['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6']
conf_link_names  = ['link_1','link_2','link_3','link_4','link_5','link_6']
conf_max_speed    = [1.71042267, 1.74532925, 2.26892803, 2.44346095, 3.14159265, 3.14159265] # rad / s joint_0..joint_1


# ---------------------------------------------------------------------------------------
# Shared variables
# ---------------------------------------------------------------------------------------
lock = thread.allocate_lock()
lockCom = thread.allocate_lock()
current_joints    	= []
trajectory_points 	= [] # Stores the current trajectory
trajectory_active 	= None # Stores the current active position
trajectory_start  	= None # Stores start time, intialized after init node

def joint_states_publisher(rate):
    global conf_base_name
    global current_joints

    com = rospy.ServiceProxy(conf_com_node, StringCommand, persistent=True) # Communication with the commander service
    # communication must be persistent in order to keep the rate stable

    publisher_joints = rospy.Publisher(conf_joints_topic, JointState, queue_size=conf_rate) # Joint State publisher

    sleeper = rospy.Rate(rate)

    while not rospy.is_shutdown():
        now = rospy.Time.now()

        joint_state_msg = JointState()
        joint_state_msg.header.stamp = now
        joint_state_msg.header.frame_id = conf_base_name

        with lockCom:
            strJoints = com('get joint position', '').response

        joint_state_msg.name = conf_joint_names #conf_link_names

        # -----------------------------------------------------------
        # Critical Section - Always for accesing shared variables (both write an read)
        # -----------------------------------------------------------
        with lock:
            # Update variables
            current_joints = [math.pi*float(i)/180.0 for i in strJoints.split()]
            # Fill joint states
            joint_state_msg.position = current_joints[:6]
        # -----------------------------------------------------------

        publisher_joints.publish(joint_state_msg)
        sleeper.sleep()


def move_manager(rate):
    pass

# ---------------------------------------------------------------------------------------
# Subscription to joint_path_command (trajectory_msgs/JointTrajectory)
# Updates the current trajectory. Warning, side effect in msg
# ---------------------------------------------------------------------------------------
def joint_path_command_callback(msg):
    global trajectory_points
    global trajectory_start

    print "trajectory_points" , msg.points
    print "trajectory_start" , msg.header.stamp
    return

if __name__ == '__main__':
    try:
        rospy.init_node(conf_node_name)         # node name: grc_driver
        print "Driver wait for talnet service"
        rospy.logwarn( "Driver wait for talnet service")
        rospy.wait_for_service(conf_com_node)   # telnet node name: grc_telnet
        rospy.logwarn( "Driver connect to talnet service")

        trajectory_start = rospy.get_rostime()

        thread.start_new_thread(joint_states_publisher, (conf_rate,))
        thread.start_new_thread(move_manager, (conf_rate,))

        rospy.Subscriber(conf_trajectory_path_name, JointTrajectory, joint_path_command_callback)
        rospy.spin()

    except rospy.ROSInterruptException:
        pass

