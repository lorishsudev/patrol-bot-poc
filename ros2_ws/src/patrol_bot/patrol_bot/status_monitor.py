"""Log the battery level, warning when it runs low."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float32

LOW_BATTERY_THRESHOLD = 20.0


class StatusMonitor(Node):
    """Subscribe to /patrol/battery and log each reading."""

    def __init__(self):
        super().__init__('status_monitor')
        self.subscription = self.create_subscription(
            Float32, '/patrol/battery', self.on_battery, 10)

    def on_battery(self, msg):
        """Log the battery level, using warn below the threshold."""
        if msg.data < LOW_BATTERY_THRESHOLD:
            self.get_logger().warn(f'Battery low: {msg.data:.1f}')
        else:
            self.get_logger().info(f'Battery: {msg.data:.1f}')


def main(args=None):
    """Run the status monitor node."""
    rclpy.init(args=args)
    node = StatusMonitor()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
