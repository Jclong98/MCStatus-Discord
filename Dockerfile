FROM python:3.8

LABEL Name=mcstatus

WORKDIR /app
ADD . /app

# Using pip:
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3", "bot.py"]