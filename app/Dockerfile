FROM python:alpine

COPY . /usr/src/code
WORKDIR /usr/src/code
RUN pip install -r requirements.txt

CMD [ "gunicorn", "-c", "gunicorn_config.py", "router:app" ]
