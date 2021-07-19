#!/bin/python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import shutil
import zipfile
try:
    from ebextensions_validator import validator
except ImportError:
    # for running pytest 
    from .ebextensions_validator import validator

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# logger.propagate = False

def application_valid(path_zip, path_allowlist):

    path_extracted = "/tmp/application"
    os.mkdir(path_extracted)

    try:
        # Unzip
        with zipfile.ZipFile(path_zip, "r") as zip_ref:
            zip_ref.extractall(path_extracted)

        VALID = validate(path_extracted, path_allowlist)

        try: 
            # Clean up
            shutil.rmtree(path_extracted)
        except FileNotFoundError:
            # Nothing to cleanup
            pass
        return VALID

    except Exception as e:
        try: 
            # Clean up
            shutil.rmtree(path_extracted)
        except FileNotFoundError:
            # Nothing to cleanup
            pass
        raise e


def validate(path_extracted, path_allowlist):

    # Check if .ebextensions is present
    VALID = True
    if ".ebextensions" not in os.listdir(path_extracted):
        logger.info("No .ebextensions present - pass")
    else:
        # .ebextensions present - validate against allowlist
        for config_file in [path_extracted + "/.ebextensions/" + filename for filename in os.listdir(path_extracted + "/.ebextensions") if filename.endswith(".config")]:
            logger.info("Validate %s ...", config_file.replace(path_extracted + "/", ""))
            if not validator.validate(config_file, path_allowlist):
                logger.info("%s not valid", config_file.replace(path_extracted + "/", ""))
                VALID = False
            else:
                logger.info("%s is valid.", config_file.replace(path_extracted + "/", ""))

    # Check if env.yaml is present
    if "env.yaml" not in os.listdir(path_extracted):
        logger.info("No env.yaml present - pass")
    else:
        logger.info("env.yaml present - fail")
        VALID = False

    try: 
        # Clean up
        shutil.rmtree(path_extracted)
    except FileNotFoundError:
        # Nothing to cleanup
        pass
    
    return VALID

