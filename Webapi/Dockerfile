FROM gcr.io/datamechanics/spark:platform-3.1-dm14
# Install apt dependencies
ENV PYSPARK_MAJOR_PYTHON_VERSION=3
# Install requirements
COPY requirements.txt requirements.txt
USER root
RUN apt-get update -y && apt install build-essential -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5500
WORKDIR /app
ENTRYPOINT python main.py

