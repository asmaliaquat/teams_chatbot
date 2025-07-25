# Use official Python slim image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.2
ENV MISTRAL_API_KEY=
ENV OPENAI_API_KEY=
ENV MICROSOFT_APP_ID=
ENV MICROSOFT_APP_PASSWORD=

# Set working directory
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    curl build-essential gcc \
    && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY . /app/

RUN pip install -r requirements.txt

# Expose app port
EXPOSE 8000

# Run the bot via uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]