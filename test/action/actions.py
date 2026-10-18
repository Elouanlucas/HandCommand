import webbrowser
import os
import subprocess
import pyautogui
import time

def tester_action():
    while True:
        print("\n=== TEST DES ACTIONS HANDCOMMAND ===")
        print("1  : Ouvrir YouTube")
        print("2  : Ouvrir l'application Deezer")
        print("3  : Ouvrir VS Code + Gemini + GitHub")
        print("4  : Baisser le volume (-)")
        print("5  : Augmenter le volume (+)")
        print("6  : Diaporama -> Page suivante")
        print("7  : Diaporama -> Page précédente")
        print("8  : YouTube -> Avancer de 10s")
        print("9  : YouTube -> Reculer de 10s")
        print("10 : YouTube -> Pause / Lecture (Espace)")
        print("0  : Quitter le menu de test")
        
        choix = input("\nEntrez un numéro de mode (0 à 10) : ").strip()
        
        if choix == "0":
            print("[INFO] Fin du test.")
            break

        elif choix == "1":
            print("[ACTION] Ouverture de YouTube...")
            webbrowser.open("https://www.youtube.com")

        elif choix == "2":
            print("[ACTION] Ouverture de Deezer...")
            try:
                os.system("start deezer:")
            except Exception as e:
                print(f"[ERREUR] Impossible d'ouvrir Deezer : {e}")

        elif choix == "3":
            print("[ACTION] Lancement de l'environnement de travail...")
            try:
                subprocess.Popen(["code"])
                print(" -> VS Code lancé !")
            except Exception as e:
                print(f" -> Erreur lors du lancement de VS Code : {e}")
                
            webbrowser.open("https://gemini.google.com")
            webbrowser.open("https://github.com")

        elif choix == "4":
            print("[ACTION] Baisse du volume...")
            pyautogui.press('volumedown', presses=5)

        elif choix == "5":
            print("[ACTION] Augmentation du volume...")
            pyautogui.press('volumeup', presses=5)

        elif choix == "6":
            print("[ACTION] Diaporama : Page suivante...")
            time.sleep(2)
            pyautogui.press('right')

        elif choix == "7":
            print("[ACTION] Diaporama : Page précédente...")
            time.sleep(2)
            pyautogui.press('left')

        elif choix == "8":
            print("[ACTION] YouTube : Avancer de 10 secondes...")
            time.sleep(2)
            pyautogui.press('l')

        elif choix == "9":
            print("[ACTION] YouTube : Reculer de 10 secondes...")
            time.sleep(2)
            pyautogui.press('j')

        elif choix == "10":
            print("[ACTION] YouTube : Pause / Lecture...")
            time.sleep(2)
            pyautogui.press('space')  # Touche Espace pour basculer entre lecture et pause

        else:
            print(f"[ACTION] Le mode {choix} n'est pas configuré.")

if __name__ == "__main__":
    tester_action()