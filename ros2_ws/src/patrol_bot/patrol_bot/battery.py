"""Simulate a draining battery with a recharge service."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger

FULL_LEVEL = 100.0
DRAIN_PER_SECOND = 1.0


class Battery(Node):
    """Publish the battery level on /patrol/battery and serve /patrol/recharge."""

    def __init__(self):
        super().__init__('battery')
        self.publisher = self.create_publisher(Float32, '/patrol/battery', 10)
        self.recharge_service = self.create_service(
            Trigger, '/patrol/recharge', self.handle_recharge)
        self.level = FULL_LEVEL
        self.timer = self.create_timer(1.0, self.publish_level)

    def publish_level(self):
        """Publish the current level, then drain it toward zero."""
        msg = Float32()
        msg.data = self.level
        self.publisher.publish(msg)
        self.level = max(0.0, self.level - DRAIN_PER_SECOND)

    def handle_recharge(self, request, response):
        """Reset the battery level to full."""
        previous = self.level
        self.level = FULL_LEVEL
        response.success = True
        response.message = f'Recharged from {previous:.1f} to {FULL_LEVEL:.1f}'
        self.get_logger().info(response.message)
        return response


def main(args=None):
    """Run the battery node."""
    rclpy.init(args=args)
    node = Battery()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
