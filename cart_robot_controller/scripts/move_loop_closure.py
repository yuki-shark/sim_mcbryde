#!/usr/bin/env python
# license removed for brevity
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D
import tf.transformations
import math

controller = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

# Parameters
linear_speed = 1.5
angular_speed = -0.2

point1 = Pose2D(-7.5, 8.5, math.pi/2)
point2 = Pose2D(6.0, 8.5, 0.0)
point3 = Pose2D(6.0, -7.2, -math.pi/2)
point4 = Pose2D(-7.5, -7.2, -math.pi)

position_margin = 0.2
angular_margin = 0.01

def callback(data):

    global msg

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    z = data.pose.pose.position.z
    quaternion = (
            data.pose.pose.orientation.x,
            data.pose.pose.orientation.y,
            data.pose.pose.orientation.z,
            data.pose.pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]

    # init Twist msg
    msg.linear.x = 0.0
    msg.linear.y = 0.0
    msg.linear.z = 0.0
    msg.angular.x = 0.0
    msg.angular.y = 0.0
    msg.angular.z = 0.0

    if x > (point1.x - position_margin) and x < (point1.x + position_margin) and \
       yaw > (point1.theta - angular_margin) and yaw < (point1.theta + angular_margin) and \
       y < point1.y:
        msg.linear.x = linear_speed
        rospy.loginfo("state 0")
    elif x > (point1.x - position_margin) and x < (point1.x + position_margin) and \
         y > (point1.y - position_margin) and y < (point1.y + position_margin) and \
         yaw > point2.theta:
        msg.angular.z = angular_speed
        rospy.loginfo("state 1")
    elif y > (point2.y - position_margin) and y < (point2.y + position_margin) and \
         yaw > (point2.theta - angular_margin) and yaw < (point2.theta + angular_margin) and \
         x < point2.x:
        msg.linear.x = linear_speed
        rospy.loginfo("state 2")
    elif y > (point2.y - position_margin) and y < (point2.y + position_margin) and \
         x > (point2.x - position_margin) and x < (point2.x + position_margin) and \
         yaw > point3.theta:
        msg.angular.z = angular_speed
        rospy.loginfo("state 3")
    elif x > (point3.x - position_margin) and x < (point3.x + position_margin) and \
         yaw > (point3.theta - angular_margin) and yaw < (point3.theta + angular_margin) and \
         y > point3.y:
        msg.linear.x = linear_speed
        rospy.loginfo("state 4")
    elif x > (point3.x - position_margin) and x < (point3.x + position_margin) and \
         y > (point3.y - position_margin) and y < (point3.y + position_margin) and \
         yaw > (point4.theta + angular_margin):
        msg.angular.z = angular_speed
        rospy.loginfo("state 5")
    elif y > (point4.y - position_margin) and y < (point4.y + position_margin) and \
         (yaw > -point4.theta - angular_margin  or yaw < point4.theta + angular_margin) and \
         x > point4.x:
        msg.linear.x = linear_speed
        rospy.loginfo("state 6")
    elif y > (point4.y - position_margin) and y < (point4.y + position_margin) and \
         x > (point4.x - position_margin) and x < (point4.x + position_margin) and \
         (yaw < (point4.theta + angular_margin) or yaw > point1.theta):
        msg.angular.z = angular_speed
        rospy.loginfo("state 7")
    else:
        rospy.logwarn("Cart robot is out of the path!")

    controller.publish(msg)
    rospy.loginfo("x:%s y:%s yaw:%s", x, y, yaw)

def auto_move_publisher():
    global msg
    msg = Twist()
    rospy.init_node('auto_move_publisher', anonymous=True)
    rospy.Subscriber("/odom", Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        auto_move_publisher()
    except rospy.ROSInterruptException:
        pass
