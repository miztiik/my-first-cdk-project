# -*- coding: utf-8 -*-
"""
.. module: stream_record_consumer
    :Actions: Process kinesis records
    :copyright: (c) 2020 Mystique.,
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

import json
import base64
import logging
import time
import os
import boto3

__author__ = "Mystique"
__email__ = "miztiik@github"
__version__ = "0.0.1"
__status__ = "production"


class global_args:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "stream_record_consumer"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def set_logging(lv=global_args.LOG_LEVEL):
    """ Helper to enable logging """
    logging.basicConfig(level=lv)
    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(lv)
    return LOGGER


def write_data_to_s3(bucket_name, data):
    s3 = boto3.resource("s3")
    object = s3.Object(bucket_name, f"{int(time.time()*1000)}.json")
    resp = object.put(Body=data)
    LOGGER.info(json.dumps(resp))


def lambda_handler(event, context):
    # Initialize Logger
    global LOGGER
    LOGGER = set_logging(logging.INFO)
    resp = {"status": False, "records": ""}
    LOGGER.info(f"Event: {json.dumps(event)}")
    bucket_name = os.getenv("BUCKET_NAME")

    try:
        if event.get("Records"):
            for record in event["Records"]:
                # Kinesis data is base64 encoded so decode here
                payload = base64.b64decode(record["kinesis"]["data"])
                write_data_to_s3(bucket_name, payload)
                LOGGER.info(f"Decoded payload: {str(payload)}")
            LOGGER.info(
                f'{{"records_processed":{len(event.get("""Records"""))}}}')
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
