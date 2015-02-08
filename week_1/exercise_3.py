import sys
sys.path.append('../lib')
import rocommon

if __name__ == '__main__':

    robot = rocommon.Robot()

    try:
        while True:
            choice = raw_input('T = turn; M = move: ')
            unit = float(input("Unit (real): "))

            if choice == 'T' or choice == 't':
                robot.turn(unit)
            else:
                robot.move_forward(unit)

    except KeyboardInterrupt:
        robot.implode()
