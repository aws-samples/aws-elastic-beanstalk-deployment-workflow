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
        EnvironmentNames=[os.environ["EnvironmentName"]],
        # EnvironmentNames=[event["EnvironmentName"]],
        )

    if "VersionLabel" in event:
        version_label = event["VersionLabel"]
    else:
        version_label = response["Environments"][0]["VersionLabel"]

    eb.update_environment(
        # ApplicationName=event["ApplicationName"],
        ApplicationName=os.environ["ApplicationName"],
        # EnvironmentId=event["EnvironmentId"],
        # EnvironmentName=event["EnvironmentName"],
        EnvironmentName=os.environ["EnvironmentName"],
        # GroupName=event["GroupName"],
        # Description=event["Description"],
        # Tier={
        #     'Name': 'string',
        #     'Type': 'string',
        #     'Version': 'string'
        # },
        VersionLabel=version_label,
        # TemplateName=event["TemplateName"],
        # SolutionStackName=event["SolutionStackName"],
        # PlatformArn=event["PlatformArn"],
        OptionSettings=[
            {
                'Namespace': 'aws:elasticbeanstalk:command',
                'OptionName': 'DeploymentPolicy',
                'Value': event["DeploymentPolicy"]
            },
        ],
        # OptionsToRemove=[
        #     {
        #         'ResourceName': 'string',
        #         'Namespace': 'string',
        #         'OptionName': 'string'
        #     },
        # ]
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
        'body': json.dumps('Lambda done!')
    }
