# --- Étape 1 : Builder (Construction) ---
# On utilise une image Python complète pour compiler les dépendances [cite: 64]
FROM python:3.11-slim AS builder

# Définition du répertoire de travail
WORKDIR /build

# Installation des dépendances dans un dossier local [cite: 65]
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Étape 2 : Runtime (Exécution) ---
# Image de base très légère (Alpine) [cite: 67]
FROM python:3.11-alpine

# Définition du répertoire de travail [cite: 25]
WORKDIR /app

# Création d'un utilisateur non-root pour la sécurité [cite: 68]
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# On récupère uniquement les bibliothèques installées dans l'étape précédente [cite: 68]
COPY --from=builder /root/.local /home/appuser/.local
# Mise à jour du PATH pour trouver les paquets Python
ENV PATH=/home/appuser/.local/bin:$PATH

# Copie du code source de l'API avec les bons droits [cite: 26, 68]
COPY --chown=appuser:appgroup app/ ./app/

# On utilise l'utilisateur non-root [cite: 68]
USER appuser

# Exposition du port 5000 [cite: 69]
EXPOSE 5000

# Commande pour lancer l'application [cite: 51]
CMD ["python", "app/main.py"]
