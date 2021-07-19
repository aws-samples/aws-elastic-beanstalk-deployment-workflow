#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import ebextensions_validator.parser as parser
import ebextensions_validator.validator
from cfn_tools import load_yaml


def test_option_settings_add_namespace():
    option_settings_without_namespace = load_yaml(open("test_files/config_files/option_settings_standard_without_namespace.config").read())
    option_settings_with_namespace = load_yaml(open("test_files/config_files/option_settings_standard_with_namespace.config").read())
    dict_without = parser.option_settings_transform(option_settings_without_namespace["option_settings"])
    dict_with = parser.option_settings_transform(option_settings_with_namespace["option_settings"])
    for namespace in dict_without:
        assert namespace in dict_with
        for option_name in dict_without[namespace]:
            assert option_name in dict_with[namespace]
            assert dict_without[namespace][option_name] == dict_with[namespace][option_name]
    for namespace in dict_with:
        assert namespace in dict_without
        for option_name in dict_with[namespace]:
            assert option_name in dict_without[namespace]
            assert dict_without[namespace][option_name] == dict_with[namespace][option_name]

def test_option_settings_transform():
    option_settings_standard = load_yaml(open("test_files/config_files/option_settings_standard.config").read())
    option_settings_shorthand = load_yaml(open("test_files/config_files/option_settings_shorthand.config").read())
    dict_standard = parser.option_settings_transform(option_settings_standard["option_settings"])
    dict_shorthand = option_settings_shorthand["option_settings"]
    for namespace in dict_shorthand:
        assert namespace in dict_standard
        for option_name in dict_shorthand[namespace]:
            assert option_name in dict_standard[namespace]
            assert dict_shorthand[namespace][option_name] == dict_standard[namespace][option_name]
    for namespace in dict_standard:
        assert namespace in dict_shorthand
        for option_name in dict_standard[namespace]:
            assert option_name in dict_shorthand[namespace]
            assert dict_shorthand[namespace][option_name] == dict_standard[namespace][option_name]

def test_option_settings_yaml_to_dict():
    option_settings_standard = parser.yaml_to_dict("test_files/config_files/option_settings_standard_long.config")
    option_settings_shorthand = parser.yaml_to_dict("test_files/config_files/option_settings_shorthand_long.config")
    parser.log_it(option_settings_standard)
    parser.log_it(option_settings_shorthand)
    for namespace in option_settings_shorthand:
        assert namespace in option_settings_standard
        for option_name in option_settings_shorthand[namespace]:
            assert option_name in option_settings_standard[namespace]
            assert option_settings_shorthand[namespace][option_name] == option_settings_standard[namespace][option_name]
    for namespace in option_settings_standard:
        assert namespace in option_settings_shorthand
        for option_name in option_settings_standard[namespace]:
            assert option_name in option_settings_shorthand[namespace]
            assert option_settings_shorthand[namespace][option_name] == option_settings_standard[namespace][option_name]
