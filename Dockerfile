FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

CMD ["sh", "-c", "uv run python -m src.seed && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000"]