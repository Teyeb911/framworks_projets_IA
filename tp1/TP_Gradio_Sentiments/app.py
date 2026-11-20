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
# le paquet "spaces" n'existe que sur Hugging Face. En local, il est absent.
# Le modele tourne toujours sur le processeur (CPU) : il est assez leger, et
# cela evite le quota GPU qui bloque les visiteurs non connectes.
try:
    import spaces

    # ZeroGPU exige au moins une fonction @spaces.GPU au demarrage.
    # Celle-ci n'est jamais appelee : aucun quota GPU n'est consomme.
    @spaces.GPU
    def _exigence_zerogpu():
        pass
except ImportError:
    pass

# 1. Modele pre-entraine (Hugging Face Hub)
#    Modele multilingue (dont francais et anglais) a trois classes :
#    negative, neutral, positive
classifieur = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
    # Meme tokenizer que le modele (XLM-RoBERTa base), mais fourni au format
    # tokenizer.json pret a l'emploi : evite une conversion qui echoue sur
    # Hugging Face Spaces.
    tokenizer="FacebookAI/xlm-roberta-base",
    top_k=None,  # renvoyer le score des trois classes
    device=-1,  # -1 = processeur (CPU)
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
