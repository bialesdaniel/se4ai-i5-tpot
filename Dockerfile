FROM python:3.8-slim-buster
RUN apt-get update

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy relevant files for training into the container
COPY movie-data.csv ratings-data.csv users-data.csv ./
COPY pipelines pipelines
COPY transformers transformers
COPY config config
COPY training training
COPY optimize-pipeline.py ./

# specify any non-default environment variables found in config/config.py
ENV TRAINING_SIZE=1000
ENV GENERATIONS=10
ENV POPULATION_SIZE=10
ENV VERBOSITY=2

ENTRYPOINT python optimize-pipeline.py
