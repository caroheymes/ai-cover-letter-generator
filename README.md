# 🎯 Générateur de Lettres de Motivation IA

Une application Streamlit alimentée par CrewAI (gpt-5-nano) qui génère des lettres de motivation ultra-personnalisées en analysant votre CV et l'entreprise cible.
Permet de générer des candidatures spontanées avec la description minimale d'un poste, ou de faire du réseau en vue d'un poste


## 🚀 Fonctionnalités
- Analyse de CV (PDF/Word)
- Recherche automatique sur le web (Culture d'entreprise)
- Rédaction et Relecture par des agents IA spécialisés
- Export en Word (.docx) et Markdown de la lettre, des paramètres des agents et du "brouillon"

## 🛠️ Installation locale

1. Cloner le repo
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer l'app : `streamlit run app.py`

## 🐳 Docker
```bash
docker build -t cover-letter-app .
docker run -p 8080:8080 cover-letter-app```


## Déploiement sur Google Cloud Run
```gcloud builds submit --tag gcr.io/VOTRE_PROJET_ID/cover-letter-app .
gcloud run deploy cover-letter-app --image gcr.io/VOTRE_PROJET_ID/cover-letter-app --platform managed --region europe-west9 --allow-unauthenticated
```
Si cette app vous fait gagner du temps, offrez moi un café !
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/CaroMS)

