import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String

from drone_landing.decision_logic import (
    landing_decision,
    update_state
)


class LandingNode(Node):

    def __init__(self):
        super().__init__("landing_node")

        self.state = "LANDING"

        self.subscription = self.create_subscription(
            Float32MultiArray,
            "/drone/landing_inputs",
            self.process_inputs,
            10
        )

        self.publisher = self.create_publisher(
            String,
            "/drone/landing_decision",
            10
        )

        self.get_logger().info("Landing node started")

    def process_inputs(self, msg):

        if len(msg.data) != 6:
            self.get_logger().warning("Invalid landing inputs")
            return

        marker_detected = bool(msg.data[0])
        marker_displacement = msg.data[1]
        altitude = msg.data[2]
        descent_velocity = msg.data[3]
        recovery_complete = bool(msg.data[4])
        landed = bool(msg.data[5])

        decision = landing_decision(
            marker_detected,
            marker_displacement,
            altitude,
            descent_velocity,
            self.state,
            recovery_complete,
            landed
        )

        previous_state = self.state

        self.state = update_state(
            self.state,
            decision
        )

        output = String()
        output.data = decision

        self.publisher.publish(output)

        self.get_logger().info(
            f"Previous state: {previous_state} | "
            f"Decision: {decision} | "
            f"New state: {self.state}"
        )


def main(args=None):
    rclpy.init(args=args)

    node = LandingNode()

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
