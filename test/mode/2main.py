import cv2
import mediapipe as mp
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
# On autorise la détection de 2 mains maximum
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

tip_ids = [4, 8, 12, 16, 20]

# --- VARIABLES D'ÉTAT POUR LES MODES (1 à 10) ---
current_mode = 0          # 0 = Aucun mode, 1 à 10 = Modes actifs
stable_fingers = -1       # Nombre total de doigts stable
hold_start_time = None    # Chronomètre général
HOLD_DURATION = 2.0       # 2 secondes pour valider un mode (1 à 10)
RESET_DURATION = 1.0      # 1 seconde pour valider le retour à 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    h, w, c = image.shape
    total_fingers = 0
    hands_detected = 0

    if results.multi_hand_landmarks:
        hands_detected = len(results.multi_hand_landmarks)
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for lm in hand_landmarks.landmark:
                lm_list.append([int(lm.x * w), int(lm.y * h)])

            if lm_list:
                fingers = []

                # 1. Gestion du Pouce (distance avec la base du petit doigt - point 17)
                distance_pouce = math.hypot(lm_list[4][0] - lm_list[17][0], lm_list[4][1] - lm_list[17][1])
                distance_ref = math.hypot(lm_list[3][0] - lm_list[17][0], lm_list[3][1] - lm_list[17][1])
                
                if distance_pouce > distance_ref * 1.1:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # 2. Les 4 autres doigts
                for id in range(1, 5):
                    if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # On additionne les doigts de cette main au total global
                total_fingers += fingers.count(1)

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    current_time = time.time()

    # --- LOGIQUE QUAND AUCUN MODE N'EST ACTIF (Mode 0 -> Sélection 1 à 10) ---
    if current_mode == 0:
        if hands_detected > 0:
            if total_fingers == 0:
                stable_fingers = 0
                hold_start_time = None
                cv2.putText(image, "Montrez entre 1 et 10 doigts (Maintien 2s)", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            elif 1 <= total_fingers <= 10:
                if total_fingers == stable_fingers:
                    if hold_start_time is None:
                        hold_start_time = current_time
                    
                    elapsed = current_time - hold_start_time
                    time_left = max(0, round(HOLD_DURATION - elapsed, 1))
                    
                    cv2.putText(image, f"Total: {total_fingers} doigt(s)... Restez {time_left}s", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                    if elapsed >= HOLD_DURATION:
                        current_mode = total_fingers
                        stable_fingers = -1
                        hold_start_time = None
                        print(f"[INFO] Mode {current_mode} active !")
                else:
                    stable_fingers = total_fingers
                    hold_start_time = current_time
        else:
            cv2.putText(image, "Montrez vos mains", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            stable_fingers = -1
            hold_start_time = None

    # --- LOGIQUE QUAND UN MODE (1 à 10) EST ACTIF ---
    else:
        # On vérifie si l'utilisateur fait 0 pour quitter (avec un maintien requis d'1 seconde)
        if hands_detected > 0 and total_fingers == 0:
            if stable_fingers == 0:
                if hold_start_time is None:
                    hold_start_time = current_time
                
                elapsed = current_time - hold_start_time
                time_left = max(0, round(RESET_DURATION - elapsed, 1))
                
                # Affichage du compte à rebours pour quitter en bas à droite
                message = f"Quitter dans {time_left}s..."
                text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.putText(image, message, (w - text_size[0] - 20, h - 55), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                if elapsed >= RESET_DURATION:
                    current_mode = 0
                    stable_fingers = -1
                    hold_start_time = None
                    print("[INFO] Mode reinitialise (Retour a 0)")
            else:
                stable_fingers = 0
                hold_start_time = current_time
        else:
            # Si l'utilisateur montre autre chose que 0, on annule le chrono de reset
            stable_fingers = -1
            hold_start_time = None

    # --- AFFICHAGE DU MODE EN BAS À DROITE ---
    if current_mode > 0:
        message = f"MODE {current_mode} ACTIF (Faites 0 pendant 1s pour quitter)"
        text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        text_x = w - text_size[0] - 20
        text_y = h - 20
        cv2.putText(image, message, (text_x, text_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Gestionnaire de Modes (1-10)', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Échap pour quitter
        break

cap.release()
cv2.destroyAllWindows()