#!/usr/bin/python3
import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from rp_project.srv import ResetPosition, CheckGoal
from rp_project.msg import Collision

"""
This node monitors the sphere position and checks two conditions:
1) If the sphere enters the field of view of one of the cameras (collision).
2) If the sphere reaches the goal area.

In case of collision, the sphere position is reset via a ROS service.
In case of goal reached, the simulation is stopped.
"""

class BallController:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node("ball_controller", anonymous=True)

        # Subscribers:
        # - sphere position in RViz
        # - rotating camera cones positions
        self.ball_sub = rospy.Subscriber("/ball_position", Marker, self.check_conditions)
        self.cone_sub = rospy.Subscriber("/rotating_cones_positions", Marker, self.update_cone_positions)

        # Publishers:
        # - collision event notification
        # - shutdown signal when goal is reached
        self.collision_pub = rospy.Publisher("/collision_event", Collision, queue_size=10)
        self.shutdown_pub = rospy.Publisher("/shutdown", Marker, queue_size=10)

        # Goal configuration
        self.goal_position = [-6.0, 6.0]
        self.goal_tolerance = 0.5

        # Camera cone configuration
        self.cone_positions = [] 
        self.cone_tolerance = 1.5


    def update_cone_positions(self, marker_msg):
        """
        Convert rotating cone positions from RViz markers into
        world coordinates used for collision detection.
        """

        adjusted_positions = []
        
        left_cone_center = (-2.5, -2.5)
        right_cone_center = (2.5, 2.5)
        
        for idx, point in enumerate(marker_msg.points):
            if idx == 0:  
                adjusted_x = point.x - (-13.0) + left_cone_center[0]
                adjusted_y = point.y - (-13.0) + left_cone_center[1]
            elif idx == 1: 
                adjusted_x = point.x - (-8.0) + right_cone_center[0]
                adjusted_y = point.y - (-8.0) + right_cone_center[1]
            else:
                continue
            
            adjusted_positions.append((adjusted_x, adjusted_y))
        
        self.cone_positions = adjusted_positions

    def check_conditions(self, marker_msg):
        """
        Check if the sphere:
        - enters a camera field of view (collision)
        - reaches the goal area
        """

        x, y = marker_msg.pose.position.x, marker_msg.pose.position.y

        for cone_position in self.cone_positions:
            distance = ((x - cone_position[0]) ** 2 + (y - cone_position[1]) ** 2) ** 0.5
            if distance <= self.cone_tolerance:
                collision_msg = Collision()
                collision_msg.message = f"Collision detected at:"
                collision_msg.x = cone_position[0]
                collision_msg.y = cone_position[1]
                
                self.collision_pub.publish(collision_msg)
                rospy.loginfo(f"Published collision message: {collision_msg.message} ({collision_msg.x}, {collision_msg.y})")

                rospy.loginfo("Collision detected! Calling reset_position service.")
                self.call_reset_position_service()
                return

        distance_to_goal = ((x - self.goal_position[0]) ** 2 + (y - self.goal_position[1]) ** 2) ** 0.5
        if distance_to_goal <= self.goal_tolerance:
            rospy.loginfo("Goal reached! Calling check_goal service.")
            self.call_check_goal_service()

    def call_reset_position_service(self):
        """Call the service that resets the sphere to its initial position."""

        rospy.wait_for_service("reset_position")
        try:
            reset_service = rospy.ServiceProxy("reset_position", ResetPosition)
            response = reset_service()
            if response.success:
                rospy.loginfo("Position reset successfully.")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")

    def call_check_goal_service(self):
        """Call the service that confirms goal reaching and shuts down the simulation."""

        rospy.wait_for_service("check_goal")
        try:
            goal_service = rospy.ServiceProxy("check_goal", CheckGoal)
            response = goal_service()
            if response.success:
                rospy.loginfo("Goal confirmed by service. Publishing shutdown signal.")
                self.shutdown_pub.publish(Marker())
                rospy.signal_shutdown("Goal reached")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")


if __name__ == "__main__":
    try:
        controller = BallController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass