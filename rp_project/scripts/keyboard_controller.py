#!/usr/bin/python3
import rospy
from geometry_msgs.msg import Twist
import sys
import termios
import tty

"""
This node allows manual control of the sphere using the keyboard.
W/A/S/D keys publish velocity commands on /cmd_vel.
"""

class KeyboardController:
    def __init__(self):
        rospy.init_node("keyboard_controller", anonymous=True)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    # Read a single key from the keyboard without blocking the terminal
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

    def run(self):
        # Main loop: read keyboard input and publish velocity commands
        
        rospy.loginfo("Press 'w', 'a', 's', 'd' for moving the sphere. Press 'q' to stop the node.")
        while not rospy.is_shutdown():
            key = self.get_key()
            twist = Twist()
            if key == 'w':  # up
                twist.linear.y = 0.5
            elif key == 's':  # down
                twist.linear.y = -0.5
            elif key == 'd':  # right
                twist.linear.x = 0.5
            elif key == 'a':  # left
                twist.linear.x = -0.5
            elif key == 'q':  # quit
                rospy.loginfo("shutting down the node.")
                break
            else:
                continue 

            self.pub.publish(twist)
            rospy.sleep(0.1)


if __name__ == "__main__":
    try:
        controller = KeyboardController()
        controller.run()
    except rospy.ROSInterruptException:
        pass