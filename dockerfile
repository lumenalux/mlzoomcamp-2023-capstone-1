FROM python:3.10-slim-bullseye

WORKDIR /usr/src/app
COPY Pipfile* ./

RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir pipenv && \
  pipenv install --deploy --ignore-pipfile

COPY . .

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  NAME=World

EXPOSE 5000

CMD ["pipenv", "run", "python", "predict.py"]
