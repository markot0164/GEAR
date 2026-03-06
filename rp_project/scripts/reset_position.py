#!/usr/bin/python3
import rospy
from rp_project.srv import ResetPosition, ResetPositionResponse
from visualization_msgs.msg import Marker

"""
ROS service server that resets the sphere position by publishing
a Marker with the initial coordinates.
"""

reset_position_pub = None

# Service callback: publish the initial position of the sphere
def handle_reset_position(req):
    global reset_position_pub
    rospy.loginfo("Resetting position to initial coordinates.")

    reset_marker = Marker()
    reset_marker.header.frame_id = "world"
    reset_marker.header.stamp = rospy.Time.now()
    reset_marker.ns = "reset"
    reset_marker.id = 0
    reset_marker.type = Marker.SPHERE
    reset_marker.action = Marker.ADD

    reset_marker.pose.position.x = 8.5
    reset_marker.pose.position.y = -8.5
    reset_marker.pose.position.z = 0.1

    reset_position_pub.publish(reset_marker)
    
    return ResetPositionResponse(success=True)

if __name__ == "__main__":
    rospy.init_node("reset_position_server")
    reset_position_pub = rospy.Publisher("/reset_position", Marker, queue_size=10)
    service = rospy.Service("reset_position", ResetPosition, handle_reset_position)
    rospy.loginfo("Service 'reset_position' is ready.")
    rospy.spin()