FROM python:3.11.4

ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py

CMD ["flask", "run"]