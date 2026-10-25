FROM python:3.11-slim

# Création d'un utilisateur non-root (E13 du cahier des charges)
RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# On donne les droits à l'utilisateur
RUN chown -R appuser:appuser /app
USER appuser

# L'API écoute sur le port 8000
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]