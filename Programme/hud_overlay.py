import tkinter as tk

def show_welcome_hud():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.95)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    w, h = 300, 80
    x = screen_width - w - 20
    y = screen_height - h - 60
    root.geometry(f"{w}x{h}+{x}+{y}")

    frame = tk.Frame(root, bg="#11111b", bd=0)
    frame.pack(fill="both", expand=True)

    accent = tk.Frame(frame, bg="#a6e3a1", width=5)
    accent.pack(side="left", fill="y")

    content = tk.Frame(frame, bg="#11111b")
    content.pack(side="left", fill="both", expand=True, padx=12, pady=12)

    tk.Label(content, text="⚡ HandCommand", fg="#cdd6f4", bg="#11111b", font=("Segoe UI", 10, "bold")).pack(anchor="w")
    tk.Label(content, text="Bienvenue Elouan !", fg="#a6e3a1", bg="#11111b", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(2, 0))

    # Disparaît tout seul au bout de 4 secondes
    root.after(4000, root.destroy)
    root.mainloop()