from app_controller import HandCommandApp

# Configuration globale
SHOW_CAMERA = True

if __name__ == "__main__":
    app = HandCommandApp(show_camera=SHOW_CAMERA)
    app.run()