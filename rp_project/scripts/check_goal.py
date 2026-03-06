#!/usr/bin/python3
import rospy
from rp_project.srv import CheckGoal, CheckGoalResponse

"""
ROS service server that confirms the goal has been reached.
Used by the camera_detection node.
"""

# Service callback: always returns success
def handle_check_goal(req):
    rospy.loginfo("Goal reached confirmed by server.")
    return CheckGoalResponse(success=True)

if __name__ == "__main__":
    rospy.init_node("check_goal_server")
    service = rospy.Service("check_goal", CheckGoal, handle_check_goal)
    rospy.loginfo("Service 'check_goal' is ready.")
    rospy.spin()
    