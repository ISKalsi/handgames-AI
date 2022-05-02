import enum
import mediapipe as mp
import math
from typing import NamedTuple

mp_landmarks = mp.solutions.hands.HandLandmark


class Finger(NamedTuple):
    tip: mp_landmarks
    base: mp_landmarks
    reference: mp_landmarks = mp_landmarks.WRIST


class Fingers(enum.Enum):
    index = Finger(mp_landmarks.INDEX_FINGER_TIP, mp_landmarks.INDEX_FINGER_PIP)
    middle = Finger(mp_landmarks.MIDDLE_FINGER_TIP, mp_landmarks.MIDDLE_FINGER_PIP)
    ring = Finger(mp_landmarks.RING_FINGER_TIP, mp_landmarks.RING_FINGER_PIP)
    pinky = Finger(mp_landmarks.PINKY_TIP, mp_landmarks.PINKY_PIP)
    thumb = Finger(mp_landmarks.THUMB_TIP, mp_landmarks.THUMB_CMC, mp_landmarks.PINKY_MCP)


class State(NamedTuple):
    index: bool = False
    middle: bool = False
    ring: bool = False
    pinky: bool = False
    thumb: bool = False

    @staticmethod
    def fromDict(state: dict[Finger, bool]):
        return State(state[Fingers.index.value],
                     state[Fingers.middle.value],
                     state[Fingers.ring.value],
                     state[Fingers.pinky.value],
                     state[Fingers.thumb.value])


class Numbers(enum.Enum):
    invalid = State(False, False, True, False, False)
    one = State(True, False, False, False, False)
    two = State(True, True, False, False, False)
    three = State(True, True, True, False, False)
    four = State(True, True, True, True, False)
    five = State(True, True, True, True, True)
    six = State(False, False, False, False, True)
    seven = State(True, False, False, False, True)
    eight = State(True, True, False, False, True)
    nine = State(False, True, True, True, True)
    ten = State(False, False, False, False, False)

    def int(self):
        for i, num in enumerate(Numbers):
            if num.value == self.value:
                return i
        return 0


class HandState:
    total_hands = 0

    def __init__(self, landmarks=None):
        HandState.total_hands += 1
        self.id = HandState.total_hands
        self.landmarks = landmarks
        self.__is_in_camera = False
        self.__has_recognized_number = False
        self.__results = []

    def __del__(self):
        HandState.total_hands -= 1

    @property
    def has_recognized_number(self):
        return self.__has_recognized_number

    @property
    def is_in_camera(self):
        return self.__is_in_camera

    @is_in_camera.setter
    def is_in_camera(self, new):
        if not new:
            self.__results.clear()
        self.__is_in_camera = new

    def __is_finger_up(self, finger: Finger) -> bool:
        wrist = self.landmarks[finger.reference]
        base = self.landmarks[finger.base]
        tip = self.landmarks[finger.tip]

        wrist_xy = [val * 100 for val in (wrist.x, wrist.y)]
        base_xy = [val * 100 for val in (base.x, base.y)]
        tip_xy = [val * 100 for val in (tip.x, tip.y)]

        tip_from_wrist = math.dist(tip_xy, wrist_xy)
        base_from_wrist = math.dist(base_xy, wrist_xy)
        return base_from_wrist <= tip_from_wrist

    def recognize_number(self, new_landmarks) -> Numbers:
        self.landmarks = new_landmarks
        finger_state: dict[Finger, bool] = {}
        for finger in Fingers:
            finger_state[finger.value] = self.__is_finger_up(finger.value)

        currentState = State.fromDict(finger_state)
        for num in Numbers:
            if num.value == currentState:
                self.__results.append(num)
                self.__has_recognized_number = True
                return self.recognized_number()

        self.__results.append(Numbers.invalid)
        return self.recognized_number()

    def recognized_number(self) -> Numbers:
        return max(self.__results, key=self.__results.count)
