FROM python:3.12-slim

EXPOSE 7070

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH="${PYTHONPATH}:/project/app"

ENV TZ="Europe/Moscow"

RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*  &&  apt-get clean
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN pip install poetry

COPY pyproject.toml poetry.lock* ./
RUN --mount=type=ssh poetry install
COPY app app
COPY alembic.ini ./
COPY migrations migrations
RUN mkdir logs
RUN mkdir schedules

CMD ["sh", "-c", "alembic upgrade head && python app/main.py"]