import os
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACEDIR = os.path.join(os.path.dirname(BASE_DIR), "images", "Moi_IA")

print("[INFO] Nettoyage et normalisation des 5 images de référence...")

for filename in os.listdir(FACEDIR):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filepath = os.path.join(FACEDIR, filename)
        
        # 1. Lecture brute avec OpenCV
        img = cv2.imread(filepath)
        if img is None:
            print(f"[ERREUR] Impossible de lire {filename}")
            continue
            
        # 2. Redimensionnement standardisé (ex: largeur max 800px pour alléger et stabiliser)
        h, w = img.shape[:2]
        if w > 800:
            scale = 800 / w
            img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
            
        # 3. Réenregistrement propre (écrase l'image avec un format standard sans métadonnées corrompues)
        cv2.imwrite(filepath, img)
        print(f"[OK] Image normalisée : {filename}")

print("[INFO] Terminé ! Tu peux supprimer ton fichier encodings.pickle et relancer main.py.")