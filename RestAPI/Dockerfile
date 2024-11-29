FROM python:3.13-slim

RUN addgroup --system appgroup && adduser --system --group appuser

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIPENV_VENV_IN_PROJECT=1

WORKDIR /app/

RUN python -m pip install --upgrade pip && pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv sync
# RUN pipenv run gunicorn --version

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

CMD ["pipenv", "run", "fastapi", "run", "main.py"]
