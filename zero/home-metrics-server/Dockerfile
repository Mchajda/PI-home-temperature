FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN chmod -R 755 /app

RUN pip install Flask

EXPOSE 5000

CMD ["python3", "app.py"]

