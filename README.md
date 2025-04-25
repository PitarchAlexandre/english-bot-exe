# 🎧 English Bot – IELTS Oral Exam Practice (Fr)

[English version here](#🌐-english-bot-ielts-oral-exam-practice)

Cette application permet aux étudiants de s'entraîner à l'examen oral de l'IELTS (General English) en simulant des sessions avec un bot vocal. L'objectif est de mettre les utilisateurs en confiance et de les aider à améliorer leur fluidité, leur vocabulaire, leur grammaire et la structuration de leurs réponses. L'application utilise la bibliothèque OpenAI pour évaluer le niveau de l'élève en enregistrant et analysant les réponses et les questions posées.

L'outil utilise la reconnaissance vocale de Whisper pour transcrire les réponses et propose des voix personnalisées via edge-tts, permettant à l'utilisateur de choisir différents accents et voix (homme, femme).


---

## 🔧 Installation (méthode recommandée pour développeurs)

### 1. Cloner le projet ou télécharger les fichiers

Clonez le repo ou téléchargez les fichiers manuellement et placez-les dans un dossier sur votre PC.

### 2. Télécharger et ajouter **FFmpeg**

Téléchargez FFmpeg ici :  
🔗 https://www.ffmpeg.org/download.html

Décompressez le dossier et placez-le **dans le dossier du projet**, avec le nom :

```
ffmpeg-7.1.1
```

> ⚠️ Nécessaire pour manipuler les fichiers audio.

---

### 3. Activer l'environnement virtuel


Créez un environnement virtuel avec cette commande :

```bash
python -m venv venv
```
Puis faîtes les commandes suivantes selon si vous avez Windows, macOS  ou Linux

>Windows :
```bash
.\venv\Scripts\Activate.ps1
```

>macOS/Linux :
```bash
source venv/bin/activate
```

---

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

### 5. Créer un fichier `.env`

Dans le dossier du projet, vous trouverez un fichier nommé `.env.example`. Pour créer votre fichier `.env`, procédez comme suit :

1. **Renommez** le fichier `.env.example` en `.env`.
2. **Ajoutez vos informations personnelles** dans ce fichier comme suit :

```env
ENV_API_KEY=ta_clé_api_ici
ENV_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
ENV_AI_MODEL=gemini-2.0-flash
```
Obtenez une clé gratuite ici :  
🔗 https://aistudio.google.com/app/apikey *(compte Google requis)*

---

### 6. Lancer l'application

```bash
python main.py
```
---
## 💬 Questions ou problèmes ?

N'hésite pas à me contacter ou à ouvrir un "issues" si tu souhaites suggérer des fonctionnalités, signaler des bugs ou contribuer. Bon apprentissage ! 🌟🇬🇧

---

# 🌐 English Bot IELTS Oral Exam Practice

This application enables students to practise for the IELTS (General English) oral exam by simulating sessions with a voice bot. The aim is to give users confidence and help them improve their fluency, vocabulary, grammar and the structure of their answers. The application uses the OpenAI library to assess the student's level by recording and analysing the answers and questions asked.

The tool uses Whisper's speech recognition to transcribe answers and offers personalised voices via edge-tts, allowing the user to choose different accents and voices (male, female).

---

## 🔧 Installation (recommended for developers)

### 1. Clone or download the project files

Clone the repo or manually download the files into a folder.

### 2. Download and add **FFmpeg**

Download FFmpeg here:  
🔗 https://www.ffmpeg.org/download.html

Unzip it and place the folder **inside the project directory** under the name:

```
ffmpeg-7.1.1
```

> ⚠️ Required for audio file processing.

---


### 3. Activate the virtual environment

Use this command to create a virtual environment:

```bash
python -m venv venv
```

Then do the following commands depending on whether you have Windows, macOS or Linux :

>Windows :
```bash
.\venv\Scripts\Activate.ps1
```

>macOS/Linux :
```bash
source venv/bin/activate
```
---

### 5. Create an `.env` file

In the project folder, you will find a file called `.env.example`. To create your `.env` file, proceed as follows:

1. **Rename** the `.env.example` file to `.env`.
2. **Add your personal information** to this file as follows:

```env
ENV_API_KEY=your_api_key_here
ENV_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
ENV_AI_MODEL=gemini-2.0-flash
```
Get a free key here :  
🔗 https://aistudio.google.com/app/apikey *(Google account required)*

Translated with DeepL.com (free version)
---

### 6. Run the app

```bash
python main.py
```
---

## 💬 Questions or issues?

Feel free to reach out or open an issue if you want to suggest features, report bugs, or contribute. Happy learning! 🌟🇬🇧