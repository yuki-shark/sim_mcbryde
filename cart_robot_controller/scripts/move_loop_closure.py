#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64
# import std_msgs.msg
import math

def auto_move_publisher():
    controller = rospy.Publisher('/cmd_vel', geometry_msgs/Twist, queue_size=10)

    rospy.init_node('auto_move_publisher', anonymous=True)
    rate = rospy.Rate(60) # 60hz
    init_time = rospy.get_time()
    rospy.loginfo("init")
    # pan.publish(0.0)
    time = 0

    while not rospy.is_shutdown():
        if robot.position.x > -7.55 and x < -7.45 and y <= 8.5:
            controller.publish('[0.0 0.5 0.0]' '[0.0 0.0 0.0]')
        elif y > 8.45 and y< 8.55 and x > -7.55 and x < -7.45 and yaw <= 0.0:
            controller.publish('[0.0 0.0 0.0]' '[0.0 0.0 -0.2]')
        elif y > 8.45 and y< 8.55 and yaw > -0.01 and yaw < 0.01 and x <= 6.0:
            controller.publish('[0.0 0.5 0.0]' '[0.0 0.0 0.0]')
        rate.sleep()

if __name__ == '__main__':
    try:
        auto_move_publisher()
    except rospy.ROSInterruptException:
        pass
