FROM python:3.9.7

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY listener ./listener
COPY config.yml ./
COPY run.sh ./
COPY setup.py ./

RUN pip install -e .

RUN chmod +x ./run.sh

CMD ["./run.sh"]
