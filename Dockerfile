FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN apt-get update && apt-get install -y libgdal-dev 

RUN poetry install --no-root

CMD ["python3", "-m", "api.main"]