
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from std_msgs.msg import Bool


class LandingController(Node):
    def __init__(self):
        super().__init__('landing_controller')

        # Track whether landing has been requested
        self.landing_requested = False

        # Publish landing commands to other nodes
        self.command_publisher = self.create_publisher(
            Bool,
            '/drone/landing_command',
            10
        )

        # Create a service to receive landing requests
        self.service = self.create_service(
            Trigger,
            '/drone/start_landing',
            self.landing_callback
        )

        self.get_logger().info('Landing controller ready.')

    def landing_callback(self, request, response):
        # Record the landing request
        self.landing_requested = True

        # Create and publish the landing command
        command = Bool()
        command.data = True
        self.command_publisher.publish(command)

        # Respond to the service client
        response.success = True
        response.message = 'Landing command accepted.'

        self.get_logger().info('Landing requested!')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = LandingController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
