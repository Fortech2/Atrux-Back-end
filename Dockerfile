FROM python:3.11.4

ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 50000

ENV FLASK_APP=app.py

CMD ["python3", "app.py"]