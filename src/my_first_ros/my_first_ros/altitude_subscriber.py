
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class AltitudeSubscriber(Node):
    def __init__(self):
        super().__init__('altitude_subscriber')

        self.subscription = self.create_subscription(
            Float32,
            '/drone/altitude',
            self.altitude_callback,
            10
        )

    def altitude_callback(self, msg):
        altitude = msg.data

        self.get_logger().info(
            f'Received altitude: {altitude:.1f} meters'
        )

        if altitude == 0.0:
            self.get_logger().info('Landing confirmed!')
        elif altitude <= 2.0:
            self.get_logger().info('Drone approaching landing platform.')


def main(args=None):
    rclpy.init(args=args)

    node = AltitudeSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
