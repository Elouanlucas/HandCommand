import tkinter as tk

# Création de la fenêtre invisible par défaut
root = tk.Tk()

# 1. Configuration de la fenêtre (Sans bordure, toujours au premier plan, transparente)
root.overrideredirect(True)  # Supprime la barre de titre et les bordures Windows
root.attributes("-topmost", True)  # Reste toujours au-dessus des autres fenêtres
root.attributes(
    "-alpha", 0.9
)  # Légère transparence globale (de 0.0 à 1.0) pour un effet stylé

# 2. Calcul de la position : en bas à droite de l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 280
window_height = 80

# Marge de 20 pixels par rapport aux bords, et 60 pixels pour éviter la barre des tâches Windows
x = screen_width - window_width - 20
y = screen_height - window_height - 60

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 3. Design du widget (Cadre aux couleurs sombres/modernes)
frame = tk.Frame(root, bg="#11111b", bd=0)
frame.pack(fill="both", expand=True)

# Ligne décorative ou bordure lumineuse sur le côté gauche
accent_bar = tk.Frame(frame, bg="#89b4fa", width=4)
accent_bar.pack(side="left", fill="y")

# Contenu textuel
text_container = tk.Frame(frame, bg="#11111b")
text_container.pack(side="left", fill="both", expand=True, padx=12, pady=12)

title_label = tk.Label(
    text_container,
    text="⚡ HandCommand HUD",
    fg="#cdd6f4",
    bg="#11111b",
    font=("Segoe UI", 10, "bold"),
)
title_label.pack(anchor="w")

status_label = tk.Label(
    text_container,
    text="Statut : En attente...",
    fg="#a6adc8",
    bg="#11111b",
    font=("Segoe UI", 9),
)
status_label.pack(anchor="w", pady=(4, 0))


# 4. Astuce pour fermer le widget facilement : un double-clic dessus
def close_app(event):
    root.destroy()


root.bind("<Double-Button-1>", close_app)

# Lancement de l'affichage
root.mainloop()