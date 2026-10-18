from actions import execute_action

def gerer_action_du_mode(current_mode, total_fingers):
    """
    Gère les sous-actions à exécuter en fonction du mode principal dans lequel tu te trouves.
    """
    # --- SI TU ES DANS LE MODE 1 : YOUTUBE ---
    if current_mode == 1:
        if total_fingers == 1:
            execute_action(4)  # Volume -
        elif total_fingers == 2:
            execute_action(5)  # Volume +
        elif total_fingers == 3:
            execute_action(8)  # Avancer de 10s
        elif total_fingers == 4:
            execute_action(9)  # Reculer de 10s
        elif total_fingers == 5:
            execute_action(10) # Pause / Lecture

    # --- SI TU ES DANS LE MODE 2 : MUSIQUE (DEEZER) ---
    elif current_mode == 2:
        if total_fingers == 1:
            execute_action(4)  # Volume -
        elif total_fingers == 2:
            execute_action(5)  # Volume +
        elif total_fingers == 3:
            execute_action(10) # Pause / Lecture

    # --- SI TU ES DANS LE MODE 5 : DIAPORAMA ---
    elif current_mode == 5:
        if total_fingers == 1:
            execute_action(6)  # Page suivante
        elif total_fingers == 2:
            execute_action(7)  # Page précédente


def obtenir_aide_contexte(current_mode):
    """
    Renvoie le texte d'aide contextuel selon le mode actuel.
    """
    if current_mode == 0:
        return (
            "--- AIDE : MENU PRINCIPAL ---\n"
            "• Mode 1 : YouTube 🎬\n"
            "• Mode 2 : Musique 🎵\n"
            "• Mode 3 : Programmation 💻\n"
            "• Mode 4 : Mails & École 🎓\n"
            "• Mode 5 : Diaporama 📊\n"
            "*(Maintenez 2s pour valider un mode)*"
        )
    
    elif current_mode == 1:
        return (
            "--- AIDE : MODE YOUTUBE ---\n"
            "• 1 Doigt : Volume - 🔉\n"
            "• 2 Doigts : Volume + 🔊\n"
            "• 3 Doigts : Avancer +10s ⏩\n"
            "• 4 Doigts : Reculer -10s ⏪\n"
            "• 5 Doigts : Pause / Lecture ⏯️\n"
            "• 10 Doigts : Afficher cette aide\n"
            "• 0 Doigt (1s) : Quitter le mode"
        )
        
    elif current_mode == 2:
        return (
            "--- AIDE : MODE MUSIQUE ---\n"
            "• 1 Doigt : Volume - 🔉\n"
            "• 2 Doigts : Volume + 🔊\n"
            "• 3 Doigts : Lecture / Pause ⏯️\n"
            "• 10 Doigts : Afficher cette aide\n"
            "• 0 Doigt (1s) : Quitter le mode"
        )
        
    elif current_mode == 5:
        return (
            "--- AIDE : MODE DIAPORAMA ---\n"
            "• 1 Doigt : Page suivante ➡️\n"
            "• 2 Doigts : Page précédente ⬅️\n"
            "• 10 Doigts : Afficher cette aide\n"
            "• 0 Doigt (1s) : Quitter le mode"
        )
        
    else:
        return f"Aucune aide disponible pour le Mode {current_mode}."