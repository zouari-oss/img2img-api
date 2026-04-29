FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install only runtime packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in an isolated venv (cached layer)
COPY requirements.txt .
RUN python -m venv /opt/venv \
  && pip install --upgrade pip \
  && pip install -r requirements.txt

# Download model in a dedicated layer (cached unless ARG changes)
ARG MODEL_PATH=models/anything-v5.safetensors
ARG MODEL_URL=https://huggingface.co/genai-archive/anything-v5/resolve/beb1810cac2af1ba73bea8c65743fe532eae5a5c/anything-v5.safetensors?download=true
RUN set -eux; \
  mkdir -p "$(dirname "$MODEL_PATH")"; \
  if [ ! -f "$MODEL_PATH" ]; then \
  curl -fsSL --retry 5 --retry-delay 2 -o "$MODEL_PATH" "$MODEL_URL"; \
  fi

# Copy application code last for better layer reuse
COPY . .

CMD ["sh", "-c", "fastapi run main.py --host 0.0.0.0 --port ${PORT: 8000}"]
