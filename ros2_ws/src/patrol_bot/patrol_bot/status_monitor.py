"""Log the battery level, requesting a recharge when it runs low."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger


class StatusMonitor(Node):
    """Subscribe to /patrol/battery and call /patrol/recharge when low."""

    def __init__(self):
        super().__init__('status_monitor')
        self.declare_parameter('low_threshold', 30.0)
        self.subscription = self.create_subscription(
            Float32, '/patrol/battery', self.on_battery, 10)
        self.recharge_client = self.create_client(Trigger, '/patrol/recharge')
        self.recharge_pending = False

    def on_battery(self, msg):
        """Log the battery level and request a recharge below the threshold."""
        threshold = self.get_parameter('low_threshold').value
        if msg.data >= threshold:
            self.get_logger().info(f'Battery: {msg.data:.1f}')
            return
        self.get_logger().warn(f'Battery low: {msg.data:.1f}')
        if self.recharge_pending:
            return
        if not self.recharge_client.service_is_ready():
            self.get_logger().warn('/patrol/recharge not available')
            return
        self.recharge_pending = True
        future = self.recharge_client.call_async(Trigger.Request())
        future.add_done_callback(self.on_recharge_response)

    def on_recharge_response(self, future):
        """Log the recharge result and allow the next request."""
        self.recharge_pending = False
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error(f'Recharge call failed: {e}')
            return
        self.get_logger().info(response.message)


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
