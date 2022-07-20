const {Point} = require('@influxdata/influxdb-client')

function updateDigitalTwinState(client, sensor_id, sensor_value){
  console.log('------updating digital twin state--------');
  return client.connect(err => {
    const collection = client.db("twins_metadata").collection("twins-metadata");
    
    const myQuery = {id: sensor_id};
    const newValues = {$set: {"id": sensor_id, "current_value": sensor_value,
              "last_updated_time": new Date().getTime()}}
    
    collection.updateOne(myQuery, newValues, function(err, res) {
      if (err) throw err;
      console.log("---- 1 document updated ----", res);
    })
  });
}

function writeDataToStore(client, data, mongoClient){

  console.log('writing data ----', data);
  
  updateDigitalTwinState(mongoClient, data['sensor_id'], data['sensor_value']);
  

  const {Point} = require('@influxdata/influxdb-client')
  const org = 'srikar.0896@gmail.com'
  const bucket = 'sensor-data'
  const writeApi = client.getWriteApi(org, bucket)
  writeApi.useDefaultTags({host: 'host1'})


  // const point =  new Point(data['sensor_id']).tag('sensor', data.sensor_tag).stringField('value', data.sensor_value);
  // writeApi.writePoint(point)

  const lightPoint =  new Point('sensor-x21227w').tag('sensor', 1).stringField('value', data.light);
  writeApi.writePoint(lightPoint)

  const movementPoint =  new Point('sensor-2g7ukk4').tag('sensor', 1).stringField('value', data.movement);
  writeApi.writePoint(movementPoint)

  return writeApi
      .close()
      .then(() => {
          console.log('FINISHED')
      })
      .catch(e => {
          console.error(e)
          console.log('Finished ERROR')
      })

  // const p1 =

  // writeClient.writePoint(p1);
}

module.exports.writeDataToStore = writeDataToStore;