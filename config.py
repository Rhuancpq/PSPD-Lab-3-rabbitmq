
from math import sqrt
import sys
import pika

MAX_POSITIONS = 100

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue')
channel.queue_declare(queue='result_queue')

connection.close()