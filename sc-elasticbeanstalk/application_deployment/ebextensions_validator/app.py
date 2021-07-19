#!/bin/python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import os
import boto3  # pylint: disable=import-error
import botocore
import validation

logger = logging.getLogger()
logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)
# logger.propagate = False

s3 = None
sc = None

def lambda_handler(event, context):

    global s3
    if not s3:
        s3 = boto3.client('s3')

    global sc
    if not sc:
        sc = boto3.client('servicecatalog')

    print(json.dumps(event))

    path_zip = "/tmp/application.zip"
    path_allowlist = "/tmp/allow.list"

    # Download application zip from S3
    with open(path_zip, "wb") as data:
        s3.download_fileobj(event["S3Bucket"], event["S3Key"], data)

    # Find allowlist bucket name
    ebextensions_allowlist_bucket = os.environ["GlobalAllowlistBucket"]
    global_allowlist_folder_name = os.environ["GlobalAllowlistFolderName"]

    # Download allowlist from S3
    with open(path_allowlist, "wb") as data:
        try:
            s3.download_fileobj(ebextensions_allowlist_bucket, os.environ["ProvisionedProductId"] + "/allow.list", data)
        except botocore.exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "404":
                logger.info("No exception allowlist found: s3://%s/%s/allow.list.", ebextensions_allowlist_bucket, os.environ["ProvisionedProductId"])
                logger.info("Continue with global allowlist.")
                try:
                    s3.download_fileobj(ebextensions_allowlist_bucket, global_allowlist_folder_name + "/allow.list", data)
                except botocore.exceptions.ClientError as e_global:
                    if e_global.response["Error"]["Code"] == "404":
                        logger.error("No global allowlist found: s3://%s/%s/allow.list.", ebextensions_allowlist_bucket, global_allowlist_folder_name)
                        logger.info("Raise error.")
                        raise e_global
                    raise e_global
            else:
                raise error

    if validation.application_valid(path_zip, path_allowlist):
        result = "Valid"
        logger.info("Ebextensions validator passed.")
    else:
        result = "NotValid"
        logger.info("Ebextensions validator not passed.")

    return {
        'statusCode': 200,
        'body': result
    }
