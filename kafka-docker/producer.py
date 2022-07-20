import json
from kafka import KafkaProducer
from datetime import datetime
from time import sleep, time
from bson import json_util

from TimestampEvent import TimestampEvent

# the frequency with which we want to produce the events
waitTime = 1


def serializer(x):
    print('data--', json.dumps(x.__dict__).encode('utf-8'))
    return json.dumps(x.__dict__).encode('utf-8')


producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=serializer)

while True:
    timestampEvent = TimestampEvent(datetime.now().strftime("%H:%M:%S"))
    print("Sending: " + timestampEvent.timestamp)
    # data = {'tag ': 'blah',
    #         'name': 'sam',
    #         'timestamp': timestampEvent.timestamp,
    #         }
    # jd = json.dumps(data)
    producer.send('timestamp', timestampEvent)
    producer.flush()
    sleep(1)
