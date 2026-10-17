import os
import pickle
import time
import cv2
import face_recognition
import numpy as np

def authenticate_user(show_camera=False):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FACEDIR = os.path.join(os.path.dirname(BASE_DIR), "images", "Moi_IA")
    CACHE_FILE = os.path.join(BASE_DIR, "encodings.pickle")

    known_face_encodings = []
    known_face_names = []

    # 1. Chargement ou création du cache d'encodages
    if os.path.exists(CACHE_FILE):
        print("[INFO] Chargement rapide des visages depuis le cache...")
        with open(CACHE_FILE, "rb") as f:
            data = pickle.load(f)
            known_face_encodings = data["encodings"]
            known_face_names = data["names"]
    else:
        print(f"[INFO] Vérification du dossier : {FACEDIR}")
        if os.path.exists(FACEDIR):
            fichiers = os.listdir(FACEDIR)
            
            for filename in sorted(fichiers):
                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    filepath = os.path.join(FACEDIR, filename)
                    
                    try:
                        image = face_recognition.load_image_file(filepath)
                        
                        height, width = image.shape[:2]
                        if width > 1200 or height > 1200:
                            scale = 1200 / max(width, height)
                            image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

                        image = np.ascontiguousarray(image)
                        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=2)
                        
                        if not face_locations:
                            print(f"[DEBUG] Aucun visage détecté dans : {filename}")
                            continue

                        encodings = face_recognition.face_encodings(image, face_locations)
                        
                        if len(encodings) > 0:
                            known_face_encodings.append(encodings[0])
                            known_face_names.append("Elouan")
                            print(f"[INFO] Visage validé et encodé : {filename}")
                    
                    except Exception as e:
                        print(f"[ATTENTION] Erreur sur {filename} : {e}")
                        continue

            if len(known_face_encodings) > 0:
                print(f"[INFO] {len(known_face_encodings)} visages de référence encodés avec succès.")
                data = {"encodings": known_face_encodings, "names": known_face_names}
                with open(CACHE_FILE, "wb") as f:
                    pickle.dump(data, f)

    if len(known_face_encodings) == 0:
        print(f"[ERREUR] Aucun visage de référence trouvé dans {FACEDIR} !")
        return False

    cap = cv2.VideoCapture(0)
    mode_str = "avec affichage" if show_camera else "en arrière-plan"
    print(f"[INFO] Authentification stricte {mode_str} en cours...")

    authenticated = False
    match_start_time = None
    required_duration = 1.5       # 1.5 secondes de présence requises pour valider
    timeout_duration = 5.0        # 5 secondes d'inactivité max avant abandon

    global_start_time = time.time()
    min_distance = 1.0            

    while True:
        success, frame = cap.read()
        if not success:
            break

        current_time = time.time()

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        recognized_this_frame = False
        target_location = None

        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                min_distance = face_distances[best_match_index]

                # Seuil strict : 0.5
                if min_distance < 0.5:
                    recognized_this_frame = True
                    target_location = face_location
                    break

        if recognized_this_frame:
            # ⭐ ASTUCE : Dès qu'on te reconnaît, on repousse le timeout global 
            # pour ne jamais abandonner tant que ton visage est face à la caméra.
            global_start_time = current_time

            if match_start_time is None:
                match_start_time = current_time

            elapsed = current_time - match_start_time

            if show_camera and target_location is not None:
                time_left = max(0, int(required_duration - elapsed + 1))
                top, right, bottom, left = [int(v * 2) for v in target_location]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"Elouan ({min_distance:.2f}) - {time_left}s",
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            if elapsed >= required_duration:
                authenticated = True
                break
        else:
            match_start_time = None
            
            # Le timeout de 5s ne s'applique que si aucun visage familier n'est détecté
            if current_time - global_start_time > timeout_duration:
                print("[INFO] Timeout atteint : Aucun visage reconnu au bout de 5 secondes. Arrêt.")
                break

            if show_camera:
                time_before_timeout = max(0, int(timeout_duration - (current_time - global_start_time) + 1))
                cv2.putText(
                    frame,
                    f"Inconnu / Recherche... ({time_before_timeout}s)",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

        if show_camera:
            cv2.imshow("HandCommand - Authentification", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            cv2.waitKey(50)

    cap.release()
    if show_camera:
        cv2.destroyAllWindows()

    return authenticated