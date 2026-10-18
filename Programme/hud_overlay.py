import tkinter as tk

def show_welcome_hud(mode_text="Bienvenue Elouan !"):
    """
    Affiche un HUD épuré et moderne en haut à droite de l'écran.
    La taille s'adapte dynamiquement si on affiche un texte long (comme l'aide).
    """
    root = tk.Tk()
    root.overrideredirect(True)      # Supprime la barre de titre et les bordures Windows
    root.attributes("-topmost", True)      # Reste toujours au premier plan
    root.attributes("-alpha", 0.94)        # Légère transparence élégante

    screen_width = root.winfo_screenwidth()

    # Détection intelligente de la taille selon le contenu
    nb_lignes = mode_text.count('\n') + 1
    
    if nb_lignes > 1:
        w, h = 440, 300  # Dimensions agrandies pour l'aide contextuelle
    else:
        w, h = 340, 90   # Taille confortable pour un simple mode

    x = screen_width - w - 25
    y = 25  # Fixé en haut à droite
    root.geometry(f"{w}x{h}+{x}+{y}")

    # Fenêtre principale avec un fond sombre style Catppuccin / Moderne
    root.configure(bg="#1e1e2e")

    # Cadre principal avec une bordure fine pour un effet "carte" épurée
    main_frame = tk.Frame(root, bg="#11111b", highlightbackground="#313244", highlightthickness=1)
    main_frame.pack(fill="both", expand=True, padx=2, pady=2)

    # Barre de couleur latérale (accentuation visuelle)
    accent_bar = tk.Frame(main_frame, bg="#a6e3a1", width=6)
    accent_bar.pack(side="left", fill="y")

    # Conteneur du texte
    content_frame = tk.Frame(main_frame, bg="#11111b")
    content_frame.pack(side="left", fill="both", expand=True, padx=16, pady=14)

    # Ligne 1 : Titre de l'application
    tk.Label(
        content_frame, 
        text="⚡ HandCommand", 
        fg="#6c7086", 
        bg="#11111b", 
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w")

    # Ligne 2 : Le texte dynamique (Mode ou Aide complète)
    tk.Label(
        content_frame, 
        text=mode_text, 
        fg="#cdd6f4", 
        bg="#11111b", 
        font=("Segoe UI", 10 if nb_lignes > 1 else 11, "bold" if nb_lignes == 1 else "normal"),
        justify="left"
    ).pack(anchor="w", pady=(6, 0), fill="both", expand=True)

    # Durée d'affichage (6s pour le menu d'aide, 3.5s pour un mode simple)
    duree_affichage = 6000 if nb_lignes > 1 else 3500
    root.after(duree_affichage, root.destroy)
    root.mainloop()

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