import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from px4_msgs.msg import VehicleLocalPosition
from px4_msgs.msg import VehicleLandDetected


class TelemetryNode(Node):

    def __init__(self):
        super().__init__("telemetry_node")

        self.local_position = None
        self.landed = None

        self.position_subscription = self.create_subscription(
            VehicleLocalPosition,
            "/fmu/out/vehicle_local_position_v1",
            self.position_callback,
            qos_profile_sensor_data
        )

        self.landing_subscription = self.create_subscription(
            VehicleLandDetected,
            "/fmu/out/vehicle_land_detected",
            self.landing_callback,
            qos_profile_sensor_data
        )

        self.timer = self.create_timer(
            1.0,
            self.display_telemetry
        )

        self.get_logger().info("Telemetry node started")

    def position_callback(self, msg):
        self.local_position = msg

    def landing_callback(self, msg):
        self.landed = msg.landed

    def display_telemetry(self):

        if self.local_position is None or self.landed is None:
            self.get_logger().info("Waiting for PX4 telemetry")
            return

        position = self.local_position

        if not position.z_valid or not position.v_z_valid:
            self.get_logger().warning("Invalid vertical telemetry")
            return

        local_height = -position.z
        descent_velocity = max(0.0, position.vz)

        self.get_logger().info(
            f"Local height: {local_height:.2f} m | "
            f"Descent velocity: {descent_velocity:.2f} m/s | "
            f"Landed: {self.landed} | "
            f"Range valid: {position.dist_bottom_valid}"
        )


def main(args=None):
    rclpy.init(args=args)

    node = TelemetryNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
