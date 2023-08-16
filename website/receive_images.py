import pika, os
import PIL.Image as Image
import io
import base64
import random
import string
import json


url = os.environ.get('CLOUDAMQP_URL', 'amqps://zqbavobe:8LsWyHTXCdM2lFB0AbUS-540BCdksEBM@cow.rmq2.cloudamqp.com/zqbavobe')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
def callback(ch, method, properties, body):
    json_data = json.loads(body)
    image_str : str = json_data['image']
    uuid = json_data['image']
    #img = Image(filename="poza.png")
    print(len(image_str))
    image_str = image_str[2:]
    image_str = image_str[:-1]
    print(len(image_str))
    raw_bytes = base64.b64decode(image_str)
    #b = base64.b64decode(raw_bytes)
    #print(raw_bytes)
    #img = Image.open(io.BytesIO(raw_bytes))
    #img.save('nume_poza.png')
    with open("poze.jpg", "wb") as binary_file:
        binary_file.write(raw_bytes)
        binary_file.close()



channel.basic_consume('hello',
                      callback,
                      auto_ack=True)
print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()