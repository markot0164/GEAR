#!/usr/bin/python3
import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import math

"""
This node creates the static environment in RViz and simulates
rotating camera fields of view using markers.
"""

class RVizMap:
    def __init__(self):
        rospy.init_node("rviz_map", anonymous=True)

        #Publisher
        self.marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size=10)
        self.cones_positions_pub = rospy.Publisher("/rotating_cones_positions", Marker, queue_size=10)

        #Subscriber
        self.shutdown_sub = rospy.Subscriber("/shutdown", Marker, self.shutdown_callback)

        self.rate = rospy.Rate(10)
        self.angle = 0.0

    # Generic helper function to create mesh markers in RViz
    def create_marker(self, x, y, z, x_orientation, y_orientation, z_orientation, w_orientation, scale_x, scale_y, scale_z, color, marker_id, mesh_path):
        marker = Marker()
        marker.header.frame_id = "world"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "map"
        marker.id = marker_id
        marker.type = Marker.MESH_RESOURCE
        marker.action = Marker.ADD

        offset_x = scale_x / 2
        offset_y = scale_y / 2
        marker.pose.position.x = x - offset_x
        marker.pose.position.y = y - offset_y
        marker.pose.position.z = z
        marker.pose.orientation.w = 1.0

        marker.scale.x = scale_x
        marker.scale.y = scale_y
        marker.scale.z = scale_z

        marker.pose.orientation.x = x_orientation
        marker.pose.orientation.y = y_orientation
        marker.pose.orientation.z = z_orientation
        marker.pose.orientation.w = w_orientation

        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.color.a = 1.0 

        marker.mesh_resource = f"package://rp_project/meshes/{mesh_path}"
        marker.mesh_use_embedded_materials = False

        return marker

    # Publish static objects: goal, cameras, obstacles
    def publish_objects(self):

        # Goal 
        goal_marker = Marker()
        goal_marker.header.frame_id = "world"
        goal_marker.header.stamp = rospy.Time.now()
        goal_marker.ns = "goal"
        goal_marker.id = 7
        goal_marker.type = Marker.CUBE
        goal_marker.action = Marker.ADD

        goal_marker.pose.position.x = -6.0
        goal_marker.pose.position.y = 6.0
        goal_marker.pose.position.z = 0.0 

        goal_marker.pose.orientation.x = 0.0
        goal_marker.pose.orientation.y = 0.0
        goal_marker.pose.orientation.z = 0.0
        goal_marker.pose.orientation.w = 1.0

        goal_marker.scale.x = 1.0
        goal_marker.scale.y = 1.0
        goal_marker.scale.z = 0.1 

        goal_marker.color.r = 0.0
        goal_marker.color.g = 0.0
        goal_marker.color.b = 1.0  
        goal_marker.color.a = 1.0

        self.marker_pub.publish(goal_marker)

        # Left camera
        cam_left = self.create_marker(-10.0, -3.0, 3.5, 1.5, 1.0, 0.8, 1.0, 0.5, 0.5, 0.3, (0.0, 0.0, 0.0), 1, "camera.dae")
        self.marker_pub.publish(cam_left)

        # Right camera                    
        cam_right = self.create_marker(10.0, 3.0, 3.5, 3.5, -2.5, -0.8, 3.0, 0.5, 0.5, 0.3, (0.0, 0.0, 0.0), 2, "camera.dae")
        self.marker_pub.publish(cam_right)

        # Cubes
        obstacle1 = self.create_marker(-8.0, -8.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, (0.5, 0.5, 0.5), 3, "cube.dae")
        obstacle2 = self.create_marker(-13.0, -13.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, (0.5, 0.5, 0.5), 4, "cube.dae")
        self.marker_pub.publish(obstacle1)
        self.marker_pub.publish(obstacle2)

    # Generate rotating camera cones and publish their positions
    def publish_rotating_cones(self):
        #left cone of view
        x_left = -13.0 + 2.0 * math.cos(self.angle)
        y_left = -13.0 + 2.0 * math.sin(self.angle)
        cone_left = self.create_marker(x_left, y_left, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.05, (1.0, 0.0, 0.0), 5, "cube.dae")
        self.marker_pub.publish(cone_left)

        #right cone of view
        x_right = -8.0 + 2.0 * math.cos(self.angle)
        y_right = -8.0 + 2.0 * math.sin(self.angle)
        cone_right = self.create_marker(x_right, y_right, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.05, (1.0, 0.0, 0.0), 6, "cube.dae")
        self.marker_pub.publish(cone_right)

        cone_positions = Marker()
        cone_positions.header.frame_id = "world"
        cone_positions.header.stamp = rospy.Time.now()
        cone_positions.ns = "rotating_cones"
        cone_positions.id = 10
        cone_positions.type = Marker.POINTS
        cone_positions.action = Marker.ADD

        cone_positions.color.r = 1.0
        cone_positions.color.g = 0.0
        cone_positions.color.b = 0.0
        cone_positions.color.a = 1.0

        cone_positions.scale.x = 0.1
        cone_positions.scale.y = 0.1

        point_left = Point()
        point_left.x = x_left
        point_left.y = y_left
        point_left.z = 0.0

        point_right = Point()
        point_right.x = x_right
        point_right.y = y_right
        point_right.z = 0.0

        cone_positions.points.append(point_left)
        cone_positions.points.append(point_right)

        self.cones_positions_pub.publish(cone_positions)

    def run(self):
        rospy.sleep(1) 
        self.publish_objects()

        while not rospy.is_shutdown():
            self.publish_rotating_cones()
            self.angle += 0.05 
            self.rate.sleep()
            
    # Stop the node when the goal is reached
    def shutdown_callback(self, msg):
        rospy.loginfo("Shutdown signal received. Stopping node.")
        rospy.signal_shutdown("Shutdown signal received")

if __name__ == "__main__":
    try:
        rviz_map = RVizMap()
        rviz_map.run()
    except rospy.ROSInterruptException:
        pass