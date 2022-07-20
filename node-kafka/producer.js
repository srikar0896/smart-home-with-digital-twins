const { Kafka, CompressionTypes, logLevel } = require('kafkajs')

// const host = "http://localhost"

const kafka = new Kafka({
  logLevel: logLevel.DEBUG,
  brokers: ["localhost:9092"],
  clientId: 'example-producer',
})

const topic = 'timestamp'
const producer = kafka.producer()

let data;
let cursor = 0;

const fs = require('fs')
const inputPath = "/Users/srikar/Desktop/workspace/graduate_project/node-kafka/data.csv";

const getRandomNumber = () => Math.round(Math.random(10) * 1000)

const formatBooleanToOnOff = (BooleanString) => BooleanString === 'False' ? 'no' : 'yes';

const createMessage = (data) => {
  const dataRow = JSON.stringify({
    data: data[cursor].split(","),
  });
  console.log('data--', dataRow);
  cursor += 1;
  return ({
    key: cursor.toString(),
    value: dataRow
  })
}


const getLightSensorMessage = (data, timestamp) => {
  
  const dataRow = JSON.stringify({
    data: data[cursor].split(","),
  });
  const JSONParsed = JSON.parse(dataRow).data;
  console.log('JSON parsed', JSONParsed);
  // cursor += 1;
  return ({
    key: cursor.toString(),
    value: `sensor-x21227w,tag1=light,tag2=1 value="${JSONParsed[3]}" ${timestamp}`,
  })
};

const getMovementSensorMessage = (data, timestamp) => {
  const dataRow = JSON.stringify({
    data: data[cursor].split(","),
  });
  const JSONParsed = JSON.parse(dataRow).data;
  return ({
    key: cursor.toString(),
    value: `sensor-2g7ukk4,tag1=movement,tag2=1 value="${JSONParsed[2]}" ${timestamp}`,
  })
};

// const getTimestampMessage = (data) => {
//   const dataRow = JSON.stringify({
//     data: data[cursor].split(","),
//   });
//   console.log('timestamp data-', dataRow.data[0]);
//   cursor += 1;
//   return ({
//     key: cursor.toString(),
//     value: dataRow.data[0]
//   })
// };

const sendMessage = (data) => {
  const timestamp = new Date().getTime() * 1000000;
  const lightSensorBroadcastMessage = getLightSensorMessage(data, timestamp);
  const movementSensorBroadcastMessage = getMovementSensorMessage(data, timestamp);
  console.log('sensor to send values -', lightSensorBroadcastMessage, movementSensorBroadcastMessage);
  return producer
    .send({
      topic,
      compression: CompressionTypes.GZIP,
      // messages: [createMessage(data)],
      messages: [lightSensorBroadcastMessage, movementSensorBroadcastMessage],
    })
    .then(() => {
      cursor += 1
      console.log('cursorr--', cursor)
    })
    .catch(e => console.error(`[example/producer] ${e.message}`, e))
}

const run = async () => {
  await producer.connect()
  fs.readFile(inputPath, 'utf8', function (err, data) {
    var dataArray = data.split(/\r?\n/);  //Be careful if you are in a \r\n world...
    // Your array contains ['ID', 'D11', ... ]
    setInterval(() => sendMessage(dataArray), 5000)
  })  
}

run().catch(e => console.error(`[example/producer] ${e.message}`, e))

const errorTypes = ['unhandledRejection', 'uncaughtException']
const signalTraps = ['SIGTERM', 'SIGINT', 'SIGUSR2']

errorTypes.forEach(type => {
  process.on(type, async () => {
    try {
      console.log(`process.on ${type}`)
      await producer.disconnect()
      process.exit(0)
    } catch (_) {
      process.exit(1)
    }
  })
})

signalTraps.forEach(type => {
  process.once(type, async () => {
    try {
      await producer.disconnect()
    } finally {
      process.kill(process.pid, type)
    }
  })
})




// const { Kafka, CompressionTypes, logLevel } = require('kafkajs')

// //const host = process.env.HOST_IP || ip.address()

// const kafka = new Kafka({
//   logLevel: logLevel.DEBUG,
//   brokers: [`localhost:9092`],
//   clientId: 'example-producer',
// })

// const topic = 'timestamp'
// const producer = kafka.producer()

// const getRandomNumber = () => Math.round(Math.random(10) * 1000)
// const createMessage = num => ({
//   key: `key-${num}`,
//   value: `${num}`,
// })

// const sendMessage = () => {
//   return producer
//     .send({
//       topic,
//       compression: CompressionTypes.None,
//       messages: [createMessage(getRandomNumber())],
//     })
//     .then(console.log)
//     .catch(e => console.error(`[example/producer] ${e.message}`, e))
// }

// const run = async () => {
//   await producer.connect()
//   setInterval(sendMessage, 6000)
// }

// run().catch(e => console.error(`[example/producer] ${e.message}`, e))

// const errorTypes = ['unhandledRejection', 'uncaughtException']
// const signalTraps = ['SIGTERM', 'SIGINT', 'SIGUSR2']

// errorTypes.forEach(type => {
//   process.on(type, async () => {
//     try {
//       console.log(`process.on ${type}`)
//       await producer.disconnect()
//       process.exit(0)
//     } catch (_) {
//       process.exit(1)
//     }
//   })
// })

// signalTraps.forEach(type => {
//   process.once(type, async () => {
//     try {
//       await producer.disconnect()
//     } finally {
//       process.kill(process.pid, type)
//     }
//   })
// })