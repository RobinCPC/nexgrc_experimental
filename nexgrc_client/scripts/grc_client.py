#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2019 NexCOBOT Inc.
# Author: Robin Chen
#
# -----------------------------------------------------------------------------
# This node manages the connection between ROS and NexGRC controller through a TCP/IP connection
# The service provided accepts string commands with parameters and returns the produced answer from the robot.
# -----------------------------------------------------------------------------
import rospy
import socket
import thread
import time
from nexgrc_client.srv import *

# Default  global parameters
TCP_IP = "192.168.88.100"
TCP_PORT = 1688
SERVICE_NAME = 'grc_telnet'

# Create tcpip socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lock = thread.allocate_lock() 	# Lock for tcp communication. Only one command can be sent at the same time

# Connect with NexGRC Controller
def connect():
    while not rospy.is_shutdown():
        try:
            rospy.logwarn('Connecting to ' + TCP_IP + ':' + str(TCP_PORT))
            sock.connect((TCP_IP, TCP_PORT))
            rospy.logwarn('Connected to ' + TCP_IP + ':' + str(TCP_PORT))
            break
        except:
            # Wait and reconnect
            time.sleep(1)

# Flush line through the socket.
def flush(line):
    while not rospy.is_shutdown():
        try:
            sock.send(line)
            return sock.recv(1024)
        except:
            connect()

# ROS service: transforms the received command into string
def send_command(req):
    with lock:
        response = StringCommandResponse()      # ROS StringCommandResponse service response
        response.error_code = 0

        rospy.logdebug('Send: ' + req.command + ' : ' + req.parameters + '\n')
        response.response = flush(req.command + ' : ' + req.parameters + '\n')
        rospy.logdebug('Received: ' + response.response)

        if response.response == 'error':
            response.error_code = 1
        return response


# Main Function
if __name__ == '__main__':
    # Start node
    rospy.init_node('grc_client')

    TCP_IP = rospy.get_param('~robot_ip', TCP_IP)
    TCP_PORT = rospy.get_param('~robot_port', TCP_PORT)

    connect()

    srv = rospy.Service(SERVICE_NAME, StringCommand, send_command)

    rospy.spin()

