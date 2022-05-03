import cv2
import mediapipe as mp
from handgames.hand import HandState


def detect_number(video_capture) -> int:
    hand = HandState()
    with mp.solutions.hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while video_capture.isOpened():
            success, image = video_capture.read()
            if not success:
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    hand.recognize_number(hand_landmarks.landmark)
            elif hand.has_recognized_number:
                yield hand.recognized_number().int()
                break

            yield None
