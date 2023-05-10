FROM python:3.11.2-slim-bullseye AS builder
RUN apt-get update && \
    apt-get update --yes
RUN useradd --create-home optimusprime
USER optimusprime
WORKDIR /home/optimusprime

ENV VIRTUALENV=/home/optimusprime/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=optimusprime pyproject.toml constraints.txt ./

RUN python -m pip install --upgrade pip setuptools && \
    python -m pip install --no-cache-dir -c constraints.txt ".[dev]"

COPY --chown=optimusprime src/ src/
COPY --chown=optimusprime test/ test/

RUN python -m pip install . -c constraints.txt && \
    python -m pytest test/unit/ && \
    python -m bandit -r src/ --quiet && \
    python -m pip wheel --wheel-dir dist/ . -c constraints.txt