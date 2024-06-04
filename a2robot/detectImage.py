import rclpy
from rclpy.node import Node
import cv2
import time
from sensor_msgs.msg import Image as Im
from std_msgs.msg import String
from cv_bridge import CvBridge
bridge = CvBridge()

import tensorflow  as tf
import numpy as np

model = tf.keras.models.load_model("resource/keras_model.h5")
class_names = open("resource/labels.txt", "r").readlines()

class DetectImage(Node):

    def __init__(self):
        super().__init__('rec_camera')
        self.subscription = self.create_subscription(Im, 'camera', self.camera_image_ai, 10)
        self.publisher = self.create_publisher(String, 'arduino_command', 10)

    def camera_image_ai(self, msg):
        cv_image = bridge.imgmsg_to_cv2(msg) # Convert for image message

        # Screw with the image to fit
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = cv2.resize(cv_image, (224, 224)) 
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array

        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        none = prediction[0,0]
        left = prediction[0,1]
        right = prediction[0,2]
        stop = prediction[0,3]

        predMax = max(none, left, right, stop)

        if predMax == left and confidence_score > 0.6:
            msg = String()
            msg.data = "go left"
            self.publisher.publish(msg)
            self.get_logger().info('Publishing left')

        elif predMax == right and confidence_score > 0.6:
            msg = String()
            msg.data = "go right"
            self.publisher.publish(msg)
            self.get_logger().info('Publishing right')

        elif predMax == stop and confidence_score > 0.6:
            msg = String()
            msg.data = "mo"
            self.publisher.publish(msg)
            self.get_logger().info('Publishing motor off')

        else:
            self.get_logger().info('Nothing detected')

    def send_arduino_command(self, command):
        command

def main(args=None):
    rclpy.init(args=args)
    detect_image = DetectImage()
    rclpy.spin(detect_image)
    detect_image.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()




