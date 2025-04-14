"""
Script d'automatisation de rédaction SEO utilisant l'API Mistral et Notion.
Ce script génère des articles optimisés SEO à partir d'une base de données
Notion.
"""

import os
from notion_client import Client
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration des clients
notion = Client(auth=os.getenv("NOTION_TOKEN"))
mistral = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def get_new_articles():
    """Récupère les nouvelles lignes non traitées de la base Notion."""
    database_id = "1d300bd51c3b806593aad455c22e7076"
    response = notion.databases.query(
        database_id=database_id,
        filter={
            "property": "Article",
            "rich_text": {
                "is_empty": True
            }
        }
    )
    return response["results"]


def generate_title(context):
    """Génère un titre SEO optimisé en français."""
    prompt = (
        "IMPORTANT: Réponds UNIQUEMENT en FRANÇAIS.\n\n"
        "En tant qu'expert SEO francophone de haut niveau, crée un titre accrocheur et "
        "professionnel qui captive immédiatement l'attention. Contexte : {context}.\n"
        "Critères:\n"
        "- Maximum 70 caractères\n"
        "- Ton dynamique et impactant\n"
        "- Vocabulaire business et innovation\n"
        "- Optimisé SEO français\n"
        "- Utilise des mots-clés percutants du secteur tech"
    ).format(context=context)

    messages = [ChatMessage(role="user", content=prompt)]
    response = mistral.chat(
        model="mistral-tiny",
        messages=messages
    )
    return response.choices[0].message.content


def generate_outline(title):
    """Génère la trame de l'article en français."""
    prompt = (
        "IMPORTANT: Réponds UNIQUEMENT en FRANÇAIS.\n\n"
        "En tant que stratège éditorial français, développe une structure d'article "
        "captivante pour le titre : {title}.\n"
        "Structure requise:\n"
        "1. Introduction percutante qui accroche immédiatement\n"
        "2. Trois parties principales avec sous-titres dynamiques\n"
        "3. Conclusion forte avec call-to-action\n\n"
        "Style attendu:\n"
        "- Ton professionnel et expert\n"
        "- Vocabulaire business et innovation\n"
        "- Structure journalistique moderne\n"
        "- Optimisation SEO française"
    ).format(title=title)

    messages = [ChatMessage(role="user", content=prompt)]
    response = mistral.chat(
        model="mistral-tiny",
        messages=messages
    )
    return response.choices[0].message.content


def generate_article(outline, context):
    """Génère l'article complet en français."""
    prompt = (
        "IMPORTANT: Réponds UNIQUEMENT en FRANÇAIS.\n\n"
        "En tant qu'expert de contenu digital français, rédige un article professionnel "
        "selon cette structure : {outline}.\n"
        "Contexte à intégrer : {context}\n\n"
        "Exigences:\n"
        "- Style journalistique moderne et dynamique\n"
        "- Ton expert et engageant\n"
        "- Vocabulaire business et innovation\n"
        "- Citations et exemples concrets\n"
        "- Chiffres et données pertinents\n"
        "- Optimisation SEO française poussée\n"
        "- Appels à l'action stratégiques\n"
        "- Phrases d'accroche impactantes\n"
        "Garde les noms propres (entreprises, personnes) tels quels."
    ).format(outline=outline, context=context)

    messages = [ChatMessage(role="user", content=prompt)]
    response = mistral.chat(
        model="mistral-tiny",
        messages=messages
    )
    return response.choices[0].message.content


def enrich_article(article):
    """Enrichit l'article en français pour atteindre 1000 mots minimum."""
    prompt = (
        "IMPORTANT: Réponds UNIQUEMENT en FRANÇAIS.\n\n"
        "En tant qu'expert SEO français, optimise et enrichis cet article : {article}\n"
        "Objectifs:\n"
        "- Atteindre minimum 1000 mots\n"
        "- Renforcer le ton professionnel et dynamique\n"
        "- Ajouter des exemples concrets et chiffres\n"
        "- Intégrer des phrases d'accroche percutantes\n"
        "- Optimiser la structure pour le SEO français\n"
        "- Maintenir un style fluide et engageant\n"
        "- Renforcer les appels à l'action\n"
        "Conserve les noms propres en l'état."
    ).format(article=article)

    messages = [ChatMessage(role="user", content=prompt)]
    response = mistral.chat(
        model="mistral-tiny",
        messages=messages
    )
    return response.choices[0].message.content


def verify_french_content(text):
    """Vérifie que le contenu est bien en français."""
    verification_prompt = (
        "IMPORTANT: Réponds UNIQUEMENT en FRANÇAIS.\n\n"
        "Vérifie que ce texte est bien en français. S'il contient des parties en anglais, "
        "traduis-les en français tout en gardant les noms propres : {text}"
    ).format(text=text)
    response = mistral.chat(
        model="mistral-tiny",
        messages=[ChatMessage(role="user", content=verification_prompt)]
    )
    return response.choices[0].message.content


def update_notion_page(page_id, article):
    """Met à jour la page Notion avec l'article final."""
    # Diviser l'article en parties de 2000 caractères maximum
    MAX_LENGTH = 1900  # Un peu moins que 2000 pour la sécurité
    parts = [article[i:i + MAX_LENGTH] for i in range(0, len(article), MAX_LENGTH)]
    
    rich_text_parts = []
    for part in parts:
        rich_text_parts.append({
            "text": {
                "content": part
            }
        })
    
    notion.pages.update(
        page_id=page_id,
        properties={
            "Article": {
                "rich_text": rich_text_parts
            }
        }
    )


def main():
    """Fonction principale qui orchestre le processus de génération d'articles."""
    # Récupération des nouveaux articles
    new_articles = get_new_articles()

    print(f"Nombre d'articles trouvés : {len(new_articles)}")

    for article in new_articles:
        try:
            # Extraction des données
            properties = article["properties"]
            print("\nPropriétés de l'article :")
            print(properties)

            # Vérification que le contexte existe
            if not properties["Contexte"]["rich_text"]:
                print(f"Article {article['id']} ignoré : contexte manquant")
                continue

            context = properties["Contexte"]["rich_text"][0]["text"]["content"]
            print(f"Contexte trouvé : {context}")

            # Génération du contenu
            title = generate_title(context)
            outline = generate_outline(title)
            article_content = generate_article(outline, context)
            final_article = enrich_article(article_content)

            # Vérification du contenu en français
            if not verify_french_content(final_article):
                print(f"Article {article['id']} ignoré : contenu non en français")
                continue

            # Mise à jour de la base Notion
            update_notion_page(article["id"], final_article)
            print(f"Article {article['id']} traité avec succès")

        except Exception as e:
            print(f"Erreur lors du traitement de l'article {article['id']}: {str(e)}")
            continue


if __name__ == "__main__":
    main()
