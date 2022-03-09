import json
from math import sqrt
import random
import string
import sys
import pika

MAX_POSITIONS = 100

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


#generate random alfanumeric string

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

connection.close()