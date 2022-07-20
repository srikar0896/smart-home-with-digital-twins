const sleep = require('k6').sleep;
const http = require('k6/http');

const options = {
    ext: {
        loadimpact: {
            distribution: {'amazon:us:ashburn': {loadZone: 'amazon:us:ashburn', percent: 100}},
            apm: [],
        },
    },
    thresholds: {},
    scenarios: {
        Scenario_1: {
            executor: 'ramping-vus',
            gracefulStop: '30s',
            stages: [
                {target: 20, duration: '1m'},
                {target: 20, duration: '3m30s'},
                {target: 0, duration: '1m'},
            ],
            gracefulRampDown: '30s',
            exec: 'scenario_1',
        },
    },
}

function scenario_1() {
    let response

    // Get Recommendations
    response = http.post(
        'http://localhost:5000/get-recommendations',
        '{\n    "home_params": {\n        "movement_status": "yes",\n        "timestamp": 68760,\n        "light_status": "On",\n        "room_label": "Room 1"\n    }\n}',
        {
            headers: {
                'content-type': 'application/json',
            },
        }
    )

    // Automatically added sleep
    sleep(1)
}

module.exports.scenario_1 = scenario_1;
module.exports.options = options;