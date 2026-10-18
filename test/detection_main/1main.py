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

    right_hand_found = False

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            
            label = handedness.classification[0].label # 'Left' ou 'Right'
            
            # À cause du flip horizontal, ta main droite physique est 'Left'
            if label == 'Right': 
                right_hand_found = True
                lm_list = []
                h, w, c = image.shape
                
                for lm in hand_landmarks.landmark:
                    lm_list.append([int(lm.x * w), int(lm.y * h)])

                if lm_list:
                    fingers = []

                    # 1. Gestion du Pouce (Basée sur la distance avec la base du petit doigt - point 17)
                    # Cela fonctionne parfaitement que ce soit paume ou dos de la main !
                    distance_pouce = math.hypot(lm_list[4][0] - lm_list[17][0], lm_list[4][1] - lm_list[17][1])
                    distance_ref = math.hypot(lm_list[3][0] - lm_list[17][0], lm_list[3][1] - lm_list[17][1])
                    
                    if distance_pouce > distance_ref * 1.1:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    # 2. Les 4 autres doigts (Comparaison sur l'axe Y : le bout vs la deuxième articulation)
                    for id in range(1, 5):
                        if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    total_fingers = fingers.count(1)

                    cv2.putText(image, f'Main Droite - Doigts: {total_fingers}', (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                break 

    if not right_hand_found:
        cv2.putText(image, 'Montrez votre main droite', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Compteur de Main Droite', image)
    if cv2.waitKey(5) & 0xFF == 27: 
        break

cap.release()
cv2.destroyAllWindows()