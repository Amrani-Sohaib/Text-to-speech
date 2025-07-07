# Text to Speech Project

## Description
Ce projet utilise l'intelligence artificielle pour convertir du texte en parole, créer des voice-overs et entraîner des IA sur des voix afin de les reproduire à des fins non lucratives.

## Fonctionnalités
- Conversion de texte en parole
- Création de voice-overs
- Entraînement de modèles IA sur des voix spécifiques
- Reproduction de voix pour des applications non lucratives

## Prérequis
- Python 3.x
- Bibliothèques nécessaires (voir `requirements.txt`)

## Installation
1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Amrani-Sohaib/text-to-speech.git
    ```
2. Accédez au répertoire du projet :
    ```bash
    cd text-to-speech
    ```
3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation
1. Pour convertir du texte en parole :
    ```bash
    python text_to_speech.py --text "Votre texte ici"
    ```
2. Pour créer un voice-over :
    ```bash
    python voice_over.py --input "fichier_audio.mp3" --text "Votre texte ici"
    ```
3. Pour entraîner un modèle IA sur une voix spécifique :
    ```bash
    python train_model.py --data "dossier_de_données"
    ```
