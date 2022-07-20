def validate_light_prediction(prediction, payload):
    timestamp = payload['timestamp']
    result = prediction[0]
    if result in ['On', 'Off']:
        return result
    else:
        print('Unrecognized status type')
        return ''
