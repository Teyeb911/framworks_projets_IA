# Teste le modele sur les phrases du compte rendu (section 4 - Resultats)
# Lancement : python tester.py
from app import analyser_sentiment

phrases = [
    ("J'adore ce cours, les explications sont tres claires !", "Positif"),
    ("Ce film etait vraiment nul, j'ai perdu mon temps.", "Negatif"),
    ("La reunion est prevue mardi a 10 heures.", "Neutre"),
    ("The delivery was fast and the product works perfectly.", "Positif"),
    ("I'm really disappointed with the customer service.", "Negatif"),
    ("Genial, encore une panne de reseau...", "Negatif (ironie)"),
]

print(f"{'Texte':58} | {'Attendu':16} | {'Predit':8} | Confiance")
print("-" * 100)
for texte, attendu in phrases:
    scores = analyser_sentiment(texte)
    predit = max(scores, key=scores.get)
    print(f"{texte[:58]:58} | {attendu:16} | {predit:8} | {scores[predit]*100:.1f} %")
