const { Kafka } = require("kafkajs");
const { getDataWriteClient } = require("./datastore-connector");
const { writeDataToStore } = require("./datastore-writer");
const { client:mongoClient } = require("./mongoClient");

run().then(() => console.log("Done"), err => console.log(err));


async function run() {
  const kafka = new Kafka({ brokers: ["localhost:9092"] });
  // If you specify the same group id and run this process multiple times, KafkaJS
  // won't get the events. That's because Kafka assumes that, if you specify a
  // group id, a consumer in that group id should only read each message at most once.
  const consumer = kafka.consumer({
    groupId: 'my-group'
  });
  const dataWriteClient = getDataWriteClient();

  await consumer.connect();

  const app = require('express')();
  const http = require('http').Server(app);
  const io = require('socket.io')(http);
  const port = 3002;
  
  http.listen(port, () => {
    console.log(`Socket.IO server running at http://localhost:${port}/`);
  });
  
  app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
  });

  const getParsedData = (message) => {
    const sensorId = message.split(',')[0]
    const result = {};
  
    result['sensor_id'] = sensorId;
  
    var tag2Phrase= /tag1=(.*)/;
    var valuePhrase = /value=(.*)/;
    const sensorTag = message.match(tag2Phrase)[1].split(',')[0];
    
    result['sensor_tag'] = sensorTag;
    if(sensorTag === 'movement'){
      result['sensor_value'] = message.match(valuePhrase)[1].split(" ")[0] === '"no"' ? 'no' : 'yes';
    } else {
      result['sensor_value'] = message.match(valuePhrase)[1].split(" ")[0] === '"Off"' ? 'Off' : 'On';
    }

    result['timestamp'] = Number(message.match(valuePhrase)[1].split(" ")[1]);
  
    console.log('Emitting Event --', result);
    return result;


    // result['sensor_tag'] = message.match(tag2Phrase)[1][0];
    // if(messageType === 'light'){
    //   result['sensor_value'] = message.match(valuePhrase)[1].split(" ")[0] === '"Off"' ? 'Off' : 'On';
    // }
    // if(messageType === 'movement'){
    //   result['sensor_value'] = message.match(valuePhrase)[1].split(" ")[0] === '"no"' ? 'no' : 'yes';
    // }
    // result['timestamp'] = Number(message.match(valuePhrase)[1].split(" ")[1]);
  
    // return result;
  };

  io.on('connection', async (socket) => {
    console.log('connection!!')
    await consumer.subscribe({ topic: "timestamp"});
    await consumer.run({ 
      eachMessage: async (data) => {
        const parsedData = getParsedData(data.message.value.toString());
        console.log(parsedData);
        writeDataToStore(dataWriteClient, parsedData, mongoClient);
        io.emit("event", parsedData);
      }
    });
  });

  io.on('close', () => {
    void setTimeout(() => {
      dataWriteClient.flush();
    }, 5000)
  });

}
