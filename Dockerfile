FROM python:3.6

WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app/requirements

RUN apt-get update && apt-get install -y libpq5

COPY requirements/ requirements/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY configs/files /

EXPOSE 8080

# TODO: make asgi
CMD ["gunicorn" , "-c", "/etc/gunicorn/gunicorn.py", "ayama.wsgi:application"]
