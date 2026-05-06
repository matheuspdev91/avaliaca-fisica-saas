FROM python:3.11-slim

# Evita buffer no Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gifsicle \
    && rm -rf /var/lib/apt/lists/*

# Diretório do app
WORKDIR /app

# Copia dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Porta Django
EXPOSE 8000

# Produção com Gunicorn
CMD ["gunicorn", "projeto.wsgi:application", "--bind", "0.0.0.0:8000"]
