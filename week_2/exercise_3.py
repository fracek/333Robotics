import rocommon

SPEED = 4.0
K = 0.1


if __name__ == "__main__":
    robot = rocommon.Robot()

    robot.SetRotationSpeed(SPEED)
    initial_distance = robot.sonar.GetValue()
    left_speed = SPEED
    right_speed = SPEED
    try:
        while True:
            if robot.left_bumper.IsTouching() or robot.right_bumper.IsTouching():
                break

            dist = initial_distance - robot.sonar.GetValue()
            # 0 = R, 1 = L
            if dist < 0: # too far away
                # left wheel > right wheel
                left_speed = SPEED - K * dist
                right_speed = SPEED
            elif dist > 0: # too close
                # right wheel > left wheel
                left_speed = SPEED
                right_speed = SPEED + K * dist
            robot.SetRotationSpeed([right_speed, left_speed], motors=[0, 1])

    except KeyboardInterrupt:
        robot.Implode()
