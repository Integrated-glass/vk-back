FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8 as base

FROM base as builder

RUN mkdir /install
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
WORKDIR /install
COPY ./app/requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local
RUN apk --no-cache add libpq
RUN apk add bash curl

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80
