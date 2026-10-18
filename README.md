# ⚡ HandCommand

**HandCommand** est un système de contrôle gesturel et de sécurité biométrique basé sur la vision par ordinateur. Il permet de piloter votre ordinateur, vos médias et vos applications grâce à des gestes de la main en temps réel, après une vérification faciale sécurisée.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?logo=google)
![Tkinter](https://img.shields.io/badge/UI-Tkinter%20HUD-purple)

---

## 🌟 Fonctionnalités Principales

* 🔒 **Authentification Faciale Biométrique** : Accès au système sécurisé par reconnaissance faciale au démarrage via `face_recognition`.
* 🖐️ **Détection Hand Tracking Temps Réel** : Reconnaissance précise des doigts levés grâce à Google MediaPipe Hand Landmarker.
* 🎛️ **Système Multimode Intelligents** :
  * **Mode 1 — YouTube 🎬** : Gestion du volume, avance/retour rapide, lecture/pause.
  * **Mode 2 — Musique 🎵** : Contrôle de la lecture audio et du volume.
  * **Mode 3 — Programmation 💻** : Raccourcis et environnements de développement.
  * **Mode 4 — Mails & École 🎓** : Navigation rapide vers vos outils de travail.
  * **Mode 5 — Diaporama 📊** : Défilement fluide de présentations (Suivant / Précédent).
* 💡 **HUD Dynamique & Épuré** : Un overlay moderne en haut à droite réagit en temps réel à vos commandes et affiche l'aide contextuelle.
* ❓ **Aide Contextuelle Réactive** : Maintenez **10 doigts pendant 1s** pour afficher le menu d'aide dynamique du mode actif.
* 🚪 **Arrêt de Sécurité Global** : Présentez **2 mains fermées (0 doigt pendant 1.5s)** pour couper instantanément l'application.
* 🚀 **Exécution Windows Réactive** : Compilée en `.exe` pour un lancement immédiat via le raccourci `Windows + R`.

---

## 📐 Arborescence du Projet

```text
HandCommand/
├── Programme/
│   ├── main.py              # Point d'entrée de l'application
│   ├── app_controller.py    # Boucle principale et machine à états (Timing & Gestes)
│   ├── face_auth.py         # Module d'authentification faciale
│   ├── hand_detector.py     # Module de détection et comptage des doigts (MediaPipe)
│   ├── mode_handler.py      # Routage des sous-actions et génération de l'aide
│   ├── choix_mode.py        # Gestion des commutations entre modes
│   ├── actions.py           # Exécution des actions système / simulateur de touches
│   └── hud_overlay.py       # Fenêtre Tkinter dynamique (HUD haut à droite)
├── images/
│   └── Moi_IA/              # Repertoire des visages de référence pour l'authentification
├── encodings.pickle         # Cache d'encodage des visages
├── hand_landmark.task       # Modèle IA MediaPipe Hand Landmarker
├── README.md                # Documentation du projet
└── HandCommand.spec         # Configuration de compilation PyInstaller
```

---

## 🚀 Installation & Exécution (Code Source)

### 1. Prérequis
Assurez-vous de disposer de **Python 3.10+** et d'une caméra opérationnelle.

### 2. Cloner et préparer l'environnement
```bash
# Cloner le dépôt
git clone https://github.com/votre-compte/HandCommand.git
cd HandCommand

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances
```bash
pip install opencv-python mediapipe face-recognition numpy pyautogui
```

### 4. Démarrer l'application
```bash
python Programme/main.py
```

---

## 🖐️ Guide des Commandes Gesturelles

| Gesture / Doigts | Condition | Action / Effet |
| :--- | :--- | :--- |
| ** Visage reconnu ** | Au démarrage | Déverrouille et lance l'application |
| **1 à 5 Doigts** | Maintenir 2s (Menu 0) | Sélectionne le Mode (1 à 5) |
| **10 Doigts** | Maintenir 1s | Affiche le menu d'Aide Contextuelle (HUD) |
| **0 Doigt** | Maintenir 1s (En Mode) | Quitte le mode actif et retourne au Menu |
| **2 Mains à 0** | Maintenir 1.5s | **Fermeture complète de HandCommand** |

---

## 🛠️ Compilation en Exécutable `.exe`

Pour générer le fichier standalone utilisable via `Windows + R` :

```bash
pyinstaller --onedir --name HandCommand --collect-all face_recognition_models --collect-all mediapipe Programme/main.py
```

1. Copiez vos fichiers de données (`images/`, `encodings.pickle`) dans le dossier généré `dist/HandCommand/`.
2. Ajoutez le chemin `C:\chemin\vers\HandCommand\dist\HandCommand` à votre variable d'environnement système **PATH**.
3. Exécutez `Windows + R`, tapez **`HandCommand`** et validez !

---

## 👤 Auteur
Projet développé par **Elouan LUCAS** — *HandCommand* ⚡