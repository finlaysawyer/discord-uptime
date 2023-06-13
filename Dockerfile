FROM python:3.8.17-slim-bullseye

COPY . /app/

RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["python3", "bot.py"]
