import cv2
import mediapipe as mp

from hand_state import HandState

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def camera_input(cap) -> int:
    hand = HandState()
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    hand.recognize_number(hand_landmarks.landmark)

            elif hand.has_recognized_number:
                return hand.recognized_number().int()

            if cv2.waitKey(5) & 0xFF == 27:
                break
