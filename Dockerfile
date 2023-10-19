FROM python:3.11.3-slim

WORKDIR /src

EXPOSE 8001

# python:
ENV PYTHONUNBUFFERED=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_ROOT_USER_ACTION=ignore \
  # poetry:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
  curl \
  git  \
  openssh-client

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
