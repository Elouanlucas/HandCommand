import os
import pickle
import cv2
import face_recognition

# Dossiers et fichiers de cache
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACEDIR = os.path.join(BASE_DIR, "images", "Moi_IA")
CACHE_FILE = os.path.join(BASE_DIR, "encodings.pickle")

known_face_encodings = []
known_face_names = []

# --- ÉTAPE 1 : CHARGEMENT OU CALCUL DU CACHE ---
if os.path.exists(CACHE_FILE):
    print("[INFO] Chargement rapide des visages depuis le cache (pickle)...")
    with open(CACHE_FILE, "rb") as f:
        data = pickle.load(f)
        known_face_encodings = data["encodings"]
        known_face_names = data["names"]
    print(f"[INFO] {len(known_face_encodings)} encodages chargés instantanément !")

else:
    print("[INFO] Cache introuvable. Analyse des photos de référence (cela ne se fera qu'une seule fois)...")
    
    if not os.path.exists(FACEDIR):
        print(f"[ERREUR] Le dossier {FACEDIR} est introuvable !")
    else:
        for filename in os.listdir(FACEDIR):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                filepath = os.path.join(FACEDIR, filename)
                
                image = face_recognition.load_image_file(filepath)
                encodings = face_recognition.face_encodings(image)
                
                if len(encodings) > 0:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append("Elouan")
                    print(f"  -> {filename} encodée avec succès")

        # Sauvegarder dans le fichier de cache pour les prochains lancements
        if len(known_face_encodings) > 0:
            data = {"encodings": known_face_encodings, "names": known_face_names}
            with open(CACHE_FILE, "wb") as f:
                pickle.dump(data, f)
            print(f"[INFO] Cache sauvegardé avec succès ({len(known_face_encodings)} visages).")

# --- ÉTAPE 2 : LANCEMENT DE LA WEBCAM ---
if len(known_face_encodings) > 0:
    cap = cv2.VideoCapture(0)
    print("[INFO] Démarrage de la webcam...")

    while True:
        success, frame = cap.read()
        if not success:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Inconnu"

            if True in matches:
                name = "Elouan (C'est bien lui !)"

            top, right, bottom, left = [v * 4 for v in face_location]
            color = (0, 255, 0) if name != "Inconnu" else (0, 0, 255)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("HandCommand - Reconnaissance Faciale", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
else:
    print("[ERREUR] Aucun visage n'a pu être chargé, vérifie tes images.")