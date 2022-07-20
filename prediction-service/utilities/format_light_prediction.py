# The utility function takes the prediction input
# and formats it with a proper message
from utilities.validation import validate_light_prediction


def format(prediction, payload):
    pred = []
    if prediction[0] == 'Off':
        pred = ['On', 'Switch On']
    if prediction[0] == 'On':
        pred = ['Off', 'Switch Off']
    print('recommendation', pred)
    result = validate_light_prediction(pred, payload)
    print('result', result)
    if result == payload['light_status']:
        return ''
    message = 'Please turn the light in ' + \
        payload['room_label'] + ' ' + result
    return message
