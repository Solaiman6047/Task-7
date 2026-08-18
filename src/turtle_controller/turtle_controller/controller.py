import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Color
from std_msgs.msg import String
import sys
import tty
import termios
import select


class Controller(Node):

    def __init__(self):
        super().__init__('controller')

        self.color_sub = self.create_subscription(
            Color, 
            "/turtle1/color_sensor", 
            self.perception,
            10)

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )
        self.color_publisher = self.create_publisher(
            String,
            '/dominant_color',
            10
        )

        self.get_logger().info('Controller started!')
        self.get_logger().info('Use W/A/S/D to move the turtle.')

    def get_key(self):
        settings = termios.tcgetattr(sys.stdin)

        try:
            tty.setcbreak(sys.stdin.fileno())

            ready, _, _ = select.select([sys.stdin], [], [], 0.01)

            if ready:
                return sys.stdin.read(1)

            return None

        finally:
            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                settings
            )

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

    def perception(self, color: Color):
        c = {
            color.r:"Red",
            color.b:"Blue",
            color.g : "Green"
        }
        major_color = c[max(c)]
        self.get_logger().info(f"Major color: {major_color}")

        msg = String()
        msg.data = major_color

        self.color_publisher.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = Controller()

    while rclpy.ok():

        rclpy.spin_once(node, timeout_sec=0)

        key = node.get_key()

        if key == 'q':
            break

        if key is not None:
            node.move_turtle(key)

        node.move_turtle(key)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()