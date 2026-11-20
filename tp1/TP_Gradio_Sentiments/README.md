# TP Gradio - Classification de sentiments

Cours 2 : Gradio - Framework d'Implementation des Projets IA

## Contenu du dossier

- `app.py` : l'application Gradio (gr.Interface, Textbox -> Label)
- `tester.py` : teste le modele sur 6 phrases et affiche les scores
- `requirements.txt` : dependances
- `compte_rendu.docx` : compte rendu a completer (section 4)
- `captures/` : dossier pour les captures d'ecran

## Etapes dans VS Code

1. Ouvrir le dossier : Fichier > Ouvrir le dossier > `TP_Gradio_Sentiments`
2. Ouvrir un terminal : Terminal > Nouveau terminal
3. Creer et activer l'environnement virtuel :

   Windows :
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   Linux / macOS :
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
   Si Windows bloque l'activation (PowerShell), executer d'abord :
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

4. Installer les dependances :
   ```
   python -m pip install -r requirements.txt
   ```
5. Verifier Gradio :
   ```
   python -c "import gradio; print(gradio.__version__)"
   ```
6. Tester le modele (le premier lancement telecharge environ 1,1 Go) :
   ```
   python tester.py
   ```
   -> recopier les resultats dans le tableau de la section 4 du compte rendu.
7. Lancer l'application :
   ```
   python app.py
   ```
   puis ouvrir http://127.0.0.1:7860 dans le navigateur.
8. Faire les captures d'ecran (Win + Maj + S ou Cmd + Maj + 4)
   et les ranger dans `captures/`, puis les inserer dans le compte rendu.
9. Arreter l'application : Ctrl + C dans le terminal.

Astuce : avec l'extension Python de VS Code, F5 propose
"Lancer l'application Gradio" ou "Tester les phrases".
