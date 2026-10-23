
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool


class AltitudePublisher(Node):
    def __init__(self):
        super().__init__('altitude_publisher')

        # Publish the drone's altitude
        self.publisher_ = self.create_publisher(
            Float32, '/drone/altitude', 10
        )

        # Listen for landing commands
        self.subscription = self.create_subscription(
            Bool,
            '/drone/landing_command',
            self.landing_callback,
            10
        )

        # Starting altitude and landing state
        self.altitude = 10.0
        self.landing_requested = False

        # Run the altitude update every second
        self.timer = self.create_timer(
            1.0, self.publish_altitude
        )

        self.get_logger().info(
            'Drone hovering at 10 meters. Waiting for landing command.'
        )

    def landing_callback(self, msg):
        if msg.data and not self.landing_requested:
            self.landing_requested = True
            self.get_logger().info('Landing command received!')

    def publish_altitude(self):
        msg = Float32()
        msg.data = self.altitude

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Drone altitude: {self.altitude:.1f} meters'
        )

        # Only descend after receiving permission
        if self.landing_requested:
            if self.altitude > 0:
                self.altitude = max(0.0, self.altitude - 0.5)
            else:
                self.get_logger().info('Drone has landed!')
                self.timer.cancel()


def main(args=None):
    rclpy.init(args=args)
    node = AltitudePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
