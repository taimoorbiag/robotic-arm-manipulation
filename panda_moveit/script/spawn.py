#!/usr/bin/env python3


#!/usr/bin/env python3
from gazebo_msgs.srv import SpawnModel, DeleteModel
import rospy
from geometry_msgs.msg import Pose
import rospkg
import random
import math

# Initialize the ROS node
rospy.init_node('spawn_model_node')

# Create ServiceProxies to call the spawn_model and delete_model services
spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
delete_model_client = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

# Wait for the services to be available
rospy.wait_for_service('/gazebo/spawn_sdf_model')
rospy.wait_for_service('/gazebo/delete_model')

# Use rospkg to get the path to the package
rospack = rospkg.RosPack()
package_path = rospack.get_path('panda_moveit')

# Construct the full paths to the SDF model files
unit_box_model_sdf_path = package_path + '/model/unit_box_panda/model.sdf'

# Load the SDF model file
with open(unit_box_model_sdf_path, 'r') as unit_box_model_file:
    unit_box_model_xml = unit_box_model_file.read()

# Define the robot namespace and reference frame
robot_namespace = '/foo'
reference_frame = 'world'

# Function to delete a model
def delete_model(model_name):
    try:
        delete_model_client(model_name)
        rospy.loginfo(f"Deleted model: {model_name}")
    except rospy.ServiceException as e:
        rospy.logwarn(f"Failed to delete model '{model_name}': {e}")

# Function to spawn a single model
def spawn_model(model_name, model_xml, x, y, z):
    initial_pose = Pose()
    initial_pose.position.x = x
    initial_pose.position.y = y
    initial_pose.position.z = z
    
    try:
        spawn_model_client(model_name, model_xml, robot_namespace, initial_pose, reference_frame)
        rospy.loginfo(f"Spawned model '{model_name}' at position ({x}, {y}, {z}).")
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call to spawn model '{model_name}' failed: {e}")

# Function to check the distance between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# List to store positions of the spawned models
spawned_positions = []

# Function to check if the new position is valid (at least 0.1 meters away from other objects)
def is_valid_position(x, y, min_distance=0.1):
    for pos in spawned_positions:
        if distance(x, y, pos[0], pos[1]) < min_distance:
            return False
    return True

# First, delete old unit_box models if they exist
for i in range(1, 4):
    model_name = f'unit_box{i}'
    delete_model(model_name)

# Wait a short moment for deletion to take effect
rospy.sleep(1.0)

# Spawn 3 unit box models with unique names and random positions
z = 0.16
for i in range(3):
    model_name = f'unit_box{i+1}'
    while True:
        x = random.uniform(0.44, 0.6)
        y = random.uniform(-0.15, 0.1)
        if is_valid_position(x, y):
            break

    spawn_model(model_name, unit_box_model_xml, x, y, z)
    spawned_positions.append((x, y))



















# from gazebo_msgs.srv import SpawnModel
# import rospy
# from geometry_msgs.msg import Pose
# import rospkg
# import random

# # Initialize the ROS node
# rospy.init_node('spawn_model_node')

# # Create a ServiceProxy to call the spawn_model service
# spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)

# # Use rospkg to get the path to the package
# rospack = rospkg.RosPack()
# package_path = rospack.get_path('panda_moveit')

# # Construct the full paths to the SDF model files
# sphere_model_sdf_path = package_path + '/model/panda_sphere/model.sdf'
# unit_box_model_sdf_path = package_path + '/model/unit_box_panda/model.sdf'

# # Load the SDF model files
# with open(sphere_model_sdf_path, 'r') as sphere_model_file:
#     sphere_model_xml = sphere_model_file.read()

# with open(unit_box_model_sdf_path, 'r') as unit_box_model_file:
#     unit_box_model_xml = unit_box_model_file.read()

# # Define the robot namespace and reference frame
# robot_namespace = '/foo'
# reference_frame = 'world'

# # Function to spawn a single model
# def spawn_model(model_name, model_xml, x, y, z):
#     initial_pose = Pose()
#     initial_pose.position.x = x
#     initial_pose.position.y = y
#     initial_pose.position.z = z
    
#     try:
#         spawn_model_client(model_name, model_xml, robot_namespace, initial_pose, reference_frame)
#         rospy.loginfo(f"Spawned model '{model_name}' at position ({x}, {y}, {z}).")
#     except rospy.ServiceException as e:
#         rospy.logerr(f"Service call to spawn model '{model_name}' failed: {e}")

# # Spawn 4 sphere models with unique names and random positions
# z = 0.31
# x_positions = [0.55, 0.65, 0.75, 0.95]
# for i in range(3):
#     model_name = f'sphere{i+1}'
#     x = random.choice(x_positions)
#     y = random.uniform(-0.25, 0.25)
#     spawn_model(model_name, sphere_model_xml, x, y, z)

# # Spawn 4 unit box models with unique names and random positions
# z = 0.31
# for i in range(3):
#     model_name = f'unit_box{i+1}'
#     x = random.choice(x_positions)
#     y = random.uniform(-0.25, 0.25)
#     spawn_model(model_name, unit_box_model_xml, x, y, z)










# from gazebo_msgs.srv import SpawnModel
# import rospy
# from geometry_msgs.msg import Pose

# # Initialize the ROS node
# rospy.init_node('spawn_model_node')

# # Create a ServiceProxy to call the spawn_model service
# spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)

# # Define the model's name
# model_name = 'box'

# # Load the SDF model file
# model_xml = open('/home/bacha20/model_editor_models/unit_box_panda/model.sdf', 'r').read()

# # Define the robot namespace and initial pose
# robot_namespace = '/foo'
# initial_pose = Pose()
# initial_pose.position.x = -0.002129  # Set X coordinate to 1
# initial_pose.position.y = 0.126578 # Set Y coordinate to 1
# initial_pose.position.z = 0.241766 # Set Z coordinate to 1

# # Set the reference frame
# reference_frame = 'world'

# # Call the spawn_model service to spawn the model
# try:
#     spawn_model_client(model_name, model_xml, robot_namespace, initial_pose, reference_frame)
#     rospy.loginfo(f"Spawned model '{model_name}' with initial pose (1, 1, 1).")
# except rospy.ServiceException as e:
#     rospy.logerr(f"Service call to spawn model failed: {e}")

# # Keep the script running
# rospy.spin()


















# from gazebo_msgs.srv import SpawnModel
# import rospy
# from geometry_msgs.msg import Pose
# import rospkg
# # Initialize the ROS node
# rospy.init_node('spawn_model_node')

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

# # Keep the script running
# rospy.spin()
