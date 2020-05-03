# -*- coding: utf-8 -*-
"""
.. module: rest_api_backend
    :Actions: Process Events and ingest to DynamoDB table
    :copyright: (c) 2020 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

import boto3
import json
import logging
import random
import os

__author__ = 'Mystique'
__email__ = 'miztiik@github'
__version__ = '0.0.1'
__status__ = 'production'


class global_args:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "rest_api_backend"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


_s3_client = boto3.client('s3')
_ddb = boto3.resource('dynamodb')


def _ddb_put_item(item):
    """ Insert Item into DynamoDb Table """
    if os.environ.get('DDB_TABLE_NAME'):
        _ddb_table = _ddb.Table(os.environ.get('DDB_TABLE_NAME'))
        try:
            return(_ddb_table.put_item(Item=item))
        except Exception as e:
            raise


def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv("LOG_LEVEL", "INFO").upper())

    LOGGER.info(f"received_event:{event}")
    resp = {
        "statusCode": 400,
        "body": json.dumps({"message": {}})
    }
    _random_user_name = ["Aarakocra", "Aasimar", "Beholder", "Bugbear", "Centaur", "Changeling", "Deep Gnome", "Deva", "Dragonborn", "Drow", "Dwarf", "Eladrin", "Elf", "Firbolg", "Genasi", "Githzerai", "Gnoll", "Gnome", "Goblin", "Goliath", "Hag", "Half-Elf",
                         "Half-Orc", "Halfling", "Hobgoblin", "Human", "Kalashtar", "Kenku", "Kobold", "Lizardfolk", "Loxodon", "Mind Flayer", "Minotaur", "Orc", "Shardmind", "Shifter", "Simic Hybrid", "Tabaxi", "Tiefling", "Tortle", "Triton", "Vedalken", "Warforged", "Wilden", "Yuan-Ti"]

    try:
        if event.get("pathParameters"):
            item = {}
            item["_id"] = event.get("pathParameters").get(
                "user_name", random.choice(_random_user_name))
            item["likes"] = event.get('pathParameters').get(
                'likes', random.randint(1, 100))
            _put_resp = _ddb_put_item(item)
            resp["statusCode"] = 200
            resp["body"] = json.dumps(
                {"message": f"Successfully updated '{item['_id']}' with '{item['likes']}' likes"})
    except Exception as e:
        LOGGER.error(f"{str(e)}")
        resp["body"] = json.dumps({
            "message": f"ERROR:{str(e)}"
        })

    return resp
