#!/bin/python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import os
import re
import boto3  # pylint: disable=import-error

logger = logging.getLogger('Main')
logger.setLevel(logging.DEBUG)
logger.propagate = False

eb = None

def lambda_handler(event, context):

    global eb
    if not eb:
        eb = boto3.client('elasticbeanstalk')

    logger.info(json.dumps(event))

    response = eb.describe_applications(
        # ApplicationNames=[event["ApplicationName"]]
        ApplicationNames=[os.environ["ApplicationName"]]
    )
    try:
        logger.info(response["Applications"][0]["Versions"])
    
        # Find last version number
        version_pattern = re.compile(r'V[0-9]*$')
        highest_version_number = -1
        for version in response["Applications"][0]["Versions"]:
            if version_pattern.match(version):
                version_number = int(version_pattern.findall(version)[0][1::])
                highest_version_number = max(highest_version_number, version_number)
        new_version_label = "V" + str(highest_version_number + 1)
    except KeyError:
        # No ApplicationVersion present
        new_version_label = "V0"

    response = eb.create_application_version(
        # ApplicationName=event["ApplicationName"],
        ApplicationName=os.environ["ApplicationName"],
        VersionLabel=new_version_label,
        # Description=event["Description"],
        # SourceBuildInformation={
        #     'SourceType': 'Zip',
        #     'SourceRepository': 'S3',
        #     'SourceLocation': event["SourceLocation"]
        # },
        SourceBundle={
            'S3Bucket': event["S3Bucket"],
            'S3Key': event["S3Key"]
        },
        # BuildConfiguration={
        #     'ArtifactName': 'string',
        #     'CodeBuildServiceRole': 'string',
        #     'ComputeType': 'BUILD_GENERAL1_SMALL'|'BUILD_GENERAL1_MEDIUM'|'BUILD_GENERAL1_LARGE',
        #     'Image': 'string',
        #     'TimeoutInMinutes': 123
        # },
        AutoCreateApplication=True,
        Process=True
        # Tags=[
        #     {
        #         'Key': 'string',
        #         'Value': 'string'
        #     },
        # ]
    )
    logger.info(response)

    # Delete old Application versions - Keep the neweset application versions. The amount of application versions kept is taken from the environment variable RemainingApplicationVersions
    describe_response = eb.describe_application_versions(
        ApplicationName=os.environ["ApplicationName"]
    )
    app_versions_list = describe_response["ApplicationVersions"]
    for app_version in app_versions_list[int(os.environ["RemainingApplicationVersions"])::]:
        if app_version["VersionLabel"] != new_version_label:
            delete_response = eb.delete_application_version(
                ApplicationName=os.environ["ApplicationName"],
                VersionLabel=app_version["VersionLabel"]
            )
            logger.info(delete_response)

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
        'VersionLabel': new_version_label,
        'body': json.dumps('Lambda done!')
    }
