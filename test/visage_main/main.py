import os
import pickle
import time
import cv2
import face_recognition
import tkinter as tk

# --- ÉTAPE 1 : CHARGEMENT DU CACHE DE RECONNAISSANCE FACIALE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACEDIR = os.path.join(BASE_DIR, "images", "Moi_IA")
CACHE_FILE = os.path.join(BASE_DIR, "encodings.pickle")

known_face_encodings = []
known_face_names = []

if os.path.exists(CACHE_FILE):
  print("[INFO] Chargement rapide des visages depuis le cache...")
  with open(CACHE_FILE, "rb") as f:
    data = pickle.load(f)
    known_face_encodings = data["encodings"]
    known_face_names = data["names"]
else:
  print("[INFO] Cache introuvable. Analyse des photos...")
  if os.path.exists(FACEDIR):
    for filename in os.listdir(FACEDIR):
      if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filepath = os.path.join(FACEDIR, filename)
        image = face_recognition.load_image_file(filepath)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
          known_face_encodings.append(encodings[0])
          known_face_names.append("Elouan")

    if len(known_face_encodings) > 0:
      data = {"encodings": known_face_encodings, "names": known_face_names}
      with open(CACHE_FILE, "wb") as f:
        pickle.dump(data, f)

if len(known_face_encodings) == 0:
  print("[ERREUR] Aucun visage de référence trouvé !")
  exit()

# --- ÉTAPE 2 : DÉTECTION EN ARRIÈRE-PLAN (SANS FENÊTRE VIDÉO) ---
cap = cv2.VideoCapture(0)
print("[INFO] Authentification en arrière-plan en cours... Regardez la caméra.")

authenticated = False
match_start_time = None
required_duration = 1.5  # 1.5 secondes de maintien

while True:
  success, frame = cap.read()
  if not success:
    break

  # Réduire la taille pour un traitement fluide et rapide en arrière-plan
  small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
  rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

  face_locations = face_recognition.face_locations(rgb_small_frame)
  face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

  recognized_this_frame = False

  for face_encoding in face_encodings:
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    if True in matches:
      recognized_this_frame = True
      break

  current_time = time.time()

  if recognized_this_frame:
    if match_start_time is None:
      match_start_time = current_time  # Début du chrono des 3s

    elapsed = current_time - match_start_time

    # Si les 3 secondes sont écoulées en continu
    if elapsed >= required_duration:
      authenticated = True
      break
  else:
    # Si tu bouges ou quittes des yeux, on remet le chrono à zéro
    match_start_time = None

  # Petite pause pour ne pas saturer le processeur inutilement en arrière-plan
  cv2.waitKey(100)

# Libérer proprement la caméra (aucune fenêtre OpenCV n'a été ouverte)
cap.release()


# --- ÉTAPE 3 : AFFICHAGE DU WIDGET HUD SI AUTHENTIFIÉ ---
def show_welcome_hud():
  root = tk.Tk()
  root.overrideredirect(True)
  root.attributes("-topmost", True)
  root.attributes("-alpha", 0.95)

  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  w, h = 300, 80
  x = screen_width - w - 20
  y = screen_height - h - 60
  root.geometry(f"{w}x{h}+{x}+{y}")

  frame = tk.Frame(root, bg="#11111b", bd=0)
  frame.pack(fill="both", expand=True)

  accent = tk.Frame(frame, bg="#a6e3a1", width=5)
  accent.pack(side="left", fill="y")

  content = tk.Frame(frame, bg="#11111b")
  content.pack(side="left", fill="both", expand=True, padx=12, pady=12)

  tk.Label(
      content,
      text="⚡ HandCommand",
      fg="#cdd6f4",
      bg="#11111b",
      font=("Segoe UI", 10, "bold"),
  ).pack(anchor="w")
  tk.Label(
      content,
      text="Bienvenue Elouan !",
      fg="#a6e3a1",
      bg="#11111b",
      font=("Segoe UI", 11, "bold"),
  ).pack(anchor="w", pady=(2, 0))

  # Le widget disparaît tout seul au bout de 4 secondes
  root.after(4000, root.destroy)
  root.mainloop()


if authenticated:
  print("[INFO] Authentification réussie !")
  show_welcome_hud()
else:
  print("[INFO] Authentification annulée.")