import tkinter as tk
import threading
import queue
import time

class HudOverlay:
    """
    Gestionnaire d'affichage HUD en arrière-plan (non bloquant).
    Tourne dans son propre thread daemon et écoute une file de messages
    afin de ne jamais bloquer la boucle principale OpenCV ni les actions.
    """
    def __init__(self):
        self.queue = queue.Queue()
        self.root = None
        self.timer_id = None
        self.ready_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        self.ready_event.wait()

    def show(self, text):
        """Envoie une notification au HUD en arrière-plan."""
        self.queue.put(text)

    def _run(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)      # Supprime la barre de titre et les bordures Windows
        self.root.attributes("-topmost", True)      # Reste toujours au premier plan
        self.root.attributes("-alpha", 0.94)        # Légère transparence élégante
        self.root.configure(bg="#1e1e2e")
        self.root.withdraw()                       # Caché par défaut

        self.screen_width = self.root.winfo_screenwidth()

        # Cadre principal avec une bordure fine pour un effet "carte" épurée
        self.main_frame = tk.Frame(self.root, bg="#11111b", highlightbackground="#313244", highlightthickness=1)
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Barre de couleur latérale (accentuation visuelle)
        accent_bar = tk.Frame(self.main_frame, bg="#a6e3a1", width=6)
        accent_bar.pack(side="left", fill="y")

        # Conteneur du texte
        self.content_frame = tk.Frame(self.main_frame, bg="#11111b")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        # Ligne 1 : Titre de l'application
        self.title_label = tk.Label(
            self.content_frame, 
            text="⚡ HandCommand", 
            fg="#6c7086", 
            bg="#11111b", 
            font=("Segoe UI", 9, "bold")
        )
        self.title_label.pack(anchor="w")

        # Ligne 2 : Le texte dynamique (Mode ou Aide complète)
        self.text_label = tk.Label(
            self.content_frame, 
            text="", 
            fg="#cdd6f4", 
            bg="#11111b", 
            justify="left"
        )
        self.text_label.pack(anchor="w", pady=(6, 0), fill="both", expand=True)

        self.ready_event.set()
        self._check_queue()
        self.root.mainloop()

    def _check_queue(self):
        try:
            while not self.queue.empty():
                text = self.queue.get_nowait()
                self._update_display(text)
        except Exception as e:
            print(f"[ERREUR HUD] : {e}")

        if self.root:
            self.root.after(40, self._check_queue)

    def _update_display(self, mode_text):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        # Détection intelligente de la taille selon le contenu
        nb_lignes = mode_text.count('\n') + 1

        if nb_lignes > 1:
            w, h = 440, 300  # Dimensions agrandies pour l'aide contextuelle
            font = ("Segoe UI", 10, "normal")
            duree_affichage = 6000
        else:
            w, h = 340, 90   # Taille confortable pour un simple mode
            font = ("Segoe UI", 11, "bold")
            duree_affichage = 3500

        x = self.screen_width - w - 25
        y = 25  # Fixé en haut à droite
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.text_label.configure(
            text=mode_text, 
            font=font
        )
        
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)

        self.timer_id = self.root.after(duree_affichage, self.root.withdraw)


# Instance unique (Singleton paresseux thread-safe)
_hud_instance = None
_hud_lock = threading.Lock()

def _get_hud():
    global _hud_instance
    if _hud_instance is None:
        with _hud_lock:
            if _hud_instance is None:
                _hud_instance = HudOverlay()
    return _hud_instance

def show_welcome_hud(mode_text="Bienvenue Elouan !"):
    """
    Affiche un HUD épuré et moderne en haut à droite de l'écran en arrière-plan.
    Non bloquant : s'exécute dans un thread d'arrière-plan sans interrompre la boucle principale.
    """
    _get_hud().show(mode_text)

# Test du rendu d'aide si exécuté directement
if __name__ == "__main__":
    aide_test = (
        "--- AIDE : MODE YOUTUBE ---\n"
        "• 1 Doigt : Ouvrir YouTube\n"
        "• 4 Doigts : Volume - 🔉\n"
        "• 5 Doigts : Volume + 🔊\n"
        "• 8 Doigts : Avancer +10s ⏩\n"
        "• 9 Doigts : Reculer -10s ⏪\n"
        "• 10 Doigts : Afficher cette aide\n"
        "• 0 Doigt (1s) : Quitter le mode"
    )
    show_welcome_hud(aide_test)
    time.sleep(7)
