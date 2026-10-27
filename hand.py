import math

import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision


class Hand:
    def __init__(self, model="models/hand_landmarker.task"):
        options = vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model), num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def find(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
        if not result.hand_landmarks:
            return None
        h, w = frame.shape[:2]
        return [(p.x * w, p.y * h) for p in result.hand_landmarks[0]]


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def count_fingers(points):
    wrist = points[0]
    count = 0
    for tip, joint in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if distance(points[tip], wrist) > distance(points[joint], wrist):
            count += 1
    if distance(points[4], points[17]) > distance(points[3], points[17]):
        count += 1
    return count
