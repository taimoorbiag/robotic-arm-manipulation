# Warehouse Robotic Manipulation
## Vision-Guided Pick-and-Place with a Panda Robotic Arm

A simulation-based robotics project that combines computer vision, motion planning, and robotic manipulation to automate warehouse-style pick-and-place tasks.

Developed by **Mirza Taimoor Sultan Baig** as an MSc dissertation project at the **University of Essex**.

## Project Overview

The system uses an overhead camera and YOLO object detection to identify boxes in a simulated workspace. Object positions are passed to the motion planning system, allowing a Franka Emika Panda robotic arm to pick up the boxes and move them to a predefined target location.

Gazebo provides the simulation environment, ROS connects the system components, and MoveIt handles robotic arm motion planning.

## Main Features

- YOLO-based box detection using a simulated RGB camera.
- Vision-guided object localisation.
- MoveIt motion planning for the Panda robotic arm.
- Two-finger gripper control.
- Automated approach, grasp, transport, and placement sequence.
- Four-box simulation scenario.
- ROS communication between perception and manipulation components.

## Technologies Used

| Component | Technology |
|-----------|------------|
| Robotics middleware | ROS |
| Simulation | Gazebo |
| Motion planning | MoveIt |
| Object detection | YOLO |
| Programming | Python |
| Robotic arm | Franka Emika Panda, 7 DOF |
| End effector | Two-finger parallel gripper |
| Workspace build system | Catkin |

## How It Works

1. The overhead camera captures the workspace.
2. YOLO detects the boxes.
3. Detection coordinates are converted into workspace positions.
4. ROS passes the object position to the manipulation system.
5. MoveIt plans the arm movement.
6. The arm approaches the box and closes the gripper.
7. The arm transports the box to the target location.
8. The gripper releases the box, and the arm returns for the next task.

## Requirements

Before running the project, prepare a compatible ROS environment with:

- Gazebo and ROS integration packages.
- MoveIt.
- Panda robot description and controller packages.
- The Python dependencies required by the detection scripts.
- The YOLO model weights expected by the perception code.

Place the project ROS packages inside `~/catkin_ws/src/`.

## Running the Project

### 1. Build and launch the simulation

Open the first terminal:

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
roslaunch panda_moveit demo_gazebo.launch
```

### 2. Start the camera and detection node

Open a second terminal:

```bash
cd ~/catkin_ws
source devel/setup.bash
rosrun panda_moveit camera.py
```

### 3. Start the manipulation node

Open a third terminal:

```bash
cd ~/catkin_ws
source devel/setup.bash
rosrun panda_moveit pub.py
```

These commands assume the package is named `panda_moveit` and contains the launch file and scripts shown above.

## Evaluation

The project was evaluated in a controlled Gazebo environment using four cubic boxes.

The simulation demonstrated integration of object detection, motion planning, and robotic manipulation. Most operations successfully grasped and transported boxes to the target area.

Observed limitations included:

- Occasional off-centre grasps.
- Box slippage during transport.
- Placement deviations.
- Inconsistent placement of one box in some four-box runs.

These results relate to simulation testing; the system has not been validated on physical robotic hardware.

## Future Improvements

- Depth sensing for improved 3D object localisation.
- Adaptive grasp planning and grip-force control.
- Automatic recovery after failed grasps.
- Improved handling of clutter and overlapping objects.
- Testing on a physical robotic arm.
