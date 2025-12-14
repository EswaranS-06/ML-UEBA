# ---- BASE IMAGE ----
FROM python:3.10-slim

# ---- ENV ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1

# ---- WORKDIR ----
WORKDIR /app

# ---- INSTALL SYSTEM DEPS (minimal) ----
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- COPY PROJECT ----
# We copy everything because backend imports preprocess/nlp/features/ml
COPY . .

# ---- INSTALL UV ----
RUN pip install --no-cache-dir uv

# ---- INSTALL PYTHON DEPS ----
RUN uv sync --frozen

# ---- EXPOSE BACKEND ----
EXPOSE 8000

# ---- START BACKEND ----
CMD ["uv", "run", "backend/main.py"]
