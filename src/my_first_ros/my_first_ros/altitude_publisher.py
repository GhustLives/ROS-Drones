import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class AltitudePublisher(Node):
    def __init__(self):
        super().__init__('altitude_publisher')

        self.publisher_ = self.create_publisher(
            Float32, '/drone/altitude', 10
        )

        self.altitude = 10.0

        self.timer = self.create_timer(
            1.0, self.publish_altitude
        )

    def publish_altitude(self):
        msg = Float32()
        msg.data = self.altitude

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Drone altitude: {self.altitude:.1f} meters'
        )

        if self.altitude > 0:
            self.altitude = max(0.0, self.altitude - 0.5)
        else:
            self.get_logger().info("Drone has landed!")
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
