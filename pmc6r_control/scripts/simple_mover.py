#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import rospy
from std_msgs.msg import Float64, Float64MultiArray, MultiArrayLayout, MultiArrayDimension
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
#import pdb

def send_command_std( pub_arm ):
    arr_layout = MultiArrayLayout()
    #pdb.set_trace()
    arr_layout.dim.append(MultiArrayDimension())
    arr_layout.dim[0].size = 6
    arr_layout.dim[0].label = "arm_values"
    #joint_name = ["joitn_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]
    #for j in xrange(len(joint_name)):
    #    arr_layout.dim.append(MultiArrayDimension())
    #    arr_layout.dim[0].size = 1
    #    arr_layout.dim[0].label = joint_name[j]
    arm_msg = Float64MultiArray()
    arm_msg.layout = arr_layout
    arm_msg.data = [math.pi*0.25, -1.0, 1., 1., 0.5, math.fabs(math.pi*-0.25)]
    while not rospy.is_shutdown():
        pub_arm.publish(arm_msg)
        arm_msg.data = arm_msg.data * -1
        rate.sleep()

def send_command_traj( pub_arm):
    jnt_traj_point = JointTrajectoryPoint()
    jnt_traj_point.positions = [math.pi*0.25, -1.0, 1., 1., 0.5, math.fabs(math.pi*-0.25)]
    while not rospy.is_shutdown():
        pub_arm.publish(jnt_traj_point)
        jnt_traj_point.positions *= -1
        rate.sleep()

def send_command_ind(pub_arm):
    joint_values = [math.pi*0.25, -1.0, 1., 1., 0.5, math.fabs(math.pi*-0.25)]
    while not rospy.is_shutdown():
        for p in xrange(len(pub_arm)):
            pub_arm[p].publish(joint_values[p])
            joint_values[p] *= -1
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('simple_mover')
    rospy.loginfo("Running! Simple move")
    #pub_arm = rospy.Publisher('/pmc6r/arm_controller/command', Float64MultiArray, queue_size=1)
    #pub_arm = rospy.Publisher('/pmc6r/arm_controller/command', JointTrajectory, queue_size=1)
    joint_name = ["joitn1", "joint2", "joint3", "joint4", "joint5", "joint6"]
    pub_arm = []
    for i in xrange(len(joint_name)):
        pub_arm.append(
                rospy.Publisher('/pmc6r/' + joint_name[i] + '_position_controller/command', Float64, queue_size = 5)
                )
    rate = rospy.Rate(0.2);
    #send_command_std()
    #send_command_traj()
    send_command_ind(pub_arm)
    rospy.spin()

