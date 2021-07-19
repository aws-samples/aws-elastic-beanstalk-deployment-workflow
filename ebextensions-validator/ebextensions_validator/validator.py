#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Validator module
"""

import logging
import re
from typing import List, Dict
from . import parser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def validate(config_file_path: str, allowlist_file_path: str) -> bool:
    """
    The function expects the path to a configuration file in yaml and the path to a allowlist file
    It returns True if the configuration is in the allowlist
    It return False if the configuration is not in the allowlist
    """

    # For each item in config_file check if there is a representation in the allowlist
    config_dict = parser.yaml_to_dict(config_file_path)
    allowlist_dict = parser.yaml_to_dict(allowlist_file_path)
    config_iterator = parser.nested_dict_iter(config_dict)
    allowed = True
    name_of_last_checked_object_name = None
    for key_stack, value in config_iterator:
        # Iterate over each item in config_file
        try:
            if key_stack[0] != parser.OPTION_SETTINGS and (
                isinstance(allowlist_dict[key_stack[0]], list)
                or (
                    key_stack[0] == parser.SERVICES
                    and isinstance(allowlist_dict[key_stack[0]][key_stack[1]], list)
                )
            ):
                # allowlist is not proper dictionary but list of dictionaries

                if key_stack[0] == parser.SERVICES and key_stack[1] == parser.SYSVINIT:
                    # dicitionaries for "services" configuration is on level 3,
                    # other configurations have dictionaries on level 2
                    top_level_object_name = key_stack[2]
                    checked_config_dict = config_dict[key_stack[0]][key_stack[1]][
                        key_stack[2]
                    ]
                    checked_allowlist_dict = allowlist_dict[key_stack[0]][key_stack[1]]
                else:
                    top_level_object_name = key_stack[1]
                    checked_config_dict = config_dict[key_stack[0]][key_stack[1]]
                    checked_allowlist_dict = allowlist_dict[key_stack[0]]

                if name_of_last_checked_object_name == top_level_object_name:
                    # No need to check for allowlisting again,
                    # since the whole dictionary containing the item is already checked.
                    continue

                # save already checked dictionary object
                name_of_last_checked_object_name = top_level_object_name

                if not dict_is_allowed(
                    dict({top_level_object_name: checked_config_dict}),
                    checked_allowlist_dict,
                ):
                    allowed = False
                    logger.info(
                        "Dictionary %s is not in allowlist",
                        str(dict({top_level_object_name: checked_config_dict}))
                    )

            elif not is_in_allowlist(key_stack.copy() + [value], allowlist_dict):
                allowed = False
                logger.info("%s is not in allowlist", str(key_stack + [value]))
        except KeyError:
            logger.info("Key %s not in allowlist", key_stack[0])
            return False
        except IndexError:
            logger.error("Invalid file")
            return False

    return allowed


def dict_is_allowed(config_dict: Dict, allowlist_dict_list: Dict) -> bool:
    """ checks if config_dict is allowed as defined ind allowlist_dict_list """
    logger.debug("Check dictionary allowlisting")
    for allowlist_dict in allowlist_dict_list:
        logger.debug("Allowlist_dict: %s", str(allowlist_dict))
        if dict_matches_allowlist_dict(config_dict, allowlist_dict):
            return True
    return False


def dict_matches_allowlist_dict(config_dict: Dict, allowlist_dict: Dict) -> bool:
    """ Check if config_dict matches the allowlist dictionary """
    config_iterator = parser.nested_dict_iter(config_dict)
    allowed = True
    for key_stack, value in config_iterator:
        if not is_in_allowlist(key_stack.copy() + [value], allowlist_dict):
            allowed = False
    return allowed


def is_in_allowlist(config_path: List[str], allowlist_dict: Dict) -> bool:
    """ Check if the config_path is present in allowlist """
    allowlist_iterator = parser.nested_dict_iter(allowlist_dict)
    logger.debug("configlist: %s", str(config_path))
    for key_stack, value in allowlist_iterator:
        allowlist_path = key_stack.copy() + [value]
        logger.debug("Allowlist: %s", str(allowlist_path))
        allowed = True
        for config_item, allowlist_item in zip(config_path, allowlist_path):
            # check if items match
            if not match(allowlist_item, config_item, config_path):
                logger.debug("%s does not match %s", str(config_item), str(allowlist_item))
                allowed = False
                break
        if allowed:
            return True
    return False


def match(regex, item, config_path: List[str]) -> bool:
    """ compare item from config_dict with regex from allowlist_dict """
    if isinstance(item, bool):
        item = str(item)
    if isinstance(regex, bool):
        regex = str(regex)

    if isinstance(regex, str) and isinstance(item, str):
        return re.match(regex, item) is not None

    if (
        config_path[0] == parser.USERS
        and config_path[2] == parser.GROUPS
        and isinstance(regex, list)
        and isinstance(item, list)
    ):
        # users - compare list of groups with list of regex
        return compare_lists(regex, item)

    if (
        config_path[0] == parser.SERVICES
        and config_path[3] in [parser.FILES, parser.SOURCES, parser.COMMANDS]
        and isinstance(regex, list)
        and isinstance(item, list)
    ):
        # services - compare list of files, sources or commands with list of regex
        return compare_lists(regex, item)

    if (
        config_path[0] == parser.COMMANDS
        and config_path[2] == parser.COMMAND
        and isinstance(regex, str)
        and isinstance(item, list)
    ):
        # Command - convert list into string
        return re.match(regex, " ".join(item)) is not None

    if (
        config_path[0] == parser.CONTAINER_COMMANDS and config_path[2] == parser.COMMAND
    ):
        # Container_command - compare list of commands with list of regex
        if isinstance(item, str):
            item = [item]
        if isinstance(regex, str):
            regex = [regex]
        return compare_lists(regex, item)

    return regex == item


def compare_lists(regex_list: List, item_list: List) -> bool:
    """ if each item matches at least one regex, then return True, else return False """
    for item in item_list:
        matched = False
        for regex in regex_list:
            if re.match(regex, item):
                matched = True
        if not matched:
            return False
    return True
