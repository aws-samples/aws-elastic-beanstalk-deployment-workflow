#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import boto3
from crhelper import CfnResource

logger = logging.getLogger(__name__)

helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL', sleep_on_delete=120)

try:
    ## Init code goes here
    s3 = boto3.resource('s3')
except Exception as e:
    helper.init_failure(e)

def initialize_files():
    s3.Object(os.environ["EbextensionsValidatorS3BucketName"], os.environ["GlobalAllowlistFolderName"] + '/empty.list').put(Body=open("empty.list", "rb"))
    s3.Object(os.environ["EbextensionsValidatorS3BucketName"], os.environ["GlobalAllowlistFolderName"] + '/allow_all.list').put(Body=open("allow_all.list", "rb"))
    s3.Object(os.environ["EbextensionsValidatorS3BucketName"], os.environ["GlobalAllowlistFolderName"] + '/allow_files_in_opt_elasticbeanstalk_tasks_logs.list').put(Body=open("allow_files_in_opt_elasticbeanstalk_tasks_logs.list", "rb"))

@helper.create
def create_policy(event, _):
    logger.info("Got Create")
    initialize_files()

@helper.update
def update_policy(event, _):
    logger.info("Got Update")
    initialize_files()

@helper.delete
def delete_policy(event, __):
    logger.info("Got Delete")
    '''Do nothing'''


def lambda_handler(event, context):
    print(event)
    try:
        helper(event, context)
    except Exception as e:
        logger.info('FAILED: {}'.format(e))
        helper.init_failure(e)
