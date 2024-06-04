import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
bridge = CvBridge()

class CameraNode(Node):

    def __init__(self):
        super().__init__('get_camera')
        self.publisher = self.create_publisher(Image, 'camera', 10)
        timer_period = 0.066
        self.timer = self.create_timer(timer_period, self.get_cam_frame)
        self.i = 0

    def get_cam_frame(self):
        vid = cv2.VideoCapture(0)               # Get CV2 video stream as vid
        ret, frame = vid.read()                      # Get frame
        cv2.imshow('frame', frame)              # Show frame on screen
        if cv2.waitKey(1) & 0xFF == ord('q'):   # If q is pressed, quit
            vid.release()
            cv2.destroyAllWindows()
            rclpy.shutdown()
        image_message = bridge.cv2_to_imgmsg(frame, encoding="passthrough") # Convert for image message
        try:
            self.publisher.publish(image_message) # Publish image
            self.get_logger().info('Publishing image')
        except Exception as e:
            print(e)

def main(args=None):
    rclpy.init(args=args) # ROS Stuff
    node = CameraNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
