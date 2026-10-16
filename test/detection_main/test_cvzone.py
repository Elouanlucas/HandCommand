import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialisation de la webcam et de MediaPipe Hands
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# ID des bouts des doigts : [Pouce, Index, Majeur, Annulaire, Auriculaire]
tip_ids = [4, 8, 12, 16, 20]

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Convertir l'image en RGB pour MediaPipe
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape
                lm_list.append([int(lm.x * w), int(lm.y * h)])

            if lm_list:
                fingers = []

                # Pouce (comparaison sur l'axe X)
                if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # 4 autres doigts (comparaison sur l'axe Y)
                for id in range(1, 5):
                    if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = fingers.count(1)

                # Afficher le résultat à l'écran
                cv2.putText(image, f'Doigts: {total_fingers}', (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Compteur de doigts', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Appuyer sur Échap pour quitter
        break

cap.release()
cv2.destroyAllWindows()