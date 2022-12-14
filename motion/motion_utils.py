import numpy as np
import math

DISTANCE_TO_SET_NEXT_POINT = 20
DISTANCE_TO_CHANGE_GAIN = 40

class motors_regulator:
    Kp_angle = 1
    Kp_dist = 1

class robot_position:
    actual_pos = [0, 0]
    alpha = 0.0
    x = 0.0
    y = 0.0
    area_radius = 10
    position = [0,0]

# Function to set motor speeds
def motors(left, right):
    return {
        "motor.left.target": [int(left)],
        "motor.right.target": [int(right)],
    }

# Compute the distance between actual_point and point_to_go (2D)
def compute_distance(actual_point, point_to_go):
  distance = math.sqrt(pow(actual_point[0] - point_to_go[0], 2) + pow(actual_point[1] - point_to_go[1], 2))
  return distance

# Compute the angle of the line which link actual_point and point_to_go compared to the horizontal axis
def compute_angle(actual_point, point_to_go):
  angle = -180*math.atan2(point_to_go[1] - actual_point[1], point_to_go[0] - actual_point[0])/math.pi
  return angle

# Modify the regulator gains depending on the distance from a particular point
def compute_regulator_gain(distance, distance_tot):
  if distance < DISTANCE_TO_CHANGE_GAIN or (distance_tot - distance) < DISTANCE_TO_CHANGE_GAIN:
      Kp_angle = 4
      Kp_dist = 0.5

  elif distance > DISTANCE_TO_CHANGE_GAIN and (distance_tot - distance) > DISTANCE_TO_CHANGE_GAIN:
      Kp_angle = 1
      Kp_dist = 1

  return Kp_angle, Kp_dist

# Compute the speed command of the robot
def compute_motor_speed(angle_error, regulator, is_finished):
  if is_finished:
    motor_L = 0
    motor_R = 0
    return motor_L, motor_R

  elif angle_error < -180 :
    angle_error = 360 + angle_error

  elif angle_error > 180 :
    angle_error = -360 + angle_error
      
  motor_L = (regulator.Kp_dist * (180-abs(angle_error))) + regulator.Kp_angle * angle_error
  motor_R = (regulator.Kp_dist * (180-abs(angle_error))) - regulator.Kp_angle * angle_error

  return motor_L, motor_R

# Compute the point where the robot must go
def set_point_to_go(center, actual_point, prev_point_to_go, point_to_go, global_trajectory, distance, is_finished):
  if actual_point == 0:
    point_to_go = list(global_trajectory[0])
    actual_point = 1
    prev_point_to_go = center


  # Point to go = Position of the robot if we reach the end of the list
  elif actual_point >= len(global_trajectory) and distance < DISTANCE_TO_SET_NEXT_POINT:
    is_finished = True

  # If the robot is close to the point to go -> Next point
  elif distance < DISTANCE_TO_SET_NEXT_POINT:
    prev_point_to_go = point_to_go
    point_to_go = list(global_trajectory[actual_point])
    actual_point += 1

  return actual_point, point_to_go, prev_point_to_go, is_finished


