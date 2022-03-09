import json
from math import sqrt
import random
import string
from threading import Lock
import sys
import pika

MAX_POSITIONS = 100

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


# generate random alfanumeric string

client_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) 

print("Starting tasks for client: " + client_id)

arr = [sqrt((i - MAX_POSITIONS/2)**2) for i in range(MAX_POSITIONS)]
# get from params
# or defaut value 
number_packets = 10
if len(sys.argv) > 1:
    number_packets =  int(sys.argv[1])

# divide array in packets of work

items_per_packet = int(MAX_POSITIONS/number_packets)
remainder = MAX_POSITIONS % number_packets

packets = []
for x in range(0, number_packets):
    start = x * items_per_packet
    end = start + items_per_packet
    if x == number_packets - 1:
        end = end + remainder
    packets.append(arr[start:end])


# send packets to queue

for idx in range(0, len(packets)):
    # payload: {'client_id': client_id, 'packet_id': packet_id, 'data': data}
    payload = {
        'client_id': client_id,
        'packet_id': idx,
        'data': packets[idx]
    }
    # transform to json
    string_payload = json.dumps(payload)
    channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=string_payload)
    print(" [x] Sent packet: " + str(packets[idx]))


# receive results from queue result_queue
# payload: {'client_id': client_id, 'packet_id': packet_id, 'data': {'first': first, 'last': last}}

resp_packets = []
received_packets = 0
received_packets_lock = Lock()
def callback(ch, method, properties, body):
    global received_packets, received_packets_lock, resp_packets, number_packets
    # parse json from body
    body = json.loads(body)
    # get data from body
    print(" [x] Received packet with client_id: " + str(body['client_id']))
    data = body['data']
    received_packets_lock.acquire()
    received_packets += 1
    resp_packets.append(data)
    received_packets_lock.release()
    if received_packets == number_packets:
        print(" [x] Received all packets")
        ch.stop_consuming()

# start consuming
channel.basic_consume(queue='result_queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

new_arr = []
for idx in range(0, len(resp_packets)):
    new_arr.extend(resp_packets[idx])


# create other packet with new_arr
payload = {
    'client_id': client_id,
    'packet_id': len(resp_packets),
    'data': new_arr
}
# transform to json
string_payload = json.dumps(payload)
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=string_payload)
print(" [x] Sent final packet: " + str(new_arr))

received_packets = 0
resp_packets = []
packets = [].append(new_arr)
number_packets = 1

channel.basic_consume(queue='result_queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

connection.close()

print(" [x] Received final packet!")
print("min: " + str(resp_packets[0][0]) + " max: " + str(resp_packets[0][1]))

