FROM python:3.11-buster

WORKDIR /opt/src
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/opt/src/main.py"]
