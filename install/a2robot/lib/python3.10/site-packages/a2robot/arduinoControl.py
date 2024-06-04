import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class arduinoControl(Node):

    def __init__(self):
        super().__init__('arduino_control')
        self.subscription = self.create_subscription(String, 'arduino_command', self.send_command_to_arduino, 10)
        self.serial_port = serial.Serial('/dev/ttyACM0', 9600)  # Change the port accordingly

    def send_command_to_arduino(self, msg):
        print("Recieved ", msg.data)
        
        match msg.data:
            case "go right":
                self.serial_port.write(b'0')  # Sending '0' to turn on right LED
                self.serial_port.write(b'q')  # Sending 'q' to turn on left motor
                self.get_logger().info("Sent 'lm1' command to Arduino")
            case "go left":
                self.serial_port.write(b'1')  # Sending '1' to turn on left LED
                self.serial_port.write(b'a')  # Sending 'a' to turn on right motor
                self.get_logger().info("Sent 'rm1' command to Arduino")
            case "mo":
                self.serial_port.write(b't')  # Sending 't' to turn all motors off
                self.get_logger().info("Sent 'mo' command to Arduino")
            case _:
                self.get_logger().warn("Invalid command recieved.")          

def main(args=None):
    rclpy.init(args=args)
    arduino_control = arduinoControl()
    rclpy.spin(arduino_control)
    arduino_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
