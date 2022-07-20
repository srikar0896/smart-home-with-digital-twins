# imports
from ast import operator
from time import time
from datetime import datetime, timedelta
from logger import logger
import random
from json_to_csv import write_json_to_csv
from dateutil import tz

# first we will generate the data for a single day.

# The time difference in which we collect the data.
# Of 86400 seconds in a day, how frequently we want to collect the data.

# units

hours = 60*60
minutes = 60

total_seconds_in_a_day = 24*hours
# 4 hours
interval = 30

# Sleeping hours
wakeup_time = 6*hours
sleep_time = 22*hours

# Light Settings
sunrise_time = 7*hours
sunset_time = 18*hours


# Week day can be derived from sqlite3 import Timestamp
# from the Timestamp. This can be used to infer if it is a weekend.

rules = [
    {
        "type": 'and',
        # Person is asleep and is not moving
        "validations": ['not_has_woke_up', 'not_is_moving', 'not_sun_rise'],
        'result': False
    },
    {
        "type": 'and',
        # Person wokeup early and moving
        "validations": ['not_has_woke_up', 'is_moving', 'not_sun_rise'],
        'result': True
    },
    {
        "type": 'and',
        # Evening
        "validations": ['has_woke_up', 'is_moving', 'not_sun_rise'],
        'result': True
    },
    {
        "type": 'and',
        # Person wokeup and is not moving --> holiday -> past the daily routine
        "validations": ['has_woke_up', 'not_is_moving', 'sun_rise'],
        'result': False
    },
    {
        "type": 'and',
        # Person woke up and is moving
        "validations": ['has_woke_up', 'is_moving', 'sun_rise'],
        'result': False
    },
    {
        "type": 'and',
        # Evening, but noone is home
        "validations": ['has_woke_up', 'not_is_moving', 'not_sun_rise'],
        'result': False
    },
]


def addSecs(tm, secs):
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + timedelta(seconds=secs)
    return fulldate.time()


def get_timestamp_from_seconds(seconds):
    est = tz.gettz('America/New_York')
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day,
                     tzinfo=tz.tzutc())
    # print(today)
    new_time_stamp = addSecs(start, seconds)
    # return new_timestamp.strftime('%c')
    return new_time_stamp.strftime('%c')


def get_movement_and_light(total_seconds_elapsed, is_moving, timer_seconds_elapsed):
    has_woke_up = total_seconds_elapsed >= wakeup_time
    sun_rise = total_seconds_elapsed >= sunrise_time

    not_has_woke_up = total_seconds_elapsed >= sleep_time or (not has_woke_up)
    not_sun_rise = total_seconds_elapsed >= sunset_time or (not sun_rise)

    not_is_moving = not is_moving

    properties = {
        "has_woke_up": has_woke_up,
        "sun_rise": sun_rise,
        "not_has_woke_up": not_has_woke_up,
        "not_sun_rise": not_sun_rise,
        "is_moving": is_moving,
        "not_is_moving": not_is_moving,
    }

    result = False
    for rule in rules:
        rule_result = True
        for validation in rule['validations']:
            rule_result = rule_result and properties[validation]
        # print('properties,', properties, rule, rule_result)
        if rule_result:
            result = result or rule['result']

    realization_time = random.randint(3, 10) * minutes
    print('realization', timer_seconds_elapsed, realization_time, result)
    status = result if timer_seconds_elapsed > realization_time else not result
    return {
        "movement": 'yes' if is_moving else 'no',
        "status": 'On' if status else 'Off'
    }

# This script generates data by following some simple rules
# waking up late and early, can be randomized between days. But for now, we are doing this for a day


def generate_data():
    total_seconds_elapsed = 0
    dataset = []
    movement_timer = 0
    timer_seconds_elapsed = 0
    is_moving = False

    while total_seconds_elapsed <= total_seconds_in_a_day:
        current_record = {}

        # timestamp field
        time_stamp = get_timestamp_from_seconds(total_seconds_elapsed)
        current_record['timestamp'] = time_stamp
        current_record['total_seconds_elapsed'] = total_seconds_elapsed

        if timer_seconds_elapsed >= movement_timer:
            # pick new random movement
            is_moving = random.choice([True, False])
            movement_timer = random.randint(5*minutes, 4*hours)
            # Reset the timer
            timer_seconds_elapsed = 0

        movement_and_light = get_movement_and_light(
            total_seconds_elapsed, is_moving, timer_seconds_elapsed)
        current_record['movement'] = movement_and_light['movement']
        current_record['status'] = movement_and_light['status']

        timer_seconds_elapsed += interval
        total_seconds_elapsed += interval
        dataset.append(current_record)
    return dataset


def init():
    logger.info('Starting Data Generation')
    generated_data = generate_data()
    logger.info('Finished Data generation.')
    logger.info('Total records generated - ' + str(len(generated_data)))

    dataset_file_name = 'data.csv'

    logger.info('Writing data generated to a csv file with name - ' +
                dataset_file_name)
    write_json_to_csv(dataset_file_name, generated_data)
    logger.info('Successfully saved the data in file - ' + dataset_file_name)


init()
