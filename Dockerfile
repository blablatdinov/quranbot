FROM python:3.10 as base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

FROM base as poetry
RUN pip install poetry==1.2.2
COPY poetry.lock pyproject.toml /app/
RUN poetry export --without dev -o requirements.txt

FROM base as runtime
COPY --from=poetry /app/requirements.txt /tmp/requirements.txt
RUN apt-get install gcc libffi-dev
RUN cat /tmp/requirements.txt
RUN python -m venv /app/.venv && \
    /app/.venv/bin/pip install 'wheel==0.36.2' && \
    /app/.venv/bin/pip install -r /tmp/requirements.txt
# Creating folders, and files for a project:
COPY . /app
