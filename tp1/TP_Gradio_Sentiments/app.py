# TP - Classification de sentiments avec Gradio
# Cours 2 : Gradio - Framework d'Implementation des Projets IA
#
# Meme demarche que le TP guide du cours (classification d'images) :
#   modele pre-entraine -> fonction Python -> interface Gradio -> utilisateur
#
# Lancement :
#   python -m pip install gradio transformers torch sentencepiece
#   python app.py

import gradio as gr
from transformers import pipeline

# Deploiement sur Hugging Face Spaces (materiel gratuit ZeroGPU) :
# le paquet "spaces" n'existe que sur Hugging Face. En local, il est absent
# et l'application tourne normalement sur le processeur (CPU).
try:
    import spaces
    SUR_HUGGING_FACE = True
except ImportError:
    SUR_HUGGING_FACE = False

# 1. Modele pre-entraine (Hugging Face Hub)
#    Modele multilingue (dont francais et anglais) a trois classes :
#    negative, neutral, positive
classifieur = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
    top_k=None,  # renvoyer le score des trois classes
    device="cuda" if SUR_HUGGING_FACE else -1,  # GPU sur Spaces, CPU en local
)

# Traduction des etiquettes du modele en francais
traduction = {"positive": "Positif", "negative": "Negatif", "neutral": "Neutre"}


# 2. Fonction Python : recoit le texte, appelle le modele, renvoie les scores
def analyser_sentiment(texte):
    if not texte or not texte.strip():
        return {}
    resultats = classifieur(texte, truncation=True)
    if isinstance(resultats[0], list):  # selon la version de transformers
        resultats = resultats[0]
    return {
        traduction[element["label"].lower()]: float(element["score"])
        for element in resultats
    }


# Sur ZeroGPU, la fonction qui utilise le GPU doit etre marquee @spaces.GPU
if SUR_HUGGING_FACE:
    analyser_sentiment = spaces.GPU(analyser_sentiment)


# 3. Interface Gradio : gr.Textbox en entree, gr.Label en sortie
demo = gr.Interface(
    fn=analyser_sentiment,
    inputs=gr.Textbox(label="Texte a analyser", lines=4,
                      placeholder="Ecrivez une phrase, un avis..."),
    outputs=gr.Label(num_top_classes=3, label="Sentiment predit"),
    title="Analyse de sentiments",
    description="Predit si un texte est positif, negatif ou neutre "
                "a l'aide d'un modele pre-entraine.",
    examples=[
        ["J'adore ce cours, les explications sont tres claires !"],
        ["Ce film etait vraiment nul, j'ai perdu mon temps."],
        ["La reunion est prevue mardi a 10 heures."],
        ["The delivery was fast and the product works perfectly."],
    ],
)

# 4. Lancement du serveur local
if __name__ == "__main__":
    demo.launch()
