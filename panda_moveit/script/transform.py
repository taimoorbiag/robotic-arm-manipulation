#!/usr/bin/env python3

import rospy
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import TransformStamped

class TransformListenerExample:
    def __init__(self):
        rospy.init_node('transform_listener_example')

        # Create TF buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)

        # Start checking for transform
        self.check_transform()

    def check_transform(self):
        rate = rospy.Rate(1)  # 1 Hz

        while not rospy.is_shutdown():
            try:
                rospy.loginfo("Waiting for transform between 'world' and 'detected_object_1'...")
                # Wait for up to 10 seconds for the transform
                transform = self.tf_buffer.lookup_transform(
                    "world", 
                    "detected_object_1", 
                    rospy.Time(0), 
                    rospy.Duration(10.0)
                )

                x = transform.transform.translation.x
                y = transform.transform.translation.y
                z = transform.transform.translation.z
                rospy.loginfo(f"Transform obtained: x={x}, y={y}, z={z}")

            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                rospy.logwarn(f"Could not get transform: {e}")
                # You can return, break or just continue waiting
                continue

            rate.sleep()

if __name__ == '__main__':
    try:
        TransformListenerExample()
    except rospy.ROSInterruptException:
        pass
