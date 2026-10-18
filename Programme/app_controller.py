import cv2
import time
from face_auth import authenticate_user
from hand_detector import HandFingerCounter

class HandCommandApp:
    def __init__(self, show_camera=True):
        self.show_camera = show_camera
        self.detector = None
        self.cap = None
        
        # Variables d'état des modes
        self.current_mode = 0
        self.stable_fingers = -1
        self.hold_start_time = None
        self.HOLD_DURATION = 2.0       # 2 secondes pour valider un mode (1 à 10)
        self.RESET_DURATION = 1.0      # 1 seconde pour valider le retour à 0

        # Sécurité globale (2 mains à 0 pendant 1.5s = fermeture complète)
        self.global_close_start_time = None
        self.GLOBAL_CLOSE_DURATION = 1.5

    def run(self):
        print("[INFO] Démarrage du processus de sécurité HandCommand...")
        
        # Étape 1 : Authentification faciale
        if authenticate_user(show_camera=self.show_camera):
            print("[INFO] Authentification réussie ! Lancement du gestionnaire de modes...")
        else:
            print("[INFO] Authentification échouée ou annulée.")
            return

        # Étape 2 : Initialisation de la caméra et du détecteur de mains
        self.cap = cv2.VideoCapture(0)
        self.detector = HandFingerCounter(max_num_hands=2, min_confidence=0.7)

        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                break

            image, total_fingers, hands_detected, hands_at_zero = self.detector.process_frame(image)
            h, w, _ = image.shape
            current_time = time.time()

            # --- SÉCURITÉ GLOBALE : 2 MAINS À 0 PENDANT 1.5s = FERMÉ ---
            if hands_detected == 2 and hands_at_zero == 2:
                if self.global_close_start_time is None:
                    self.global_close_start_time = current_time
                
                close_elapsed = current_time - self.global_close_start_time
                close_time_left = max(0, round(self.GLOBAL_CLOSE_DURATION - close_elapsed, 1))

                if self.show_camera:
                    cv2.putText(image, f"Fermeture dans {close_time_left}s...", (50, h - 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if close_elapsed >= self.GLOBAL_CLOSE_DURATION:
                    print("[INFO] 2 mains à 0 détectées pendant 1.5s. Fermeture de HandCommand...")
                    break
            else:
                self.global_close_start_time = None

            # --- LOGIQUE DE SÉLECTION DES MODES (0 à 10) ---
            if self.current_mode == 0:
                if hands_detected > 0:
                    if total_fingers == 0:
                        self.stable_fingers = 0
                        self.hold_start_time = None
                        if self.show_camera:
                            cv2.putText(image, "Montrez 1 a 10 doigts (Maintien 2s)", (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    elif 1 <= total_fingers <= 10:
                        if total_fingers == self.stable_fingers:
                            if self.hold_start_time is None:
                                self.hold_start_time = current_time
                            
                            elapsed = current_time - self.hold_start_time
                            time_left = max(0, round(self.HOLD_DURATION - elapsed, 1))
                            
                            if self.show_camera:
                                cv2.putText(image, f"Total: {total_fingers}... Restez {time_left}s", (50, 50), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            
                            if elapsed >= self.HOLD_DURATION:
                                self.current_mode = total_fingers
                                self.stable_fingers = -1
                                self.hold_start_time = None
                                print(f"[INFO] Mode {self.current_mode} activé !")
                        else:
                            self.stable_fingers = total_fingers
                            self.hold_start_time = current_time
                else:
                    if self.show_camera:
                        cv2.putText(image, "Montrez vos mains", (50, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    self.stable_fingers = -1
                    self.hold_start_time = None
            else:
                # Mode actif -> Vérification du retour à 0 pour quitter
                if hands_detected > 0 and total_fingers == 0:
                    if self.stable_fingers == 0:
                        if self.hold_start_time is None:
                            self.hold_start_time = current_time
                        
                        elapsed = current_time - self.hold_start_time
                        time_left = max(0, round(self.RESET_DURATION - elapsed, 1))
                        
                        if self.show_camera:
                            msg = f"Quitter le mode dans {time_left}s..."
                            text_size = cv2.getTextSize(msg, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                            # Correction appliquée ici avec l'argument 'image'
                            cv2.putText(image, msg, (w - text_size[0] - 20, h - 55), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                        
                        if elapsed >= self.RESET_DURATION:
                            self.current_mode = 0
                            self.stable_fingers = -1
                            self.hold_start_time = None
                            print("[INFO] Mode réinitialisé (Retour à 0)")
                    else:
                        self.stable_fingers = 0
                        self.hold_start_time = current_time
                else:
                    self.stable_fingers = -1
                    self.hold_start_time = None

            # --- AFFICHAGE DU MODE ACTIF EN BAS À DROITE ---
            if self.current_mode > 0:
                message = f"MODE {self.current_mode} ACTIF (0 pdt 1s pour quitter)"
                if self.show_camera:
                    text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                    cv2.putText(image, message, (w - text_size[0] - 20, h - 20), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Affichage de la caméra
            if self.show_camera:
                cv2.imshow('HandCommand - Sécurisé', image)
                if cv2.waitKey(5) & 0xFF == 27:  # Échap pour quitter
                    break
            else:
                cv2.waitKey(50)

        self.cap.release()
        self.detector.release()
        if self.show_camera:
            cv2.destroyAllWindows()
        print("[INFO] Programme HandCommand fermé.")