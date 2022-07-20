# app.py
import os
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS

from light_prediction_model import predict_light
from utilities.format_light_prediction import format as format_light_prediction

import requests


app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/status")
def get_status():
    return 'Service is up and running!'


@app.route("/get-twins")
def get_twins():
    import pymongo

    client = pymongo.MongoClient(
        "mongodb://devuser:devuser123@cluster0-shard-00-00.xzsyp.mongodb.net:27017,cluster0-shard-00-01.xzsyp.mongodb.net:27017,cluster0-shard-00-02.xzsyp.mongodb.net:27017/?ssl=true&replicaSet=atlas-7tx4dz-shard-0&authSource=admin&retryWrites=true&w=majority")

    mydb = client["twins_metadata"]
    mycol = mydb["digital-twins"]
    x = list(mycol.find({}))

    metadatax = mydb["twins-metadata"]
    y = list(metadatax.find({}))

    print('metadata', y)
    return jsonify({
        'status': 200,
        'twins': str(x),
        'metadata': str(y)
    })


def get_light_recommendations(params):
    recommendation = predict_light(
        params['movement_status'], params['timestamp'])
    return format_light_prediction(recommendation[0], params)


@app.route("/get-recommendations", methods=['POST'])
def get_recommendations():
    if request.method == 'POST':
        # run validations before returning recommendations
        payload = request.get_json()

        print(payload)

        recommendations = []

        light_recommendation = get_light_recommendations(
            payload['home_params'])

        if not light_recommendation == '':
            recommendations.append(light_recommendation)
        # insert each recommendation into the db to take feedback

        return jsonify({
            'status': 200,
            'recommendations': recommendations
        })


@ app.route("/feedback", methods=['POST'])
def take_feedback():
    return jsonify({
        'status': 200,
        'response': 'Thank you for your feedback!'
    })


if __name__ == "__main__":
    app.run()
