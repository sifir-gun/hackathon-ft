# Générateur d'Articles SEO

Ce script automatise la génération d'articles SEO optimisés en utilisant l'API Mistral et Notion.

## Prérequis

- Python 3.8+
- Compte Notion avec une base de données configurée
- Clé API Mistral

## Installation

1. Clonez ce dépôt
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```
3. Configurez les variables d'environnement dans le fichier `.env`

## Structure de la base Notion

La base Notion doit contenir les colonnes suivantes :
- name (titre)
- keyword (mot-clé)
- topic (thématique)
- angle (angle éditorial)
- seo_goal (objectif SEO)
- audience (public visé)
- article_final (réservé pour le contenu généré)

## Utilisation

Exécutez le script :
```bash
python seo_writer.py
```

Le script va :
1. Détecter les nouvelles entrées dans la base Notion
2. Générer un titre SEO optimisé
3. Créer une trame d'article
4. Rédiger l'article complet
5. Enrichir le contenu pour atteindre 1000 mots minimum
6. Mettre à jour la base Notion avec l'article final 
