from face_auth import authenticate_user
from hud_overlay import show_welcome_hud

if __name__ == "__main__":
    print("[INFO] Démarrage du processus de sécurité HandCommand...")
    
    # Étape 1 : On appelle l'authentification faciale en arrière-plan
    if authenticate_user(show_camera=True):
        print("[INFO] Authentification réussie ! Affichage du HUD...")
        # Étape 2 : Si validé, on appelle l'affichage du widget
        show_welcome_hud()
    else:
        print("[INFO] Authentification échouée ou annulée.")