# Projet : Analyse temporelle du Bitcoin

Ce projet a été réalisé dans le cadre du cours **8PRO408 – Outils de programmation pour la science des données (UQAC)**.  
Il consiste en une analyse exploratoire et temporelle des données historiques du Bitcoin, ainsi qu’une application interactive développée avec **Streamlit**.

---

## Objectifs du projet

- Charger et manipuler un jeu de données volumineux (séries temporelles).
- Réaliser une analyse exploratoire du prix et du volume.
- Étudier les tendances, la volatilité et les relations entre variables.
- Produire des visualisations adaptées aux séries temporelles.
- Proposer une application interactive pour explorer les données.

---

## Contenu du dépôt

- `notebook.ipynb` : Analyse exploratoire et temporelle complète (EDA) réalisée à partir du jeu de données brut.
- `app.py` : Application Streamlit interactive (version déployée en ligne).
- `btc_daily_agg.csv` : Jeu de données agrégé par jour, utilisé par l’application Streamlit.
- `reductiondataframe.py` : Script Python permettant de transformer le jeu de données brut (à la minute) en données journalières.
- `rapport.pdf` : Rapport synthétique du projet.
- `requirements.txt` : Bibliothèques nécessaires au fonctionnement de l’application.
- `README.md` : Description du projet.
---

## Jeu de données

Le jeu de données est trop volumineux pour être hébergé sur GitHub.

Lien Kaggle : https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data

---

## Prétraitement des données

Le jeu de données original fourni est très volumineux (données à la minute).  
Afin de pouvoir l’exploiter efficacement dans l’application Streamlit, un script de réduction a été utilisé :  

- `reductiondataframe.py`

Ce script permet de :
- Charger les données brutes à la minute.
- Convertir la colonne `Timestamp` en format date.
- Trier les données chronologiquement.
- Agréger les données par **jour** avec les opérations suivantes :
  - Open → première valeur de la journée  
  - High → maximum journalier  
  - Low → minimum journalier  
  - Close → dernière valeur de la journée  
  - Volume → somme journalière  

Le fichier généré est :
- `btc_daily_agg.csv`  
Ce fichier correspond à une version allégée des données, utilisée directement par l’application Streamlit.

---

## Prérequis

- Python 3.14
- Bibliothèques Python :
  - streamlit  
  - pandas  
  - plotly  
  - matplotlib  
  - seaborn  
  - numpy  

---

## Acces au tableau de bord

L’application sera accessible dans le navigateur à l’adresse : https://analyse-temporelle-du-bitcoin-bqf32mpvj2ydwmf6xzrv3r.streamlit.app

---

## Fonctionnalités de l’application

- Visualisation interactive du prix du Bitcoin.

- Analyse du volume avec filtres temporels.

- Visualisation de la volatilité.

- Affichage des moyennes mobiles.

- Filtres par période.

---

## Auteur

Projet réalisé par : Ayad-Zeddam Malik / Lopez Valentin / Abgarov Artur / Razafindratsima Nathan

Cours : 8PRO408 – UQAC

Année universitaire : 2025–2026



















