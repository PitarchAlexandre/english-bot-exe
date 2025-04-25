import os
from dotenv import load_dotenv

class EnvManager:
    def __init__(self, env_file=".env"):
        self.env_file = env_file
        self.env = {}
        self.load()

    def load(self):
        """Charge les variables d'environnement depuis le fichier .env."""
        if os.path.exists(self.env_file):
            with open(self.env_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and not line.strip().startswith("#"):
                        if "=" in line:
                            key, value = line.strip().split("=", 1)
                            self.env[key.strip()] = value.strip()
                            os.environ[key.strip()] = value.strip()
        load_dotenv(dotenv_path=self.env_file)

    def get(self, key):
        """Retourne la valeur d'une variable d'environnement."""
        return self.env.get(key) or os.getenv(key)

    def set(self, key, value):
        """Modifie ou ajoute une variable d'environnement."""
        self.env[key] = value
        os.environ[key] = value
        self.save()

    def save(self):
        """Écrit les variables locales dans le fichier .env."""
        with open(self.env_file, "w", encoding="utf-8") as f:
            for key, value in self.env.items():
                f.write(f"{key}={value}\n")
        print("✅ .env file updated successfully!")

    def display(self):
        """Affiche le contenu actuel du fichier .env."""
        print("📄 Contenu de .env :\n")
        with open(self.env_file, "r", encoding="utf-8") as f:
            print(f.read())
