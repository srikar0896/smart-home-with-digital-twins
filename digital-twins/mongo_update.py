import pymongo
import time

client = pymongo.MongoClient(
    "mongodb://devuser:devuser123@cluster0-shard-00-00.xzsyp.mongodb.net:27017,cluster0-shard-00-01.xzsyp.mongodb.net:27017,cluster0-shard-00-02.xzsyp.mongodb.net:27017/?ssl=true&replicaSet=atlas-7tx4dz-shard-0&authSource=admin&retryWrites=true&w=majority")

mydb = client["twins_metadata"]
mycol = mydb["twins-metadata"]

# mydict = {"id": 'sensor-x21227w', "current_value": 'on',
#           "last_updated_time": time.time()}

# x = mycol.insert_one(mydict)

# mydict = {"id": 'sensor-2g7ukk4', "current_value": 'yes',
#           "last_updated_time": time.time()}

# x = mycol.insert_one(mydict)

# mydict = {"id": 'sensor-x21227w', "current_value": 'on',
#           "last_updated_time": time.time()}

# x = mycol.insert_one(mydict)

x = mycol.find_one_and_update(
    {
        "id": 'sensor-x21227w'
    },
    {
        '$set': {"current_value": 'On'}
    },
    upsert=False
)

# https://data.mongodb-api.com/app/data-pfobr/endpoint/data/v1
