FROM python:3.7-alpine

LABEL Name=mcstatus Version=0.0.1

WORKDIR /app
ADD . /app

# Using pip:
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3", "bot.py"]