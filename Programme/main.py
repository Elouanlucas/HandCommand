from app_controller import HandCommandApp

# Configuration globale
SHOW_CAMERA = True
NOT_SHOW_CAMERA = False

if __name__ == "__main__":
    app = HandCommandApp(show_camera=NOT_SHOW_CAMERA)
    app.run()