#!/usr/bin/env python3





import rospy
import tf
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from geometry_msgs.msg import TransformStamped
from tf.transformations import quaternion_from_euler
from std_msgs.msg import String
from ultralytics import YOLO
import rospkg
import os
# get the YOLO model path from the packiage
rospack = rospkg.RosPack()
package_path = rospack.get_path('panda_moveit')
model_path = os.path.join(package_path, 'script', 'best.pt')

model = YOLO(model_path)
class CameraSubscriber:
    def __init__(self):
        self.bridge = CvBridge()
        # self.model = YOLO('/home/ubunut20/catkin_ws/src/panda/panda_moveit/script/best.pt')

        rospy.init_node('camera_visualizer', anonymous=True)
        rospy.Subscriber('/rrbot/camera1/image_raw', Image, self.image_callback)

        # Transform broadcaster
        self.broadcaster = tf.TransformBroadcaster()

        # Camera intrinsics (replace these with your actual camera params)
        self.fx = 1231.4642020509286
        self.fy = 1231.4642020509286
        self.cx = 400.5
        self.cy = 400.5

        # Fixed depth for now (replace with actual depth data if available)
        self.fixed_depth = 1.15

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            # print(cv_image.shape)
            cv_image= cv_image[ 100: 700  , 100:650 , : ]
            result1 = model(cv_image , conf= 0.8)

            boxes = result1[0].boxes.xyxy.cpu().numpy()

            # Draw boxes, centers, labels and publish TF
            for idx, box in enumerate(boxes):
                x1, y1, x2, y2 = box
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                # center_x= center_x + 100

                # Draw rectangle and center point
                cv2.rectangle(cv_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(cv_image, (center_x, center_y), 5, (255, 0, 0), -1)
                cv2.putText(cv_image, str(idx+1), (center_x+5, center_y-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

                # Print center in image coords
                print(f"Object {idx+1}: Center = ({center_x}, {center_y})")

                # Compute 3D position (in camera frame)
                depth = self.fixed_depth
                u = center_x + 100
                v = center_y + 100

                x_3d = depth
                y_3d = -((u - self.cx) * depth / self.fx)
                z_3d = -((v - self.cy) * depth / self.fy)

                print(f"Object {idx+1}: 3D position = ({x_3d:.3f}, {y_3d:.3f}, {z_3d:.3f})")

                # Identity quaternion (no rotation)
                q = quaternion_from_euler(0, 0, 0)

                # Publish transform
                object_name = f"detected_object_{idx+1}"
                self.broadcaster.sendTransform(
                    (x_3d, y_3d, z_3d),
                    q,
                    rospy.Time.now(),
                    object_name,
                    "camera_link"
                )

            # Display image
            cv2.imshow("Gazebo Camera - Processed", result1[0].plot())
            cv2.waitKey(1)

        except Exception as e:
            rospy.logerr(f"Error in image callback: {e}")

def main():
    camera_subscriber = CameraSubscriber()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()





# int ssrPin1 = 7;  // SSR Channel 1 control pin
# int ssrPin2 = 8;  // SSR Channel 2 control pin

# void setup() {
#   pinMode(ssrPin1, OUTPUT);
#   pinMode(ssrPin2, OUTPUT);
# }

# void loop() {
#   // Turn both SSRs ON
#   digitalWrite(ssrPin1, HIGH);
#   digitalWrite(ssrPin2, HIGH);
#   # delay(1000); // 1 second delay

#   // Turn both SSRs OFF
#   digitalWrite(ssrPin1, LOW);
#   digitalWrite(ssrPin2, LOW);
#   # delay(1000); // 1 second delay
# }























# import rospy
# import tf
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import cv2
# import numpy as np
# from geometry_msgs.msg import Point, TransformStamped
# from tf.transformations import quaternion_from_euler
# from std_msgs.msg import String  # Import the String message type


# class CameraSubscriber:
#     def __init__(self):
#         self.bridge = CvBridge()
#         rospy.init_node('camera_visualizer', anonymous=True)
#         rospy.Subscriber('/rrbot/camera1/image_raw', Image, self.image_callback)
        
#         # Initialize transform broadcaster
#         self.broadcaster = tf.TransformBroadcaster()

#         # Initialize publisher for detected object class
#         self.object_class_publisher = rospy.Publisher('/detected_object_class', String, queue_size=10)


#     def image_callback(self, msg):
#         try:
#             # Convert the ROS image message to an OpenCV image
#             cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

#             # Convert the image to HSV color space
#             hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

#             # Define color ranges for red and yellow in HSV
#             # Red color range (adjust as needed)
#             lower_red1 = np.array([0, 120, 70])
#             upper_red1 = np.array([10, 255, 255])
#             lower_red2 = np.array([170, 120, 70])
#             upper_red2 = np.array([180, 255, 255])

#             # Yellow color range (adjust as needed)
#             lower_yellow = np.array([20, 100, 100])
#             upper_yellow = np.array([30, 255, 255])

#             # Create masks for red and yellow
#             mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
#             mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
#             mask_red = cv2.bitwise_or(mask_red1, mask_red2)
#             mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

#             # Find contours for red and yellow objects
#             contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#             detected_objects = []

#             # Process red objects (strawberries)
#             for contour in contours_red:
#                 # Calculate the bounding box for the red object
#                 x, y, w, h = cv2.boundingRect(contour)
#                 if w > 10 and h > 10:  # Ignore small contours
#                     detected_objects.append(('strawberry', (x, y, w, h)))

#             # Process yellow objects (bananas)
#             for contour in contours_yellow:
#                 # Calculate the bounding box for the yellow object
#                 x, y, w, h = cv2.boundingRect(contour)
#                 if w > 10 and h > 10:  # Ignore small contours
#                     detected_objects.append(('banana', (x, y, w, h)))

#             # Sort the detected objects by the highest y-coordinate (from top to bottom)
#             detected_objects.sort(key=lambda obj: obj[1][1], reverse=True)

#             # Publish the class of the first detected object
#             if detected_objects:
#                 first_object_label = detected_objects[0][0]
#                 self.object_class_publisher.publish(first_object_label)
#                 rospy.loginfo(f"Published class of the first detected object: {first_object_label}")
#             else:
#                 rospy.loginfo("No objects detected.")

#             # Publish transforms for all detected objects
#             for idx, (label, (x, y, w, h)) in enumerate(detected_objects):
#                 # Calculate 3D coordinates from the pixel values (x, y, and depth)
#                 depth = 1.036  # You should replace this with the actual depth
#                 fx = 1231.4642020509286
#                 fy = 1231.4642020509286
#                 cx = 400.5
#                 cy = 400.5

#                 object_center_u = x + w // 2
#                 object_center_v = y + h // 2

#                 x_3d = depth
#                 y_3d = -((object_center_u - cx) * depth / fx)
#                 z_3d = -((object_center_v - cy) * depth / fy)

#                 # Create a transform for each detected object
#                 translation = (x_3d, y_3d, z_3d)
#                 rotation = quaternion_from_euler(0, 0, 0)  # Identity rotation (no rotation)

#                 # Send the transform
#                 object_name = f"detected_object_{idx}" if idx > 0 else "detected_object"
#                 self.broadcaster.sendTransform(
#                     translation,
#                     rotation,
#                     rospy.Time.now(),
#                     object_name,
#                     "camera_link"
#                 )

#                 # Draw bounding box and label on the image
#                 if label == 'strawberry':
#                     color = (0, 0, 255)  # Red for strawberry
#                 elif label == 'banana':
#                     color = (0, 255, 255)  # Yellow for banana
                
#                 # Draw the rectangle (bounding box) around the object
#                 cv2.rectangle(cv_image, (x, y), (x + w, y + h), color, 2)
#                 cv2.putText(cv_image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

#                 rospy.loginfo(f"{object_name}: {label} at 3D Coordinates -> x={x_3d}, y={y_3d}, z={z_3d}")

#             # Display the processed image
#             cv2.imshow("Gazebo Camera - Processed", cv_image)
#             cv2.waitKey(1)

#         except Exception as e:
#             rospy.logerr(f"Error in image callback: {e}")


# def main():
#     camera_subscriber = CameraSubscriber()
#     try:
#         rospy.spin()
#     except KeyboardInterrupt:
#         print("Shutting down")
#     cv2.destroyAllWindows()


# if __name__ == '__main__':
#     main()









# working model 
# import rospy
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import cv2
# import numpy as np
# from geometry_msgs.msg import Point

# class CameraSubscriber:
#     def __init__(self):
#         self.bridge = CvBridge()
#         rospy.init_node('camera_visualizer', anonymous=True)
#         rospy.Subscriber('/rrbot/camera1/image_raw', Image, self.image_callback)

#     def image_callback(self, msg):
#         try:
#             # Convert the ROS image message to an OpenCV image
#             cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

#             # Convert the image to HSV color space
#             hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

#             # Define color ranges for red and yellow in HSV
#             # Red color range (adjust as needed)
#             lower_red1 = np.array([0, 120, 70])
#             upper_red1 = np.array([10, 255, 255])
#             lower_red2 = np.array([170, 120, 70])
#             upper_red2 = np.array([180, 255, 255])

#             # Yellow color range (adjust as needed)
#             lower_yellow = np.array([20, 100, 100])
#             upper_yellow = np.array([30, 255, 255])

#             # Create masks for red and yellow
#             mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
#             mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
#             mask_red = cv2.bitwise_or(mask_red1, mask_red2)
#             mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

#             # Find contours for red and yellow objects
#             contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#             # Process red objects (spheres) - Strawberry
#             for contour in contours_red:
#                 # Calculate the minimum enclosing circle (useful for spheres)
#                 ((x, y), radius) = cv2.minEnclosingCircle(contour)
#                 center = (int(x), int(y))

#                 # Only consider significant contours based on radius
#                 if radius > 10:
#                     # Draw the circle and its center
#                     # cv2.circle(cv_image, center, int(radius), (0, 0, 255), 2)
#                     cv2.circle(cv_image, center, 5, (0, 255, 255), -1)

#                     # Draw bounding box around the red sphere
#                     x, y, w, h = cv2.boundingRect(contour)
#                     cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
#                     cv2.putText(cv_image, "Strawberry", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
#                     print(f"Red Sphere Center: {center}, Radius: {radius}")

#             # Process yellow objects (squares) - Banana
#             for contour in contours_yellow:
#                 # Approximate the contour to find the shape
#                 epsilon = 0.04 * cv2.arcLength(contour, True)
#                 approx = cv2.approxPolyDP(contour, epsilon, True)

#                 # Check if the shape is a square (4 sides)
#                 if len(approx) == 4:
#                     # Calculate the center of the square
#                     M = cv2.moments(contour)
#                     if M["m00"] > 0:
#                         cx = int(M["m10"] / M["m00"])
#                         cy = int(M["m01"] / M["m00"])
#                         center = (cx, cy)

#                         # Draw the contour and its center
#                         # cv2.drawContours(cv_image, [contour], -1, (0, 255, 255), 2)
#                         cv2.circle(cv_image, center, 5, (255, 0, 0), -1)

#                         # Draw bounding box around the yellow square
#                         x, y, w, h = cv2.boundingRect(contour)
#                         cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 255), 2)
#                         cv2.putText(cv_image, "Banana", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
#                         print(f"Yellow Square Center: {center}")

#             # Display the processed image
#             cv2.imshow("Gazebo Camera - Processed", cv_image)
#             cv2.waitKey(1)

#         except Exception as e:
#             print(e)

# def main():
#     camera_subscriber = CameraSubscriber()
#     try:
#         rospy.spin()
#     except KeyboardInterrupt:
#         print("Shutting down")
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()








# import rospy
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import cv2
# import numpy as np
# from geometry_msgs.msg import Point
# import os
# # print("ROS_MASTER_URI =", os.environ.get("ROS_MASTER_URI"))t

# class CameraSubscriber:
#     def __init__(self):
#         self.bridge = CvBridge()
#         rospy.init_node('camera_visualizer', anonymous=True)
#         rospy.Subscriber('/rrbot/camera1/image_raw', Image, self.image_callback)


#     def image_callback(self, msg):
#         try:
#             cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

#             # cv2.imwrite("dental_image2.jpg", cv_image)
#             cv2.imshow("Gazebo Camera", cv_image)
#             cv2.waitKey(1)  # Adjust the delay as needed
#         except Exception as e:
#             print(e)

# def main():
#     camera_subscriber = CameraSubscriber()
#     try:
#         rospy.spin()
#     except KeyboardInterrupt:
#         print("Shutting down")
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()







