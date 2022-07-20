const { MongoClient, ServerApiVersion } = require('mongodb');
const uri = "mongodb+srv://devuser:devuser123@cluster0.xzsyp.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });

module.exports.client = client;