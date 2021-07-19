#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
'''
Create dummy ec2 key pair. Do not save the private key!
This key pair will be attached to the beanstalk environment during creation, such that it cannot be updated afterwards.
'''

import logging
import os
import boto3
from crhelper import CfnResource

logger = logging.getLogger(__name__)

helper = CfnResource(json_logging=False, log_level='DEBUG', boto_level='CRITICAL', sleep_on_delete=120)

try:
    ## Init code goes here
    ec2 = boto3.client("ec2")
except Exception as e:
    helper.init_failure(e)

@helper.create
def create_policy(event, _):
    logger.info("Got Create")
    ec2.create_key_pair(KeyName=os.environ["KeyName"])


@helper.update
def update_policy(event, _):
    logger.info("Got Update")
    '''Do nothing'''

@helper.delete
def delete_policy(event, __):
    logger.info("Got Delete")
    ec2.delete_key_pair(KeyName=os.environ["KeyName"])


def lambda_handler(event, context):
    print(event)
    try:
        helper(event, context)
    except Exception as e:
        logger.info('FAILED: {}'.format(e))
        helper.init_failure(e)
