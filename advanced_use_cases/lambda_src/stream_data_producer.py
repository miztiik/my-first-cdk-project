# -*- coding: utf-8 -*-
"""
.. module: sample_kinesis_producer
    :Actions: Put Records in Kinesis Data Stream 
    :copyright: (c) 2020 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

import json
import logging
import os
import random
import string
import time
import uuid

import boto3

__author__ = "Mystique"
__email__ = "miztiik@github"
__version__ = "0.0.1"
__status__ = "production"


class global_args:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "sample_kinesis_producer"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    STREAM_NAME = os.getenv("STREAM_NAME", "data_pipe")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def set_logging(lv=global_args.LOG_LEVEL):
    """ Helper to enable logging """
    logging.basicConfig(level=lv)
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(lv)
    return LOGGER


def _gen_uuid():
    """ Generates a uuid string and return it """
    return str(uuid.uuid4())


def random_str_generator(size=40, chars=string.ascii_uppercase + string.digits):
    """ Generate Random String for given string length """
    return "".join(random.choice(chars) for _ in range(size))


def send_data(client, data, key, stream_name):
    # LOGGER.info(f"data:{json.dumps(data)}")
    # LOGGER.info(f"key:{key}")
    resp = client.put_records(
        Records=[
            {
                "Data": json.dumps(data),
                "PartitionKey": key},
        ],
        StreamName=stream_name

    )
    LOGGER.info(f"Response:{resp}")


client = boto3.client(
    "kinesis", region_name=global_args.AWS_REGION)


def lambda_handler(event, context):
    # Initialize Logger
    global LOGGER
    LOGGER = set_logging(logging.INFO)
    resp = {"status": False, "resp": ""}
    LOGGER.info(f"Event: {json.dumps(event)}")

    _random_user_name = ["Aarakocra", "Aasimar", "Beholder", "Bugbear", "Centaur", "Changeling", "Deep Gnome", "Deva", "Dragonborn", "Drow", "Dwarf", "Eladrin", "Elf", "Firbolg", "Genasi", "Githzerai", "Gnoll", "Gnome", "Goblin", "Goliath", "Hag", "Half-Elf",
                         "Half-Orc", "Halfling", "Hobgoblin", "Kalashtar", "Kenku", "Kobold", "Lizardfolk", "Loxodon", "Mind Flayer", "Minotaur", "Orc", "Shardmind", "Shifter", "Simic Hybrid", "Tabaxi", "Tiefling", "Tortle", "Triton", "Vedalken", "Warforged", "Wilden", "Yuan-Ti"]

    try:
        record_count = 0
        for i in range(random.randint(1, 3)):
            send_data(client, {"name": random.choice(_random_user_name),
                               "age": random.randint(1, 500),
                               "location": f"Middle Earth"
                               },
                      _gen_uuid(), global_args.STREAM_NAME)
            record_count += 1
        resp["resp"] = record_count
        resp["status"] = True

    except Exception as e:
        LOGGER.error(f"ERROR:{str(e)}")
        resp["error_message"] = str(e)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": resp
        })
    }


if __name__ == "__main__":
    lambda_handler({}, {})
