# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from time import time
import numpy as np
import matplotlib.pyplot as plt

# from std_msgs.msg import time
from std_msgs.msg import Float64


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Float64,
            'topic',
            self.listener_callback,
            10)
        self.subscription 
        self.latency_list=np.array([]) # prevent unused variable warning

    def listener_callback(self, msg):
        receive_time = time()
        send_time = msg.data
        latency = (receive_time - send_time)*10**6
        self.get_logger().info('Received: %.15f (Latency: %.6f micro seconds)' % (send_time, latency))
        self.latency_list=np.append(self.latency_list,latency)
        # self.get_logger().info('Published: %.15f' % receive_time)
        if len(self.latency_list) == 120:
            self.plot_graph(self.latency_list)

    def plot_graph(self,latency:np.array):
        plt.style.use("ggplot")
        plt.plot(latency)
        plt.xlabel("Number of messages received")
        plt.ylabel("latency in µs")
        plt.title("Latency for communication on same device")
        plt.savefig("/home/jayanth/latency/plot/graph.png")

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
