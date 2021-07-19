#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
from . import validator as validator
import logging
import sys


def main(args=None):
    if not args:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Validate a config file from the .ebextensions directory against a allowlist of dictionaries"
    )
    parser.add_argument("config_file", help="Config file from .ebextensions directory")
    parser.add_argument(
        "allowlist_file",
        help="File which defines a allowlist of dictionaries. Regex can be used",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print information about not allowlisted configuration",
        action="store_true",
    )
    args = parser.parse_args(args)

    if args.verbose:
        logging.basicConfig(format="* %(message)s", level=logging.INFO)

    result = validator.validate(args.config_file, args.allowlist_file)
    if result == True:
        print("Configuration is in allowlist")
    elif result == False:
        print("Configuration NOT in allowlist")
