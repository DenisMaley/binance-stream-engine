FROM python:3.9.7

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config.yml ./
COPY runner.py ./
COPY run.sh ./

RUN chmod +x ./run.sh

CMD ["./run.sh"]
