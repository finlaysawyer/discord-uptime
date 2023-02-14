FROM python:3.8.16-slim-bullseye

LABEL maintainer alsoGAMER <alsogamer3@gmail.com>

COPY . /app/

RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["python3", "bot.py"]
