import webbrowser
import os
import subprocess
import threading
import pyautogui
from hud_overlay import show_welcome_hud

def execute_action(action_id):
    """
    Exécute l'action et affiche le HUD dans un thread séparé pour éviter les latences.
    """
    print(f"[ACTION] Exécution de la commande pour l'Action {action_id}...")
    
    # On lance le HUD dans un thread indépendant pour ne pas bloquer OpenCV
    threading.Thread(target=_run_action_logic, args=(action_id,), daemon=True).start()

def _run_action_logic(action_id):
    """
    Contient la vraie logique d'exécution pour ne pas bloquer le fil principal.
    """
    if action_id == 1:
        show_welcome_hud("Ouverture de YouTube 🎬")
        webbrowser.open("https://www.youtube.com")
        
    elif action_id == 2:
        show_welcome_hud("Ouverture de Deezer 🎵")
        try:
            os.system("start deezer:")
        except Exception as e:
            print(f"[ERREUR] Impossible d'ouvrir Deezer : {e}")
            
    elif action_id == 3:
        show_welcome_hud("Ouverture Environnement Dev 💻")
        try:
            subprocess.Popen(["code"])
        except Exception as e:
            print(f" -> Erreur lors du lancement de VS Code : {e}")
        webbrowser.open("https://gemini.google.com")
        webbrowser.open("https://github.com")

    elif action_id == 4:
        show_welcome_hud("Volume - 🔉")
        pyautogui.press('volumedown', presses=5)

    elif action_id == 5:
        show_welcome_hud("Volume + 🔊")
        pyautogui.press('volumeup', presses=5)

    elif action_id == 6:
        show_welcome_hud("Diaporama : Suivant ➡️")
        pyautogui.press('right')

    elif action_id == 7:
        show_welcome_hud("Diaporama : Précédent ⬅️")
        pyautogui.press('left')

    elif action_id == 8:
        show_welcome_hud("YouTube : +10s ⏩")
        pyautogui.press('l')

    elif action_id == 9:
        show_welcome_hud("YouTube : -10s ⏪")
        pyautogui.press('j')

    elif action_id == 10:
        show_welcome_hud("YouTube : Pause / Lecture ⏯️")
        pyautogui.press('space')

    elif action_id == 11:
        show_welcome_hud("Ouverture Mails 🎓")
        webbrowser.open("https://mail.google.com/mail/")

    elif action_id == 12:
        show_welcome_hud("Ouverture École ESEO 🎓")
        webbrowser.open("https://reseaueseo.sharepoint.com/sites/etu/")

    else:
        show_welcome_hud(f"Action {action_id} inconnue ⚠️")