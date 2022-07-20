const getParsedData = (message) => {
  console.log('message', message.split(','));
  const sensorId = message.split(',')[0]
  const result = {};

  result['sensor_id'] = sensorId;

  var tag2Phrase= /tag1=(.*)/;
  var valuePhrase = /value=(.*)/;
  console.log(message.match(tag2Phrase));
  console.log(message.match(valuePhrase));
  result['sensor_tag'] = message.match(tag2Phrase)[1].split(',')[0];
  result['sensor_value'] = message.match(valuePhrase)[1].split(" ")[0] === '"no"' ? 'no' : 'yes';
  result['timestamp'] = Number(message.match(valuePhrase)[1].split(" ")[1]);

  return result;
};

const lightMessage = 'sensor-x21227,tag1=light,tag2=1 value="On" 1658117991158000000';
const movementMessage = 'movement,tag1=sensor,tag2=1 value="no" 1657814994902000000';

console.log(getParsedData(lightMessage));