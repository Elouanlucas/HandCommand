import cv2
import time
from hand_detector import HandFingerCounter

def main():
    cap = cv2.VideoCapture(0)
    detector = HandFingerCounter(max_num_hands=2, min_confidence=0.7)

    # --- VARIABLES D'ÉTAT POUR LES MODES (1 à 10) ---
    current_mode = 0          
    stable_fingers = -1       
    hold_start_time = None    
    HOLD_DURATION = 2.0       # 2 secondes pour valider un mode (1 à 10)
    RESET_DURATION = 1.0      # 1 seconde pour valider le retour à 0

    print("[INFO] Démarrage du gestionnaire de modes par gestes...")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Appel du module externe pour détecter les mains et compter les doigts
        image, total_fingers, hands_detected = detector.process_frame(image)
        h, w, _ = image.shape
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
            if hands_detected > 0 and total_fingers == 0:
                if stable_fingers == 0:
                    if hold_start_time is None:
                        hold_start_time = current_time
                    
                    elapsed = current_time - hold_start_time
                    time_left = max(0, round(RESET_DURATION - elapsed, 1))
                    
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

        cv2.imshow('HandCommand - Gestionnaire de Modes', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Échap pour quitter
            break

    cap.release()
    detector.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()