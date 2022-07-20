
from logger import logger
# Registers a twin and creates an entry in the "twins" bucket
# Returns id as response.


def register_twin(name, id, topic):
    logger.info('Registering Twin')
    # datastore.write()
    return ''


def update_twin(id, value):
    return ''


def get_twin(id):
    return {}


def get_twins():
    return []
#                                                                             a. twins configuration Table
#                                                                             b. status Table
#                                                                             c. historic data Table
#                                                                         writes data to datastore
#  Physical Asset(producer)-> _                                 _ ------------> FluxDB
#                              \                               /                  |
#                               \                             /                   |
#                                 -> Digital Twin(Consumer) -                     |
#                               /                     |                           |
#                              /                      |                           |
#           Node Web-Server ->                        |                           v
#     (on request, acts like producer)                |                AnalyticsService(FlaskServer)
#                   ^                                 |                           |
#                   |                                 |                           |
#   makes modification request to physical asset      |                           |
#     through a.control toggle b.ML feedback          |                           |
#                   |                                 |                           |
#                   |                                 |                           |
#             Frontend client <----------------------------------------------------
#                   ^
#                   |
#                   |
#                   |
#                   v
#           Machine Learning Service
#
#
#
