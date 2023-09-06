FROM python:3.11.4

ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]