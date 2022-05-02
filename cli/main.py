import cv2

from camera_input import camera_input
from demo_camera_input import demo_camera_input

from cli import batting, bowling, toss

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    input_func = camera_input

    has_won_toss = toss()
    while True:
        if has_won_toss:
            decider = int(input('''
    you won the toss:
        1-bat first
        2-bowl first
                '''))
            if decider == 2:
                target = bowling(0, 0, input_function=input_func, arg=(cap,))
                batting(target, 1, input_function=input_func, args=(cap,))
                break
            else:
                score = batting(0, 0, input_function=input_func, args=(cap,))
                bowling(score, 1, input_function=input_func, arg=(cap,))
                break
        else:
            print('''computer won the toss, it chose to bowl first''')
            score = batting(0, 0, input_function=input_func, args=(cap,))
            bowling(score, 1, input_function=input_func, arg=(cap,))
            break

    cap.release()
