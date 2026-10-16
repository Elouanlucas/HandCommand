import cv2

# Ouvre la webcam
cap = cv2.VideoCapture(0)

print("Appuie sur 'q' pour quitter la vidéo.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible d'accéder à la caméra.")
        break

    # Affiche le flux vidéo
    cv2.imshow("HandCommand - Test", frame)

    # Quitte avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()