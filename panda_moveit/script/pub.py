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
        self.place_states = ["place_1", "place_2", "place_3", "place_4"]
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





# import moveit_commander
# import rospy
# import tf2_ros
# import sys
# from geometry_msgs.msg import PoseStamped


# def get_transform():
#     rospy.init_node('get_transform_node', anonymous=True)
    
#     # Initialize tf2 listener and buffer
#     tf_buffer = tf2_ros.Buffer()
#     listener = tf2_ros.TransformListener(tf_buffer)

#     # Initialize MoveIt! Commander
#     moveit_commander.roscpp_initialize(sys.argv)
#     robot = moveit_commander.RobotCommander()
#     arm_group = moveit_commander.MoveGroupCommander("arm")
#     arm_group.set_pose_reference_frame("world")

#     # Gripper initialization
#     gripper_group = moveit_commander.MoveGroupCommander("gripper")
#     predefined_open_state = 'open'  # Defined in your SRDF for opening the gripper
#     predefined_close_state = 'close'  # Defined in your SRDF for closing the gripper
#     arm_group.set_named_target("s_place")
#     arm_group.go(wait=True)
#     # Open the gripper
#     rospy.loginfo("Opening the gripper...")
#     gripper_group.set_named_target(predefined_open_state)
#     gripper_group.go(wait=True)
#     rospy.sleep(2)
#     rospy.loginfo("Gripper opened successfully.")

#     try:
#         # Wait for the transform between 'world' and 'detected_object'
#         rospy.loginfo("Waiting for transform between 'world' and 'detected_object'...")
#         transform = tf_buffer.lookup_transform("world", "detected_object", rospy.Time(0), rospy.Duration(10.0))

#         # Extract translation
#         x = transform.transform.translation.x
#         y = transform.transform.translation.y
#         z = transform.transform.translation.z
#         rospy.loginfo(f"Transform obtained: x={x}, y={y}, z={z}")

#         # Define orientation (example - identity rotation; adjust as needed)
#         orientation = [1.000001, -0.02600001, -0.00900001, 0.00000001]
#         gripper_group.set_named_target(predefined_open_state)
#         gripper_group.go(wait=True)
#         # Define waypoints for Cartesian path
#         waypoints = []

#         # First waypoint (approach above the object)
#         target_pose0 = PoseStamped()
#         target_pose0.header.frame_id = "world"
#         target_pose0.pose.position.x = x
#         target_pose0.pose.position.y = y
#         target_pose0.pose.position.z = 0.271 + 0.1  # Adjust Z for approach
#         target_pose0.pose.orientation.x = orientation[0]
#         target_pose0.pose.orientation.y = orientation[1]
#         target_pose0.pose.orientation.z = orientation[2]
#         target_pose0.pose.orientation.w = orientation[3]
#         waypoints.append(target_pose0.pose)

#         # Second waypoint (reach the object)
#         target_pose1 = PoseStamped()
#         target_pose1.header.frame_id = "world"
#         target_pose1.pose.position.x = x
#         target_pose1.pose.position.y = y
#         target_pose1.pose.position.z = 0.271
#         target_pose1.pose.orientation.x = orientation[0]
#         target_pose1.pose.orientation.y = orientation[1]
#         target_pose1.pose.orientation.z = orientation[2]
#         target_pose1.pose.orientation.w = orientation[3]
#         waypoints.append(target_pose1.pose)

#         rospy.loginfo(f"Waypoints defined: {waypoints}")

#         # Retry mechanism for planning the Cartesian path
#         max_retries = 5
#         retries = 0
#         fraction = 0.0

#         while fraction < 0.9 and retries < max_retries:
#             rospy.loginfo(f"Planning Cartesian path (attempt {retries + 1})...")
#             (plan, fraction) = arm_group.compute_cartesian_path(
#                 waypoints,  # List of waypoints
#                 0.02,       # eef_step (meters)
#                 0.0,        # jump_threshold
#                 True        # Avoid collisions
#             )
#             rospy.loginfo(f"Cartesian path computed with coverage: {fraction * 100:.2f}%")

#             if fraction >= 0.9:
#                 rospy.loginfo("Sufficient path coverage achieved. Executing motion...")
#                 try:
#                     arm_group.execute(plan, wait=True)
#                     rospy.loginfo("Motion executed successfully!")
#                     break
#                 except Exception as e:
#                     rospy.logerr(f"Execution failed: {e}")
#             else:
#                 retries += 1
#                 rospy.logwarn(f"Insufficient path coverage. Retrying... {retries}/{max_retries}")

#         if retries >= max_retries:
#             rospy.logerr("Failed to compute a valid Cartesian path after multiple attempts.")
#             return
        
#         print('Target pose set.')

#         # Plan and execute the trajectory

#         # Close the gripper
#         rospy.loginfo("Closing the gripper...")
#         gripper_group.set_named_target(predefined_close_state)
#         gripper_group.go(wait=True)
#         rospy.sleep(2)
#         rospy.loginfo("Gripper closed successfully.")
#         # arm_group.set_pose_target(target_pose1)
#         # plan_success, plan, planning_time, error_code = arm_group.plan()
#         # if plan_success:
#         #     arm_group.execute(plan)
#         #     print("Trajectory executed successfully.")
#         # else:
#         #     rospy.logwarn("Failed to plan a trajectory.")
#         # Move to b_place
#         rospy.loginfo("Moving to 'b_place' pose...")
#         arm_group.set_named_target("b_place")
#         arm_group.go(wait=True)
#         rospy.sleep(2)


#         arm_group.set_named_target("s_place")
#         arm_group.go(wait=True)
#         rospy.sleep(2)

#         # Open the gripper
#         rospy.loginfo("Opening the gripper...")
#         gripper_group.set_named_target(predefined_open_state)
#         gripper_group.go(wait=True)
#         rospy.loginfo("Gripper opened successfully.")

#         # Move to m_pose
#         # rospy.loginfo("Moving to 'm_pose' pose...")
#         # arm_group.set_named_target("m_pose")
#         # arm_group.go(wait=True)

#     except (tf2_ros.TransformException, rospy.ROSException) as e:
#         rospy.logerr(f"Failed to get transform or execute motion: {e}")


# if __name__ == '__main__':
#     get_transform()











# import moveit_commander
# import rospy
# import tf2_ros
# import sys
# from geometry_msgs.msg import PoseStamped
# from tf2_geometry_msgs import tf2_geometry_msgs


# def get_transform():
#     rospy.init_node('get_transform_node', anonymous=True)
    
#     # Initialize tf2 listener and buffer
#     tf_buffer = tf2_ros.Buffer()
#     listener = tf2_ros.TransformListener(tf_buffer)

#     # Initialize MoveIt! Commander
#     moveit_commander.roscpp_initialize(sys.argv)
#     robot = moveit_commander.RobotCommander()
#     group = moveit_commander.MoveGroupCommander("arm")
#     group.set_pose_reference_frame("world")

#     # Wait until the transform is available
#     try:
#         # Wait for transform between 'world' and 'detected_object'
#         rospy.loginfo("Waiting for transform...")
#         transform = tf_buffer.lookup_transform("world", "detected_object", rospy.Time(0), rospy.Duration(10.0))

#         # You can access the position from the transform
#         x = transform.transform.translation.x
#         y = transform.transform.translation.y
#         z = transform.transform.translation.z

#         rospy.loginfo(f"Transform obtained: x={x}, y={y}, z={z}")

#         # Define orientation (example - identity rotation, change if needed)
#         orientation = [1.000000001, -0.0260000000000001, -0.00900000000000001, 0.000100000000000000000001]

#         # Define waypoints for Cartesian path
#         waypoints = []

#         # First waypoint
#         target_pose0 = PoseStamped()
#         target_pose0.header.frame_id = "base_link"
#         target_pose0.pose.position.x = x
#         target_pose0.pose.position.y = y
#         target_pose0.pose.position.z = 0.271 + 0.1  # Adjust the Z for the first pose
#         target_pose0.pose.orientation.x = orientation[0]
#         target_pose0.pose.orientation.y = orientation[1]
#         target_pose0.pose.orientation.z = orientation[2]
#         target_pose0.pose.orientation.w = orientation[3]
#         waypoints.append(target_pose0.pose)

#         # Second waypoint
#         target_pose1 = PoseStamped()
#         target_pose1.header.frame_id = "base_link"
#         target_pose1.pose.position.x = x
#         target_pose1.pose.position.y = y
#         target_pose1.pose.position.z = 0.271
#         target_pose1.pose.orientation.x = orientation[0]
#         target_pose1.pose.orientation.y = orientation[1]
#         target_pose1.pose.orientation.z = orientation[2]
#         target_pose1.pose.orientation.w = orientation[3]
#         waypoints.append(target_pose1.pose)

#         rospy.loginfo(f"Waypoints: {waypoints}")

#         # Retry mechanism to keep planning until the fraction is above 90%
#         max_retries = 5  # Set a maximum number of retries
#         retries = 0
#         fraction = 0.0

#         while fraction < 0.9 and retries < max_retries:
#             # Plan Cartesian path
#             rospy.loginfo("Planning Cartesian path...")
#             (plan, fraction) = group.compute_cartesian_path(
#                 waypoints,  # List of waypoints
#                 0.025,       # eef_step (meters)
#                 0.0,        # jump_threshold
#                 True        # Avoid collisions
#             )

#             rospy.loginfo(f"Cartesian path computed: Coverage = {fraction * 100:.2f}%")

#             # Check if the plan was successful
#             if fraction >= 0.9:
#                 rospy.loginfo(f"Path computed successfully. Coverage: {fraction * 100:.2f}%")
#                 try:
#                     group.execute(plan, wait=True)
#                     rospy.loginfo("Motion executed successfully!")
#                     break  # Exit the loop if successful
#                 except Exception as e:
#                     rospy.logerr(f"Execution failed: {e}")
#                     break  # Exit the loop on execution failure
#             else:
#                 retries += 1
#                 rospy.logwarn(f"Path planning failed. Coverage: {fraction * 100:.2f}%. Retrying... {retries}/{max_retries}")

#         if retries >= max_retries:
#             rospy.logerr("Failed to compute a valid path after multiple attempts.")

#     except (tf2_ros.TransformException, rospy.ROSException) as e:
#         rospy.logerr(f"Failed to get transform: {e}")


# if __name__ == '__main__':
#     get_transform()






# strawberries bin
# x=[-0.405, 0.501, 0.354]
# 0= [0.027, 1.000, -0.001, -0.004]










# import moveit_commander
# import rospy
# import tf2_ros
# import sys
# from geometry_msgs.msg import PoseStamped

# def get_transform():
#     rospy.init_node('get_transform_node', anonymous=True)
#     tf_buffer = tf2_ros.Buffer()
#     listener = tf2_ros.TransformListener(tf_buffer)

#     moveit_commander.roscpp_initialize(sys.argv)
#     robot = moveit_commander.RobotCommander()
#     group = moveit_commander.MoveGroupCommander("arm")

#     try:
#         # Wait until the transform is available
#         transform = tf_buffer.lookup_transform("world", "detected_object", rospy.Time(), rospy.Duration(10.0))

#         x_formatted = "{:.1f}".format(transform.transform.translation.x)
#         y_formatted = "{:.1f}".format(transform.transform.translation.y)
#         z_formatted = "{:.3f}".format(transform.transform.translation.z)

#         # Define the target pose
#         o=[1.000000000000000000000000000001, -0.02600000000000000001, -0.0090000001, 0.00000000000000000000000010]
#         target_pose = PoseStamped()
#         target_pose.header.frame_id = "world"
#         # target_pose.pose.position.x = float(x_formatted)
#         # target_pose.pose.position.y = float(y_formatted)
#         print(f"x:: {x_formatted}            y:: {y_formatted}")
#         target_pose.pose.position.x = transform.transform.translation.x
#         target_pose.pose.position.y = transform.transform.translation.y
#         target_pose.pose.position.z =  0.418 + 0.16
#         target_pose.pose.orientation.x = o[0]
#         target_pose.pose.orientation.y = o[1]
#         target_pose.pose.orientation.z = o[2]
#         target_pose.pose.orientation.w = o[3]

#         # Set the target pose for the end effector
#         group.set_pose_target(target_pose)
#         print('Target pose set.')

#         # Plan and execute the trajectory
#         plan_success, plan, planning_time, error_code = group.plan()
#         if plan_success:
#             group.execute(plan)
#             print("Trajectory executed successfully.")
#         else:
#             rospy.logwarn("Failed to plan a trajectory.")

#         # target_pose = PoseStamped()
#         # target_pose.header.frame_id = "world"
#         # target_pose.pose.position.x = float(x_formatted)
#         # target_pose.pose.position.y = float(y_formatted)
#         # target_pose.pose.position.z =  0.418 
#         # target_pose.pose.orientation.x = o[0]
#         # target_pose.pose.orientation.y = o[1]
#         # target_pose.pose.orientation.z = o[2]
#         # target_pose.pose.orientation.w = o[3]

#         # # Set the target pose for the end effector
#         # group.set_pose_target(target_pose)
#         # print('Target pose set.')

#         # # Plan and execute the trajectory
#         # plan_success, plan, planning_time, error_code = group.plan()
#         # if plan_success:
#         #     group.execute(plan)
#         #     print("Trajectory executed successfully.")
#         # else:
#         #     rospy.logwarn("Failed to plan a trajectory.")
            

#     except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
#         rospy.logwarn("Did not find the detected object: {}".format(e))

# if __name__ == '__main__':
#     try:
#         get_transform()
#     except rospy.ROSInterruptException:
#         pass


