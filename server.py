import json
import pika, sys, os

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

def get_minor_major(data):
    return [max(data), min(data)]

def send_response(payload):
    string_payload = json.dumps(payload)
    channel.basic_publish(exchange='',
                      routing_key='result_queue',
                      body=string_payload)
    print(" [x] Sent response: " + str(payload["data"]))

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        # parse json from body
        body = json.loads(body)
        # get data from body
        print(" [x] Received packet from client: " + str(body['client_id']))
        data = body['data']
        print(data)
        body["data"] = get_minor_major(data)
        send_response(body)

    channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
