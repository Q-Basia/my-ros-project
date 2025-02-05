#!/usr/bin/env python3

import os
import rospy
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage

import cv2
from cv_bridge import CvBridge


class CameraProcessorNode(DTROS):

    def __init__(self, node_name):
        # Initialize the DTROS parent class
        super(CameraProcessorNode, self).__init__(node_name=node_name, node_type=NodeType.VISUALIZATION)
        # Get the vehicle name
        self._vehicle_name = os.environ.get('VEHICLE_NAME', 'default_robot')
        # Define the camera topic and output topic
        self._camera_topic = f"/{self._vehicle_name}/camera_node/image/compressed"
        self._output_topic = f"/{self._vehicle_name}/camera/image_processed"
        # Bridge between OpenCV and ROS
        self._bridge = CvBridge()
        # Set up subscriber and publisher
        self.sub = rospy.Subscriber(self._camera_topic, CompressedImage, self.callback)
        self.pub = rospy.Publisher(self._output_topic, CompressedImage, queue_size=10)

    def callback(self, msg):
        try:
            # Convert compressed image message to OpenCV image
            image = self._bridge.compressed_imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Get image dimensions
            height, width = image.shape[:2]

            # Convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Add annotation text
            text = f"{self._vehicle_name} says, 'Cheese! Capturing {width}x{height} - quack-tastic!'"
            position = (10, height - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(gray_image, text, position, font, 0.5, (255, 255, 255), 1)

            # Convert the annotated image back to a compressed message
            annotated_msg = self._bridge.cv2_to_compressed_imgmsg(gray_image)

            # Publish the processed image
            self.pub.publish(annotated_msg)

        except Exception as e:
            rospy.logerr(f"Error processing image: {e}")

if __name__ == '__main__':
    # Create the node
    node = CameraProcessorNode(node_name='camera_processor_node')
    # Keep the node running
    rospy.spin()


