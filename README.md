# Loca API

Une API RESTful géolocalisée pour l'application Loca, conçue pour offrir des services de cartographie intelligents, de suivi GPS en temps réel et de calcul d'itinéraires.

## 🚀 Fonctionnalités
- Localisation en temps réel
- Calcul d’itinéraires
- Enregistrement des trajets
- Géocodage / reverse géocoding
- Authentification des utilisateurs

## 🛠️ Tech Stack
- Python 3.x
- Flask RESTful
- PostgreSQL + PostGIS
- Docker (optionnel)

## 📦 Installation

```bash
git clone https://github.com/ton_user/loca-api.git
cd loca-api
python -m venv venv
source venv/bin/activate   # Ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python app.py
