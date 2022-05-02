import cv2
import mediapipe as mp

from camera_input import camera_input
from cli import batting, bowling, toss

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    has_won_toss = toss()
    while True:
        if has_won_toss:
            decider = int(input('''
    you won the toss:
        1-bat first
        2-bowl first
                '''))
            if decider == 2:
                target = bowling(0, 0, input_function=camera_input, arg=(cap,))
                batting(target, 1, input_function=camera_input, args=(cap,))
                break
            else:
                score = batting(0, 0, input_function=camera_input, args=(cap,))
                bowling(score, 1, input_function=camera_input, arg=(cap,))
                break
        else:
            print('''computer won the toss, it chose to bowl first''')
            score = batting(0, 0, input_function=camera_input, args=(cap,))
            bowling(score, 1, input_function=camera_input, arg=(cap,))
            break

    cap.release()
