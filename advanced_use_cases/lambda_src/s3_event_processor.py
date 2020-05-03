# -*- coding: utf-8 -*-
"""
.. module: s3_event_processor.py
    :Actions: Process S3 Events and ingest to DynamoDB table
    :copyright: (c) 2020 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

import boto3
import json
import logging
import os

__author__ = 'Mystique'
__email__ = 'miztiik@github'
__version__ = '0.0.1'
__status__ = 'production'


class global_args:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "s3_event_processor"
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
    try:
        if "Records" in event:
            item = {}
            item["_id"] = event["Records"][0]["s3"]["object"]["key"]
            item["_size"] = event["Records"][0]["s3"]["object"]["size"]
            item["_bucket"] = event["Records"][0]["s3"]["bucket"]["name"]
            item["_bucket_owner"] = event["Records"][0]["s3"]["bucket"]["ownerIdentity"]["principalId"]
            _put_resp = _ddb_put_item(item)
            resp["statusCode"] = 200
            resp["body"] = json.dumps({"message": _put_resp})
    except Exception as e:
        LOGGER.error(f"{str(e)}")
        resp["body"] = json.dumps({
            "message": f"ERROR:{str(e)}"
        })

    return resp
