FROM python:3.12-slim
WORKDIR /app

COPY ./app /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]