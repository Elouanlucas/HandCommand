import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

tip_ids = [4, 8, 12, 16, 20]

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    h, w, c = image.shape
    y_offset = 50  

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            
            label = handedness.classification[0].label # 'Left' ou 'Right'
            
            # CORRECTION : On inverse l'affichage pour correspondre à tes vraies mains
            nom_main = "Main Gauche" if label == 'Left' else "Main Droite"

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
                    if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = fingers.count(1)

                cv2.putText(image, f'{nom_main} - Doigts: {total_fingers}', (50, y_offset), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                y_offset += 40  

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Compteur 2 Mains', image)
    if cv2.waitKey(5) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()