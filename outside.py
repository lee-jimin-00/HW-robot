#!/home/pi/.pyenv/versions/rospy3/bin/python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 0

    def lds_callback(self, scan):
        right_range, left_range = 0, 0
        turtle_vel = Twist()
        for i in range(40):
            range_per_angle = scan.ranges[i]
            right_range += range_per_angle
            range_per_angle = scan.ranges[320+i]
            left_range += range_per_angle
        right_range = right_range / 40
        left_range = left_range / 40
        if right_range < 0.25 or left_range < 0.25:
            if right_range < left_range:
                turtle_vel.linear.x = 0.0
                turtle_vel.angular.z = -1.2
            else:
                turtle_vel.linear.x = 0.0
                turtle_vel.angular.z = 1.2
        else:
            if (scan.ranges[90] < 0.25 or scan.ranges[80] < 0.25) and (scan.ranges[270] > 0.25 or scan.ranges[280] > 0.25):
                turtle_vel.linear.x = 0.18
                turtle_vel.angular.z = 0.0
            elif (scan.ranges[90] > 0.25 or scan.ranges[80] > 0.25) and (scan.ranges[270] < 0.25 or scan.ranges[280] < 0.25):
                turtle_vel.linear.x = 0.18
                turtle_vel.angular.z = 0.0
            elif (scan.ranges[90] > 0.25 or scan.ranges[80] > 0.25) and (scan.ranges[270] > 0.25 or scan.ranges[280] > 0.25):
                if scan.ranges[130] < 0.25:
                    turtle_vel.linear.x = 0.18
                    turtle_vel.angular.z = -0.1
                elif scan.ranges[220] < 0.25:
                    turtle_vel.linear.x = 0.18
                    turtle_vel.angular.z = 0.1
                else: 
                    turtle_vel.linear.x = 0.18    
                    turtle_vel.angular.z = 1.0
            else:
                turtl_vel.linear.x=0.18
                turtle_vel.angular.z=0.0          


        self.publisher.publish(turtle_vel)


def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan, lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()
