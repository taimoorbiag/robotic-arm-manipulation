#!/usr/bin/env python3



import rospy
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import Pose
from std_msgs.msg import Header

# Initialize ROS node
rospy.init_node('publish_collision_object_node')

# Create a publisher for the collision object
collision_object_publisher = rospy.Publisher('/collision_object', CollisionObject, queue_size=10)

# Wait for the publisher to be ready
rospy.sleep(1)

# Define the collision object
collision_object = CollisionObject()
collision_object.id = "box_1"
collision_object.header = Header()
collision_object.header.frame_id = "world"

# Define the primitive (box)
box = SolidPrimitive()
box.type = SolidPrimitive.BOX
box.dimensions = [0.3, 0.3, 0.15]  # Dimensions of the box

# Define the pose of the box
box_pose = Pose()
box_pose.position.x = 0.5
box_pose.position.y = 0.0
box_pose.position.z = 0.075
box_pose.orientation.x = 0.0
box_pose.orientation.y = 0.0
box_pose.orientation.z = 0.0
box_pose.orientation.w = 1.0

# Add the primitive and pose to the collision object
collision_object.primitives.append(box)
collision_object.primitive_poses.append(box_pose)
collision_object.operation = CollisionObject.ADD

# Publish the collision object
rospy.loginfo("Publishing collision object...")
collision_object_publisher.publish(collision_object)

# Keep the script alive to ensure message is published
rospy.spin()

















# import sys
# import rospy
# import moveit_commander
# import moveit_msgs.msg
# import geometry_msgs.msg
# import rospkg

# rospy.init_node('move_group_python_interface', anonymous=True)

# # Initialize the moveit_commander
# moveit_commander.roscpp_initialize(sys.argv)

# # Instantiate a RobotCommander object
# robot = moveit_commander.RobotCommander()

# # Instantiate a PlanningSceneInterface object
# scene = moveit_commander.PlanningSceneInterface()


# group_name = "arm"  # Change to your group name if different
# move_group = moveit_commander.MoveGroupCommander(group_name)

# # Get information for debugging
# planning_frame = move_group.get_planning_frame()
# rospy.loginfo(f"Planning frame: {planning_frame}")

# eef_link = move_group.get_end_effector_link()
# rospy.loginfo(f"End effector link: {eef_link}")

# group_names = robot.get_group_names()
# rospy.loginfo(f"Available Planning Groups: {group_names}")

# rospy.loginfo(f"Robot state: {robot.get_current_state()}")

# # Load and execute the predefined group state
# predefined_state_name = 'straight'  # The state name defined in your SRDF
# move_group.set_named_target(predefined_state_name)

# # Plan to the new state
# plan = move_group.go(wait=True)

# # Ensure that there is no residual movement
# move_group.stop()

# # Clear pose targets
# move_group.clear_pose_targets()













# # Instantiate a MoveGroupCommander object for the arm
# group_name = "gripper"  # Change to your group name if different
# move_group = moveit_commander.MoveGroupCommander(group_name)

# # Get information for debugging
# planning_frame = move_group.get_planning_frame()
# rospy.loginfo(f"Planning frame: {planning_frame}")

# eef_link = move_group.get_end_effector_link()
# rospy.loginfo(f"End effector link: {eef_link}")

# group_names = robot.get_group_names()
# rospy.loginfo(f"Available Planning Groups: {group_names}")

# rospy.loginfo(f"Robot state: {robot.get_current_state()}")

# # Load and execute the predefined group state
# predefined_state_name = 'gripper_open'  # The state name defined in your SRDF
# move_group.set_named_target(predefined_state_name)

# # Plan to the new state
# plan = move_group.go(wait=True)

# # Ensure that there is no residual movement
# move_group.stop()

# # Clear pose targets
# move_group.clear_pose_targets()

# rospy.loginfo(f"Executed the group state: {predefined_state_name}")





# rospy.sleep(1)

# from gazebo_msgs.srv import SpawnModel
# import rospy
# from geometry_msgs.msg import Pose
# import rospkg
# # Initialize the ROS node
# # rospy.init_node('spawn_model_node')

# # Create a ServiceProxy to call the spawn_model service
# spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)

# # Define the model's name
# model_name = 'box'

# # Load the SDF model file
# # model_xml = open('/home/bacha20/model_editor_models/arm_clynder/model.sdf', 'r').read()
# # model_xml = open('/home/ubunut20/model_editor_models/unit_cylinder/model.sdf', 'r').read()

# # Use rospkg to get the path to the package
# rospack = rospkg.RosPack()
# package_path = rospack.get_path('panda_moveit')

# # Construct the full path to the SDF model file
# model_sdf_path = package_path + '/model/unit_box_panda/model.sdf'

# # Load the SDF model file
# with open(model_sdf_path, 'r') as model_file:
#     model_xml = model_file.read()













# # Define the robot namespace and initial pose
# robot_namespace = '/foo'
# initial_pose = Pose()
# initial_pose.position.x = 0.774703 # Set X coordinate
# initial_pose.position.y = 0.002095   # Set Y coordinate
# initial_pose.position.z = 0.292557  # Set Z coordinate  0.168327
# # initial_pose.position.z = 0.132106
# # Set orientation (quaternion representation)
# # initial_pose.orientation.x = 1.629220
# # initial_pose.orientation.y = 0.012144
# # initial_pose.orientation.z = -0.666762
# # initial_pose.orientation.w = 1.0  # Default orientation (no rotation)

# # Set the reference frame
# reference_frame = 'world'

# # Call the spawn_model service to spawn the model
# try:
#     spawn_model_client(model_name, model_xml, robot_namespace, initial_pose, reference_frame)
#     rospy.loginfo(f"Spawned model '{model_name}' with initial pose and orientation.")
# except rospy.ServiceException as e:
#     rospy.logerr(f"Service call to spawn model failed: {e}")


# rospy.sleep(5)
# group_name = "arm"  # Change to your group name if different
# move_group = moveit_commander.MoveGroupCommander(group_name)

# # Get information for debugging
# planning_frame = move_group.get_planning_frame()
# rospy.loginfo(f"Planning frame: {planning_frame}")

# eef_link = move_group.get_end_effector_link()
# rospy.loginfo(f"End effector link: {eef_link}")

# group_names = robot.get_group_names()
# rospy.loginfo(f"Available Planning Groups: {group_names}")

# rospy.loginfo(f"Robot state: {robot.get_current_state()}")

# # Load and execute the predefined group state
# predefined_state_name = 'pick'  # The state name defined in your SRDF
# move_group.set_named_target(predefined_state_name)

# # Plan to the new state
# plan = move_group.go(wait=True)

# # Ensure that there is no residual movement
# move_group.stop()

# # Clear pose targets
# move_group.clear_pose_targets()





# group_name = "gripper"  # Change to your group name if different
# move_group = moveit_commander.MoveGroupCommander(group_name)

# # Get information for debugging
# planning_frame = move_group.get_planning_frame()
# rospy.loginfo(f"Planning frame: {planning_frame}")

# eef_link = move_group.get_end_effector_link()
# rospy.loginfo(f"End effector link: {eef_link}")

# group_names = robot.get_group_names()
# rospy.loginfo(f"Available Planning Groups: {group_names}")

# rospy.loginfo(f"Robot state: {robot.get_current_state()}")

# # Load and execute the predefined group state
# predefined_state_name = 'gripper_close'  # The state name defined in your SRDF
# move_group.set_named_target(predefined_state_name)

# # Plan to the new state
# plan = move_group.go(wait=True)

# # Ensure that there is no residual movement
# move_group.stop()

# # Clear pose targets
# move_group.clear_pose_targets()








# group_name = "arm"  # Change to your group name if different
# move_group = moveit_commander.MoveGroupCommander(group_name)

# # Get information for debugging
# planning_frame = move_group.get_planning_frame()
# rospy.loginfo(f"Planning frame: {planning_frame}")

# eef_link = move_group.get_end_effector_link()
# rospy.loginfo(f"End effector link: {eef_link}")

# group_names = robot.get_group_names()
# rospy.loginfo(f"Available Planning Groups: {group_names}")

# rospy.loginfo(f"Robot state: {robot.get_current_state()}")

# # Load and execute the predefined group state
# predefined_state_name = 'straight'  # The state name defined in your SRDF
# move_group.set_named_target(predefined_state_name)

# # Plan to the new state
# plan = move_group.go(wait=True)

# # Ensure that there is no residual movement
# move_group.stop()

# # Clear pose targets
# move_group.clear_pose_targets()


# # group_name = "gripper"  # Change to your group name if different
# # move_group = moveit_commander.MoveGroupCommander(group_name)

# # # Get information for debugging
# # planning_frame = move_group.get_planning_frame()
# # rospy.loginfo(f"Planning frame: {planning_frame}")

# # eef_link = move_group.get_end_effector_link()
# # rospy.loginfo(f"End effector link: {eef_link}")

# # group_names = robot.get_group_names()
# # rospy.loginfo(f"Available Planning Groups: {group_names}")

# # rospy.loginfo(f"Robot state: {robot.get_current_state()}")

# # # Load and execute the predefined group state
# # predefined_state_name = 'gripper_close'  # The state name defined in your SRDF
# # move_group.set_named_target(predefined_state_name)

# # # Plan to the new state
# # plan = move_group.go(wait=True)

# # # Ensure that there is no residual movement
# # move_group.stop()

# # # Clear pose targets
# # move_group.clear_pose_targets()


# rospy.sleep(2)


# group_name = "arm"  # Change to your group name if different
# move_group = moveit_commander.MoveGroupCommander(group_name)

# # Get information for debugging
# planning_frame = move_group.get_planning_frame()
# rospy.loginfo(f"Planning frame: {planning_frame}")

# eef_link = move_group.get_end_effector_link()
# rospy.loginfo(f"End effector link: {eef_link}")

# group_names = robot.get_group_names()
# rospy.loginfo(f"Available Planning Groups: {group_names}")

# rospy.loginfo(f"Robot state: {robot.get_current_state()}")

# # Load and execute the predefined group state
# predefined_state_name = 'place'  # The state name defined in your SRDF
# move_group.set_named_target(predefined_state_name)

# # Plan to the new state
# plan = move_group.go(wait=True)

# # Ensure that there is no residual movement
# move_group.stop()

# # Clear pose targets
# move_group.clear_pose_targets()











# rospy.sleep(2)

# group_name = "gripper"  # Change to your group name if different
# move_group = moveit_commander.MoveGroupCommander(group_name)

# # Get information for debugging
# planning_frame = move_group.get_planning_frame()
# rospy.loginfo(f"Planning frame: {planning_frame}")

# eef_link = move_group.get_end_effector_link()
# rospy.loginfo(f"End effector link: {eef_link}")

# group_names = robot.get_group_names()
# rospy.loginfo(f"Available Planning Groups: {group_names}")

# rospy.loginfo(f"Robot state: {robot.get_current_state()}")

# # Load and execute the predefined group state
# predefined_state_name = 'gripper_open'  # The state name defined in your SRDF
# move_group.set_named_target(predefined_state_name)

# # Plan to the new state
# plan = move_group.go(wait=True)

# # Ensure that there is no residual movement
# move_group.stop()

# # Clear pose targets
# move_group.clear_pose_targets()