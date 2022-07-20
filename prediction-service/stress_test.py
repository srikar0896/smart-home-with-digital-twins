from light_prediction_model import predict_light
import time
from utilities.format_light_prediction import format as format_light_prediction

execution_times = []


def get_prediction():
    st = time.time()

    params = {
        "movement_status": "yes",
        "timestamp": 68760,
        "light_status": "On",
        "room_label": "Room 1"
    }
    recommendation = predict_light(
        params['movement_status'], params['timestamp'])
    et = time.time()
    elapsed_time = et - st
    execution_times.append(elapsed_time)
    return format_light_prediction(recommendation[0], params)


for i in range(100):
    get_prediction()

print('execution times', execution_times)
