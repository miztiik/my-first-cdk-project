# -*- coding: utf-8 -*-

import boto3
import json
import logging
import os

_s3_client = boto3.client('s3')
_ddb = boto3.resource('dynamodb')


def _ddb_put_item(item):
    """ Insert Item into DynamoDb Table """
    if os.environ.get('DDB_TABLE_NAME'):
        _ddb_table = _ddb.Table(os.environ.get('DDB_TABLE_NAME'))
        try:
            _ddb_table.put_item(Item=item)
        except Exception as e:
            raise


def get_bkts_inventory():
    """ Generate List of S3 Buckets """
    try:
        resp = _s3_client.list_buckets()
        bkt_inventory = {"buckets": []}
        for bkt in resp['Buckets']:
            bkt_inventory["buckets"].append(bkt["Name"])
            _ddb_put_item({"_id": bkt["Name"]})
        return bkt_inventory
    except Exception as e:
        raise


def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())
    LOGGER.info(f"received_event:{event}")

    resp = {
        "statusCode": 400,
        "body": json.dumps({"message": event})
    }

    try:
        bkt_inventory = get_bkts_inventory()
        resp["body"] = json.dumps({
            "message": bkt_inventory
        })
        resp['statusCode'] = 200
    except Exception as e:
        resp["body"] = json.dumps({
            "message": f"ERROR:{str(e)}"
        })

    return resp
