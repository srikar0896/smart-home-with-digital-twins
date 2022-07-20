import pymongo
import time

client = pymongo.MongoClient(
    "mongodb://devuser:devuser123@cluster0-shard-00-00.xzsyp.mongodb.net:27017,cluster0-shard-00-01.xzsyp.mongodb.net:27017,cluster0-shard-00-02.xzsyp.mongodb.net:27017/?ssl=true&replicaSet=atlas-7tx4dz-shard-0&authSource=admin&retryWrites=true&w=majority")

mydb = client["twins_metadata"]
mycol = mydb["digital-twins"]

# mydict = {"id": 'sensor-x21227w',
#           "label": "Room 1 light", "sensor_type": "light"}

# x = mycol.insert_one(mydict)


# mydict = {"id": 'sensor-2g7ukk4',
#           "label": "Room 1 movement", "sensor_type": "movement"}

# x = mycol.insert_one(mydict)

mydict = {"id": 'sensor-a56sot2',
          "label": "Coffee maker", "sensor_type": "coffee_maker"}

x = mycol.insert_one(mydict)

# https://data.mongodb-api.com/app/data-pfobr/endpoint/data/v1
