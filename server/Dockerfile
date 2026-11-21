FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 BLENDER_BIN=/usr/bin/blender
RUN apt-get update && apt-get install -y --no-install-recommends \
    blender libegl1 libgl1 libx11-6 libxi6 libxrender1 libxxf86vm1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["blender-env-server", "--host", "0.0.0.0", "--port", "8000"]
