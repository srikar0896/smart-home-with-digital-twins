const {InfluxDB, Point} = require('@influxdata/influxdb-client')

const token = process.env.INFLUXDB_TOKEN
const url = 'https://us-east-1-1.aws.cloud2.influxdata.com'

const client = new InfluxDB({url, token})


let org = `srikar.0896@gmail.com`
let bucket = `sensor-data`


let queryClient = client.getQueryApi(org)
let fluxQuery = `from(bucket: "sensor-data")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")`

queryClient.queryRows(fluxQuery, {
  next: (row, tableMeta) => {
    const tableObject = tableMeta.toObject(row)
    console.log(tableObject)
  },
  error: (error) => {
    console.error('\nError', error)
  },
  complete: () => {
    console.log('\nSuccess')
  },
})



// Aggregate query

// ----------------------------------------------------------------
// queryClient = client.getQueryApi(org)
// fluxQuery = `from(bucket: "sensor-data")
//  |> range(start: -10m)
//  |> filter(fn: (r) => r._measurement == "measurement1")
//  |> mean()`

// queryClient.queryRows(fluxQuery, {
//   next: (row, tableMeta) => {
//     const tableObject = tableMeta.toObject(row)
//     console.log(tableObject)
//   },
//   error: (error) => {
//     console.error('\nError', error)
//   },
//   complete: () => {
//     console.log('\nSuccess')
//   },
// })