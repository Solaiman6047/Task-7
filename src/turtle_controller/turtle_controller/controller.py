import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios


class Controller(Node):

    def __init__(self):
        super().__init__('controller')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.get_logger().info('Controller started!')
        self.get_logger().info('Use W/A/S/D to move the turtle.')

    def get_key(self):
        settings = termios.tcgetattr(sys.stdin)

        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

        return key

    def move_turtle(self, key):

        msg = Twist()

        if key == 'w':
            msg.linear.x = 2.0

        elif key == 's':
            msg.linear.x = -2.0

        elif key == 'a':
            msg.angular.z = 2.0

        elif key == 'd':
            msg.angular.z = -2.0

        else:
            return

        self.publisher.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = Controller()

    while rclpy.ok():

        key = node.get_key()

        if key == 'q':
            break

        node.move_turtle(key)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()