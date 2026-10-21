"""Publish a periodic heartbeat with the hostname and a counter."""

import socket

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class Heartbeat(Node):
    """Publish a String on /patrol/heartbeat once per second."""

    def __init__(self):
        super().__init__('heartbeat')
        self.publisher = self.create_publisher(String, '/patrol/heartbeat', 10)
        self.hostname = socket.gethostname()
        self.count = 0
        self.timer = self.create_timer(1.0, self.publish_heartbeat)

    def publish_heartbeat(self):
        """Publish one heartbeat message."""
        msg = String()
        msg.data = f'{self.hostname} {self.count}'
        self.publisher.publish(msg)
        self.count += 1


def main(args=None):
    """Run the heartbeat node."""
    rclpy.init(args=args)
    node = Heartbeat()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
