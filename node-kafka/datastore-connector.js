const {InfluxDB} = require('@influxdata/influxdb-client')

function getDataWriteClient(){
  const {InfluxDB} = require('@influxdata/influxdb-client')

  // You can generate an API token from the "API Tokens Tab" in the UI
  const token = process.env.INFLUX_TOKEN
  const org = 'srikar.0896@gmail.com'
  const bucket = 'sensor-data'

  const client = new InfluxDB({url: 'https://us-east-1-1.aws.cloud2.influxdata.com', token: token})

  return client;
}

module.exports.getDataWriteClient = getDataWriteClient;