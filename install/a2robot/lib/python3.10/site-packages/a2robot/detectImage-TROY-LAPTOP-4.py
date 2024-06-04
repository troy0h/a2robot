import rclpy
from rclpy.node import Node
import cv2
from PIL import Image, ImageOps
from sensor_msgs.msg import Image as Im
from std_msgs.msg import String
from cv_bridge import CvBridge
bridge = CvBridge()

import tensorflow  as tf
from tensorflow.keras.models import Sequential
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
        #image = ImageOps.fit(cv_image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array

        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        left = prediction[0,1]
        right = prediction[0,2]
        stop = prediction[0,3]
        predMax = max(left, right, stop)

        print(class_name, confidence_score) # 0 = none, 1 = left, 2 = right, 3 = stop

        if predMax == left:
            msg = String().data = "on left"
            msg2 = String().data = "go left"
            self.publisher.publish(msg)
            self.publisher.publish(msg2)
            self.get_logger().info('Publishing left')

        elif predMax == right:
            msg = String().data = "on right"
            msg2 = String().data = "go right"
            self.publisher.publish(msg)
            self.publisher.publish(msg2)
            self.get_logger().info('Publishing right')

        elif predMax == stop:
            msg = String().data = "mo"
            self.publisher.publish("mo") # Motors off, nothing detected
            self.get_logger().info('Publishing motor off')

        else:
            self.get_logger()

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