import cv2
import mediapipe as mp
import math

class HandFingerCounter:
    def __init__(self, max_num_hands=2, min_confidence=0.7):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands, 
            min_detection_confidence=min_confidence, 
            min_tracking_confidence=min_confidence
        )
        self.tip_ids = [4, 8, 12, 16, 20]

    def process_frame(self, image):
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        h, w, c = image.shape
        total_fingers = 0
        hands_detected = 0
        hands_at_zero = 0  # Compte les mains levées mais fermées à 0 doigts

        if results.multi_hand_landmarks:
            hands_detected = len(results.multi_hand_landmarks)
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = []
                for lm in hand_landmarks.landmark:
                    lm_list.append([int(lm.x * w), int(lm.y * h)])

                if lm_list:
                    fingers = []

                    # Pouce (distance avec la base du petit doigt - point 17)
                    distance_pouce = math.hypot(lm_list[4][0] - lm_list[17][0], lm_list[4][1] - lm_list[17][1])
                    distance_ref = math.hypot(lm_list[3][0] - lm_list[17][0], lm_list[3][1] - lm_list[17][1])
                    
                    if distance_pouce > distance_ref * 1.1:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    # Les 4 autres doigts
                    for id in range(1, 5):
                        if lm_list[self.tip_ids[id]][1] < lm_list[self.tip_ids[id] - 2][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    hand_fingers = fingers.count(1)
                    total_fingers += hand_fingers

                    if hand_fingers == 0:
                        hands_at_zero += 1

                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return image, total_fingers, hands_detected, hands_at_zero

    def release(self):
        self.hands.close()