FROM --platform=linux/amd64 python:3.9-slim

RUN apt-get update && apt-get install -y curl bash python3-pip autoconf autogen libtool libffi-dev libssl-dev make swig meson cmake zsh gcc

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

RUN pip install poetry

COPY x21e8 /x21e8
COPY poetry.lock pyproject.toml ./
COPY external_packages_armv7 /external_packages_armv7

RUN poetry config virtualenvs.create false
RUN poetry install --no-root
RUN poetry shell

EXPOSE 8000:8000

RUN adduser --system --group nonroot
USER nonroot

CMD ["uvicorn", "x21e8.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "240", "--log-level=debug"]
