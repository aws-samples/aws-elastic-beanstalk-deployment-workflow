#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Parser module
"""

import logging
from collections import abc
from typing import Generator, List, Tuple
from cfn_tools import load_yaml  # type: ignore

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

AWS_ELASTICBEANSTALK_APPLICATION_ENVIRONMENT = (
    "aws:elasticbeanstalk:application:environment"
)
COMMAND = "command"
COMMANDS = "commands"
CONTAINER_COMMANDS = "container_commands"
FILES = "files"
GROUPS = "groups"
NAMESPACE = "namespace"
OPTION_NAME = "option_name"
OPTION_SETTINGS = "option_settings"
SERVICES = "services"
SOURCES = "sources"
SYSVINIT = "sysvinit"
USERS = "users"
VALUE = "value"


def nested_dict_iter(nested: abc.Mapping, key_stack: List = None) -> Generator[Tuple[List, str], None, None]:
    """ Iterator for dictionary yielding path and item """
    if not key_stack:
        key_stack = []
    for key, value in nested.items():
        key_stack.append(key)
        if value != dict() and isinstance(value, abc.Mapping):
            yield from nested_dict_iter(value, key_stack)
        else:
            yield key_stack, value
            key_stack.pop()
    try:
        key_stack.pop()
    except IndexError:
        pass


def option_settings_transform(option_settings: list) -> dict:
    """ Transforms standard syntax into shorthand syntax """
    logger.debug(option_settings)
    option_settings_candidate = dict()
    for item in option_settings:
        item = dict(item.items())
        if NAMESPACE in item:
            option_settings_candidate.update(
                {item[NAMESPACE]: {item[OPTION_NAME]: item[VALUE]}}
            )
        else:
            option_settings_candidate.update(
                {
                    AWS_ELASTICBEANSTALK_APPLICATION_ENVIRONMENT: {
                        item[OPTION_NAME]: item[VALUE]
                    }
                }
            )
    logger.debug(option_settings_candidate)
    return option_settings_candidate


def yaml_to_dict(file_path: str) -> dict:
    """ load yaml file and transform into dictionary """
    plain_dict = load_yaml(open(file_path).read())
    if plain_dict is None:
        logger.debug("Empty file")
        return dict({})
    if OPTION_SETTINGS in plain_dict.keys():
        option_settings = plain_dict[OPTION_SETTINGS]
        if isinstance(option_settings, list):
            logger.info("Standard Syntax - transform into shorthand")
            option_settings = option_settings_transform(option_settings)
        logger.debug(option_settings)
        plain_dict.update({OPTION_SETTINGS: option_settings})
    logger.debug(plain_dict)
    return dict(plain_dict)


def log_it(item):
    """ logger """
    logger.info(item)
