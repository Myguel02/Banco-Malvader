# Imagem base
FROM python:3.11

# Pasta de trabalho
WORKDIR /app

# Copiar requirements primeiro (melhora cache)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do projeto
COPY . .

# Variáveis de ambiente para o CustomTkinter
ENV DISPLAY=:0

# Comando principal
CMD ["python", "main.py"]
