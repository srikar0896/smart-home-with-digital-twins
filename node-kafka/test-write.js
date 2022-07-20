const { getDataWriteClient } = require("./datastore-connector");

const { writeDataToStore } = require("./datastore-writer");

const dataWriteClient = getDataWriteClient();

const data = {
  sensor_id: 'sensor-2g7ukk4',
  sensor_tag: 'movement',
  sensor_value: 'yes',
  timestamp: 1658126383246000000
}

writeDataToStore(dataWriteClient, data);

console.log('writing data ----', data);
