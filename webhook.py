from asyncio import log
from flask import Flask, request, Response
from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['192.168.12.122:4444'])
# Asynchronous by default
future = producer.send('my-topic', b'raw_bytes')
app = Flask(__name__)
@app.route('/pac_webhook', methods=['POST'])
def return_response():
    print(request.json);
    ## Do something with the request.json data.
    producer.send('my-topic', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)
    return Response(status=200)
def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)
    # handle exception
if __name__ == "__main__": app.run()