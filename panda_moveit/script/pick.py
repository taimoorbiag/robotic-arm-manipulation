#!/usr/bin/env python3
import moveit_commander
import rospy
import tf2_ros
import sys
from geometry_msgs.msg import PoseStamped


class ObjectClassHandler:
    def __init__(self):
        rospy.init_node('get_transform_node', anonymous=True)

        # Initialize tf2 listener and buffer
        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)

        # Initialize MoveIt! Commander
        moveit_commander.roscpp_initialize(sys.argv)
        self.robot = moveit_commander.RobotCommander()
        self.arm_group = moveit_commander.MoveGroupCommander("arm")
        self.arm_group.set_pose_reference_frame("world")

        # Gripper initialization
        self.gripper_group = moveit_commander.MoveGroupCommander("gripper")
        self.predefined_open_state = 'open'
        self.predefined_close_state = 'close'

        # Place state management
        self.place_states = ["place_1", "place_2", "place_4", "place_3"]
        self.current_place_index = 0

        self.motion_executed = False

    def execute_motion(self):
        if not self.motion_executed:
            # Move to first place position and open gripper
            initial_place = self.place_states[self.current_place_index]
            rospy.loginfo(f"Moving to initial place position: {initial_place}")
            self.arm_group.set_named_target("place_1")
            self.arm_group.go(wait=True)

            rospy.loginfo("Opening the gripper at initial position...")
            self.gripper_group.set_named_target(self.predefined_open_state)
            self.gripper_group.go(wait=True)
            rospy.loginfo("Gripper opened successfully.")
            self.motion_executed = True

        try:
            rospy.loginfo("Waiting for transform between 'world' and 'detected_object_1'...")
            transform = self.tf_buffer.lookup_transform("world", "detected_object_1", rospy.Time(0), rospy.Duration(10.0))

            x = transform.transform.translation.x
            y = transform.transform.translation.y
            z = transform.transform.translation.z
            rospy.loginfo(f"Transform obtained: x={x}, y={y}, z={z}")

            # Example orientation
            orientation = [1.0, -0.026, -0.009, 0.00001]

            waypoints = []

            # Approach above object
            target_pose0 = PoseStamped()
            target_pose0.header.frame_id = "world"
            target_pose0.pose.position.x = x
            target_pose0.pose.position.y = y
            target_pose0.pose.position.z = 0.125 + 0.1
            target_pose0.pose.orientation.x = orientation[0]
            target_pose0.pose.orientation.y = orientation[1]
            target_pose0.pose.orientation.z = orientation[2]
            target_pose0.pose.orientation.w = orientation[3]
            waypoints.append(target_pose0.pose)

            # Move down to object
            target_pose1 = PoseStamped()
            target_pose1.header.frame_id = "world"
            target_pose1.pose.position.x = x
            target_pose1.pose.position.y = y
            target_pose1.pose.position.z = 0.125
            target_pose1.pose.orientation.x = orientation[0]
            target_pose1.pose.orientation.y = orientation[1]
            target_pose1.pose.orientation.z = orientation[2]
            target_pose1.pose.orientation.w = orientation[3]
            waypoints.append(target_pose1.pose)

            rospy.loginfo(f"Waypoints defined: {waypoints}")

            # Plan Cartesian path
            max_retries = 5
            retries = 0
            fraction = 0.0

            while fraction < 0.9 and retries < max_retries:
                rospy.loginfo(f"Planning Cartesian path (attempt {retries + 1})...")
                (plan, fraction) = self.arm_group.compute_cartesian_path(
                    waypoints,
                    0.02,
                    True
                )
                rospy.loginfo(f"Path coverage: {fraction * 100:.2f}%")
                if fraction >= 0.9:
                    rospy.loginfo("Executing planned path...")
                    self.arm_group.execute(plan, wait=True)
                    rospy.loginfo("Path executed.")
                    break
                else:
                    retries += 1
                    rospy.logwarn(f"Retrying Cartesian plan: {retries}/{max_retries}")

            if retries >= max_retries:
                rospy.logerr("Failed to compute valid Cartesian path.")
                return

            # Close the gripper
            rospy.loginfo("Closing the gripper...")
            self.gripper_group.set_named_target(self.predefined_close_state)
            self.gripper_group.go(wait=True)
            rospy.sleep(2)
            rospy.loginfo("Gripper closed successfully.")

            # Move to place position
            current_place = self.place_states[self.current_place_index]
            rospy.loginfo(f"Moving to place position: {current_place}")
            self.arm_group.set_named_target(current_place)
            self.arm_group.go(wait=True)

            # Open the gripper after placing
            rospy.loginfo("Opening the gripper after placement...")
            self.gripper_group.set_named_target(self.predefined_open_state)
            self.gripper_group.go(wait=True)
            rospy.sleep(2)
            
            rospy.loginfo("Gripper opened after placement.")
            self.arm_group.set_named_target("place_1")
            self.arm_group.go(wait=True)
            # Move to next place index
            rospy.sleep(2)
            self.current_place_index = (self.current_place_index + 1) % len(self.place_states)

        except (tf2_ros.TransformException, rospy.ROSException) as e:
            rospy.logerr(f"Transform or motion failed: {e}")

    def run(self):
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.execute_motion()
            rate.sleep()


if __name__ == '__main__':
    handler = ObjectClassHandler()
    handler.run()


