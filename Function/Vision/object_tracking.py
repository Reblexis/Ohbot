# import the opencv library
import cv2
from Function import physical_controller
import math


class FaceTracking:
    """
    Experimental implementation of face tracking via mounted camera on the robot.
    """

    DISTANCE_TRESHOLD = 0.1
    SPEED_LIMIT = 0.8

    def rotate_to_target(self, relative_target_pos: tuple, speed: float = 10):
        """
        Rotates the robot's head to the target position.
        :param relative_target_pos: Tuple of relative target position (x, y) in range <-1, 1> where (0, 0) is the center.
         -1 = left / top and 1 = right / bottom from the robot's perspective.
        """
        x_pos = relative_target_pos[0]
        y_pos = relative_target_pos[1]

        x_distance = abs(relative_target_pos[0])
        y_distance = abs(relative_target_pos[1])

        distance_total = math.sqrt(x_distance ** 2 + y_distance ** 2)

        speed_x = max(min(x_distance * speed, self.SPEED_LIMIT), 0.1)
        speed_y = max(min(y_distance * speed, self.SPEED_LIMIT), 0.1)

        if x_distance > self.DISTANCE_TRESHOLD:
            dir_x = (x_pos) / x_distance
            cur_x_rotation += 3 * dir_x * (x_distance ** 2)
            cur_x_rotation = max(min(OHBOT_ROT_LIMIT, cur_x_rotation), 0)
            ohbot.move(ohbot.HEADTURN, cur_x_rotation, spd=speed_x)

        if y_distance > DISTANCE_TRESHOLD:
            dir_y = -(face_y - 0.5) / y_distance
            cur_y_rotation += 3 * dir_y * (y_distance ** 2)
            cur_y_rotation = max(min(OHBOT_ROT_LIMIT, cur_y_rotation), 0)
            ohbot.move(ohbot.HEADNOD, cur_y_rotation, spd=speed_y)


def direct_move_to_target(x, y, speed):
    currentMotorXRotation = ohbot.motorPos[ohbot.HEADTURN]
    currentMotorYRotation = 10 - ohbot.motorPos[ohbot.HEADNOD]

    move_x = (x - 0.5) * HORIZONTAL_MOVE_SCALE * DIRECTION
    move_y = (y - 0.5) * VERTICAL_MOVE_SCALE * DIRECTION

    if currentMotorXRotation + move_x < 0 or currentMotorXRotation + move_x > OHBOT_ROT_LIMIT or currentMotorYRotation + move_y > OHBOT_ROT_LIMIT or currentMotorYRotation + move_y < 0:
        print("Target too far!")
        return

    ohbot.move(ohbot.HEADTURN, currentMotorXRotation + move_x, spd=speed)
    ohbot.move(ohbot.HEADNOD, currentMotorYRotation + move_y, spd=speed)
