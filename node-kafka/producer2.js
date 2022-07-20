// const { Kafka,  CompressionTypes, logLevel } = require("kafkajs");
// const { getDataWriteClient } = require("./datastore-connector");
// const { writeDataToStore } = require("./datastore-writer");
// const { client:mongoClient } = require("./mongoClient");

// run().then(() => console.log("Done"), err => console.log(err));

// const kafka = new Kafka({
//   logLevel: logLevel.DEBUG,
//   brokers: ["localhost:9092"],
//   clientId: 'example-producer',
// })

// const topic = 'timestamp'
// const producer = kafka.producer()

// async function run() {
  

//   const app = require('express')();
//   const http = require('http').Server(app);
//   const io = require('socket.io')(http);
//   const port = 3004;
  
//   http.listen(port, () => {
//     console.log(`Socket.IO server running at http://localhost:${port}/`);
//   });
  
//   io.on('iot-event', (params) => {
//     console.log('params - ', params);
//     return producer
//     .send({
//       topic,
//       compression: CompressionTypes.GZIP,
//       // messages: [createMessage(data)],
//       messages: [lightSensorBroadcastMessage, movementSensorBroadcastMessage],
//     })
//     .then(() => {
//       cursor += 1
//       console.log('cursorr--', cursor)
//     })
//     .catch(e => console.error(`[example/producer] ${e.message}`, e))
//   });

//   io.on('connection', async (socket) => {
//     // await producer.connect()
//     run().catch(e => console.error(`[example/producer] ${e.message}`, e))
//   });

//   io.on('close', () => {
//     void setTimeout(() => {
//       dataWriteClient.flush();
//     }, 5000)
//   });

// }


const { Kafka,  CompressionTypes, logLevel } = require("kafkajs");


const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);

const PORT = 3005;

const kafka = new Kafka({
  logLevel: logLevel.DEBUG,
  brokers: ["localhost:9092"],
  clientId: 'example-producer',
})

const topic = 'timestamp'
const producer = kafka.producer()


app.get('/', function(req, res) {
   res.sendfile('index.html');
});

io.on('iot-event', function(data) {
  console.log('iot-event', data);
})
let count = 0;
//Whenever someone connects this gets executed
io.on('connection', function(socket) {
    console.log('A user connected');
    producer.connect()

    socket.on('iot-event', function(data) {
      console.log('iot-event(socker)', data);
      const lightSensorBroadcastMessage = {
        key: count.toString(),
        value: `sensor-x21227w,tag1=light,tag2=1 value="${data['light']}" ${new Date().getTime()}`,
      };
      const dataToSend = {
        key: count.toString(),
        value: JSON.stringify(data),
      };
      console.log('dataToSend', dataToSend);
      return producer
    .send({
        topic,
        compression: CompressionTypes.GZIP,
        // messages: [createMessage(data)],
        messages: [dataToSend],
      })
      .then(() => {
        count += 1
        console.log('count --', count)
      })
      .catch(e => console.error(`[example/producer] ${e.message}`, e))
      })

   //Whenever someone disconnects this piece of code executed
   socket.on('disconnect', function () {
      console.log('A user disconnected');
   });
});

http.listen(PORT, function() {
   console.log('listening on *:', PORT);
});