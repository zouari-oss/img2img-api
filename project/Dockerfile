FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
  curl \
  git \
  && rm -rf /var/lib/apt/lists/*

# Python dependencies layer (cached)
COPY requirements.txt .

RUN python -m venv /opt/venv \
  && /opt/venv/bin/pip install --upgrade pip \
  && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# Create model directories early (cached layer)
RUN mkdir -p models/Stable-diffusion

# Download model (cached unless ARG changes)
ARG MODEL_PATH=models/anything-v5.safetensors
ARG MODEL_URL=https://huggingface.co/genai-archive/anything-v5/resolve/beb1810cac2af1ba73bea8c65743fe532eae5a5c/anything-v5.safetensors?download=true

RUN if [ ! -f "$MODEL_PATH" ]; then \
  echo "Downloading model..." && \
  mkdir -p models && \
  curl -L --retry 3 --retry-delay 2 -o "$MODEL_PATH" "$MODEL_URL"; \
  else \
  echo "Model already exists, skipping download"; \
  fi

# Copy project files last (best caching)
COPY . .

# Default command (change if needed)
CMD ["bash"]
