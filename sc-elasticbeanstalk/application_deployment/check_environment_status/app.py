#!/bin/python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import os
import boto3  # pylint: disable=import-error

logger = logging.getLogger('Main')
logger.setLevel(logging.DEBUG)
logger.propagate = False

eb = None

def lambda_handler(event, context):

    global eb
    if not eb:
        eb = boto3.client('elasticbeanstalk')

    # try:
    print(json.dumps(event))

    response = eb.describe_environments(
        # ApplicationName=event["ApplicationName"],
        ApplicationName=os.environ["ApplicationName"],
        # EnvironmentId=event["EnvironmentId"],
        # EnvironmentNames=[event["EnvironmentName"]],
        EnvironmentNames=[os.environ["EnvironmentName"]],
        )

    # except Exception as e:

    #     # Handle exception
    #     logger.exception("## EXCEPTION")
    #     logger.exception(e)
    #     traceback.print_exc()
    #     print("Unexpected error: %s" % e)

    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({
    #             "message": print(e),
    #         }),
    #     }

    return {
        'statusCode': 200,
        'body': response["Environments"][0]["Status"]
    }
