FROM python:3.9.7

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY logger ./logger
ADD alembic ./alembic
COPY requirements.txt ./
COPY setup.py ./

COPY config.yml ./
COPY run.sh ./
COPY alembic.ini ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

RUN chmod +x ./run.sh

CMD ["./run.sh"]
