from hud_overlay import show_welcome_hud
from actions import execute_action

def gerer_choix_mode(mode):
    """
    Fonction centrale qui gère le choix du mode (1 à 5).
    Pour l'instant, elle affiche simplement le HUD épuré correspondant.
    Dans le futur, c'est ici que tu appelleras tes fichiers d'actions.
    """
    print(f"[MODE] Mode {mode} détecté et traité.")
    
    if mode == 0:
        show_welcome_hud("Choix mode principal 🎛️")
        

    elif mode == 1:
        show_welcome_hud("Mode YouTube 🎬")
        execute_action(1)  # Appel de l'action spécifique à YouTube

    elif mode == 2:
        show_welcome_hud("Mode Musique 🎵")
        execute_action(2)  # Appel de l'action spécifique à la musique
            
    elif mode == 3:
        show_welcome_hud("Mode Programmation 💻")
        execute_action(3)  # Appel de l'action spécifique au code

    elif mode == 4:
        show_welcome_hud("Mode École 📚")
        execute_action(12)  # Appel de l'action spécifique à l'école (SharePoint ESEO)
        execute_action(11)  # Appel de l'action spécifique aux mails (Gmail)

    elif mode == 5:
        show_welcome_hud("Mode Diaporama 📊")
        
    else:
        show_welcome_hud(f"Mode {mode} inconnu ⚠️")
        print(f"[MODE] Avertissement : Le mode {mode} n'est pas répertorié.")


# Petit bloc de test indépendant si tu lances ce fichier seul depuis ton terminal
if __name__ == "__main__":
    print("=== TEST DU GESTIONNAIRE DE MODES ===")
    choix = input("Entre un numéro de mode à tester (1 à 5) : ").strip()
    
    if choix.isdigit():
        gerer_choix_mode(int(choix))
    else:
        print("[ERREUR] Veuillez entrer un nombre valide.")