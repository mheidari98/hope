FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app