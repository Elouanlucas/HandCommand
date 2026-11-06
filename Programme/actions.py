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
        pyautogui.press('volumedown', presses=5)
        show_welcome_hud("Volume - 🔉")

    elif action_id == 5:
        pyautogui.press('volumeup', presses=5)
        show_welcome_hud("Volume + 🔊")

    elif action_id == 6:  
        pyautogui.press('right')
        show_welcome_hud("Diaporama : Suivant ➡️")

    elif action_id == 7:
        pyautogui.press('left')
        show_welcome_hud("Diaporama : Précédent ⬅️")

    elif action_id == 8:
        pyautogui.press('l')
        show_welcome_hud("YouTube : +10s ⏩")

    elif action_id == 9:
        pyautogui.press('j')
        show_welcome_hud("YouTube : -10s ⏪")

    elif action_id == 10:
        pyautogui.press('space')
        show_welcome_hud("YouTube : Pause / Lecture ⏯️")

    elif action_id == 11:
        webbrowser.open("https://mail.google.com/mail/")
        show_welcome_hud("Ouverture Mails 🎓")

    elif action_id == 12:
        webbrowser.open("https://reseaueseo.sharepoint.com/sites/etu/")
        show_welcome_hud("Ouverture École ESEO 🎓")

    else:
        show_welcome_hud(f"Action {action_id} inconnue ⚠️")