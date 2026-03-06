#!/usr/bin/python3
import math
import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Twist
from rp_project.msg import Collision

"""
This node controls the sphere motion in RViz.
It updates the sphere position based on velocity commands,
publishes its position, and handles collisions and reset events.
"""

class RVizController:
    def __init__(self):
        rospy.init_node("rviz_controller", anonymous=True)
    
        #Pub/Sub
        self.marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size=10)
        self.position_pub = rospy.Publisher("/ball_position", Marker, queue_size=10)
        self.sub = rospy.Subscriber("/cmd_vel", Twist, self.update_position)

        self.cone_sub = rospy.Subscriber("/rotating_cones_positions", Marker, self.update_cone_positions)
        self.collision_sub = rospy.Subscriber("/collision_event", Collision, self.collision_callback)
        self.reset_sub = rospy.Subscriber("/reset_position", Marker, self.reset_position_callback)

        self.shutdown_sub = rospy.Subscriber("/shutdown", Marker, self.shutdown_callback)
        self.rate = rospy.Rate(10)

        # Sphere movement speed (can be changed at runtime via rosparam)
        self.speed = rospy.get_param('/rviz_controller/speed', 0.1) #rosparam /rviz_controller/speed

        self.position = [8.5, -8.5] 
        self.cone_positions = []

    # generate sphere in RViz
    def create_marker(self):
        marker = Marker()
        marker.header.frame_id = "world"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "moving_ball"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        marker.pose.position.x = self.position[0]
        marker.pose.position.y = self.position[1]
        marker.pose.position.z = 0.5

        marker.scale.x = 1.0
        marker.scale.y = 1.0
        marker.scale.z = 1.0

        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        return marker

    # Update sphere position based on velocity commands
    def update_position(self, twist_msg):
        self.position[0] += twist_msg.linear.x * self.speed
        self.position[1] += twist_msg.linear.y * self.speed

        self.position[0] = max(-10.0, min(10.0, self.position[0]))
        self.position[1] = max(-10.0, min(10.0, self.position[1]))

        rospy.loginfo(f"Updated position: x={self.position[0]}, y={self.position[1]}")

    # Receive updated camera cone positions
    def update_cone_positions(self, marker_msg):
        self.cone_positions = []
        for point in marker_msg.points:
            self.cone_positions.append((point.x, point.y))

    # Callback triggered when a collision is detected
    def collision_callback(self, collision_msg):
        rospy.logwarn(f"Collision detected! Message: {collision_msg.message}, Position: ({collision_msg.x}, {collision_msg.y})")

    # Reset sphere position after collision
    def reset_position_callback(self, marker_msg):
        self.position[0] = marker_msg.pose.position.x
        self.position[1] = marker_msg.pose.position.y

    # Main loop: publish sphere marker and position
    def run(self):
        while not rospy.is_shutdown():
            self.speed = rospy.get_param('/rviz_controller/speed', 0.1)
            marker = self.create_marker()
            self.marker_pub.publish(marker)
            self.position_pub.publish(marker)
            self.rate.sleep()

    #shutdown message for the node
    def shutdown_callback(self, msg):
        rospy.loginfo("Shutdown signal received. Stopping node.")
        rospy.signal_shutdown("Shutdown signal received")

if __name__ == "__main__":
    try:
        controller = RVizController()
        controller.run()
    except rospy.ROSInterruptException:
        pass