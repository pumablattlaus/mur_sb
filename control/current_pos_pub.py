#!/usr/bin/env python 

import tf
import rospy
from geometry_msgs.msg import Pose
#import roslib
#roslib.load_manifest('learning')
#import math
#import numpy as np

if __name__ == "__main__":
    rospy.init_node("listener")
    
    listener = tf.TransformListener()
    
    robot_pose = rospy.Publisher('/tool0_pose', Pose, queue_size=1)

    listener.waitForTransform('base_link', 'tool0', rospy.Time(), rospy.Duration(4.0))
    rate = rospy.Rate(10.0)
    #print("Receiving...")
    
    while not rospy.is_shutdown():
        try:
            now = rospy.Time.now()
            listener.waitForTransform("base_link", "tool0", now, rospy.Duration(4.0))
            (trans,rot) = listener.lookupTransform('base_link', 'tool0', now)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        cmd = Pose()
        cmd.position.x = trans[0]
        cmd.position.y = trans[1]
        cmd.position.z = trans[2]
        cmd.orientation.x = rot[0]
        cmd.orientation.y = rot[1]
        cmd.orientation.z = rot[2]
        cmd.orientation.w = rot[3]
        print(cmd)
        robot_pose.publish(cmd)
        rate.sleep()
        
    
    
    
    #print("Stopped...")
