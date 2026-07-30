FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    jq \
    python3 \
    python3-pip \
    ffmpeg \
    poppler-utils \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages \
    pymupdf \
    pillow \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5 \
    requests==2.32.3

# Copy skills to all agent framework paths
COPY skills /root/.claude/skills
RUN mkdir -p /root/.codex/skills /root/.opencode/skills /root/.goose/skills /root/.factory/skills /root/.agents/skills /root/.gemini/skills /root/.cursor/skills && cp -a /root/.claude/skills/. /root/.codex/skills/ && cp -a /root/.claude/skills/. /root/.opencode/skills/ && cp -a /root/.claude/skills/. /root/.goose/skills/ && cp -a /root/.claude/skills/. /root/.factory/skills/ && cp -a /root/.claude/skills/. /root/.agents/skills/ && cp -a /root/.claude/skills/. /root/.gemini/skills/ && cp -a /root/.claude/skills/. /root/.cursor/skills/

# Copy persona
COPY persona /root/.openclaw/persona

# Copy multimodal artifacts
COPY artifacts/inputs/files /app/artifacts/inputs/files

WORKDIR /app
