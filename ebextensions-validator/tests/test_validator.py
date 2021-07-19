#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import ebextensions_validator.parser as parser
import ebextensions_validator.validator as validator
from cfn_tools import load_yaml
import glob


def test_unit_dict_matches_allowlist_dict():
    input_dict_1 = dict({'command2': [{'command': 'a'}, {'cwd': 'b'}]})
    input_dict_2 = dict({'command2': [{'command': 'a'}, {'cwd': 'c'}]})
    input_dict_3 = dict({'command2': [{'command': 'c'}, {'cwd': 'b'}]})
    input_dict_4 = dict({'command2': [{'command': 'c'}, {'cwd': 'c'}]})
    allowlist_dict = dict({'.*': [{'command': 'a'}, {'cwd': 'b'}]})
    assert validator.dict_matches_allowlist_dict(input_dict_1, allowlist_dict)
    assert not validator.dict_matches_allowlist_dict(input_dict_2, allowlist_dict)
    assert not validator.dict_matches_allowlist_dict(input_dict_3, allowlist_dict)
    assert not validator.dict_matches_allowlist_dict(input_dict_4, allowlist_dict)

def test_unit_dict_is_in_allowlist():
    input_path_a = ["command1", "command", "a"]
    input_path_d = ["command1", "cwd", "d"]
    allowlist_dict = dict({'.*': {'command': 'a', 'cwd': 'b'}})
    assert validator.is_in_allowlist(input_path_a, allowlist_dict)
    assert not validator.is_in_allowlist(input_path_d, allowlist_dict)

def test_unit_dict_is_allowed_valid():
    # One item does not match
    input_dict_1 = dict({'command1': [{'command': 'a'}, {'cwd': 'b'}]})
    input_dict_2 = dict({'command2': [{'command': 'c'}, {'cwd': 'd'}]})
    allowlist_dict_list = [dict({'.*': [{'command': 'a'}, {'cwd': 'b'}]}), dict({'.*': [{'command': 'c'}, {'cwd': 'd'}]})]
    assert validator.dict_is_allowed(input_dict_1, allowlist_dict_list)
    assert validator.dict_is_allowed(input_dict_2, allowlist_dict_list)

def test_unit_dict_is_allowed_not_valid():
    # One item does not match
    input_dict_1 = dict({'command1': [{'command': 'a'}, {'cwd': 'b'}]})
    input_dict_2 = dict({'command2': [{'command': 'c'}, {'cwd': 'd'}]})
    allowlist_dict_list_swapped = [dict({'.*': {'command': 'a', 'cwd': 'd'}}), dict({'.*': {'command': 'c', 'cwd': 'b'}})]
    assert not validator.dict_is_allowed(input_dict_1, allowlist_dict_list_swapped)
    assert not validator.dict_is_allowed(input_dict_2, allowlist_dict_list_swapped)

def test_unit_compare_list():
    # One item does not match
    regex_list = ["file1"]
    item_list = ["file1", "file2"]
    assert not validator.compare_lists(regex_list, item_list)
    # Each item matches one regex
    regex_list = ["file.*", "NO_MATCH"]
    item_list = ["file1", "file2"]
    assert validator.compare_lists(regex_list, item_list)
    # Unsorted list
    regex_list = ["file2", "file1"]
    item_list = ["file1", "file2"]
    assert validator.compare_lists(regex_list, item_list)

def test_allowlist_all_allowed_valid():
    for path in glob.glob("test_files/config_files/*.config"):
        assert validator.validate(path, "test_files/allowlist_files/allowlist_all.list")

def test_allowlist_empty_not_valid():
    for path in glob.glob("test_files/config_files/*.config"):
        assert not validator.validate(path, "test_files/allowlist_files/empty.list")

def test_allowlist_packages_valid():
    assert validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_valid.list")

def test_allowlist_packages_multiple_regex_valid():
    assert validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_multiple_regex.list")

def test_allowlist_packages_multiple_regex_not_valid():
    assert not validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_multiple_regex_no_match.list")

def test_allowlist_packages_not_sorted_valid():
    assert validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_valid_not_sorted.list")

def test_allowlist_packages_not_valid_value():
    assert not validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_not_valid_value.list")

def test_allowlist_packages_not_valid_key():
    assert not validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_not_valid_key.list")

def test_allowlist_packages_regex_valid():
    assert validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_regex_valid.list")

def test_allowlist_packages_allow_all_valid():
    assert validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_allow_all_valid.list")

def test_allowlist_packages_only_yum_valid():
    assert validator.validate("test_files/config_files/packages_only_yum.config", "test_files/allowlist_files/packages_only_yum.list")

def test_allowlist_packages_only_yum_not_valid():
    assert not validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/packages_only_yum.list")

def test_allowlist_option_settings_standard_long_valid():
    assert validator.validate("test_files/config_files/option_settings_standard_long.config", "test_files/allowlist_files/option_settings_standard_long_regex.list")

def test_allowlist_option_settings_standard_shorthand_long_valid():
    assert validator.validate("test_files/config_files/option_settings_shorthand_long.config", "test_files/allowlist_files/option_settings_standard_long_regex.list")

def test_allowlist_option_settings_standard_short_non_valid():
    assert not validator.validate("test_files/config_files/option_settings_standard_long.config", "test_files/allowlist_files/option_settings_standard_short_regex.list")

def test_allowlist_option_settings_standard_short_valid():
    assert validator.validate("test_files/config_files/option_settings_standard.config", "test_files/allowlist_files/option_settings_standard_short_regex.list")

def test_allowlist_option_settings_shorthand_shorthand_regex_valid():
    assert validator.validate("test_files/config_files/imdsv1.config", "test_files/allowlist_files/imdsv1_valid.list")

def test_allowlist_option_settings_boolean_valid():
    assert validator.validate("test_files/config_files/imdsv1.config", "test_files/allowlist_files/imdsv1.list")

def test_allowlist_groups_valid():
    assert validator.validate("test_files/config_files/groups.config", "test_files/allowlist_files/groups.list")

def test_allowlist_groups_non_valid():
    assert not validator.validate("test_files/config_files/groups.config", "test_files/allowlist_files/groups_only_groupOne.list")

def test_allowlist_groups_groupOne_valid():
    assert validator.validate("test_files/config_files/groups_only_groupOne.config", "test_files/allowlist_files/groups.list")

def test_allowlist_groups_multiple_regex_multiple_groups_valid():
    assert validator.validate("test_files/config_files/groups.config", "test_files/allowlist_files/groups_multiple_regex.list")

def test_allowlist_groups_multiple_regex_multiple_groups_not_valid():
    assert not validator.validate("test_files/config_files/groups_wrong_attribute.config", "test_files/allowlist_files/groups_multiple_regex.list")

def test_allowlist_groups_multiple_regex_groupOne_valid():
    assert validator.validate("test_files/config_files/groups_only_groupOne.config", "test_files/allowlist_files/groups_multiple_regex.list")

def test_allowlist_users_valid():
    assert validator.validate("test_files/config_files/users.config", "test_files/allowlist_files/users.list")

def test_allowlist_users_multiple_regex_valid():
    assert validator.validate("test_files/config_files/users.config", "test_files/allowlist_files/users_multiple_regex.list")

def test_allowlist_users_multiple_regex_not_valid():
    assert not validator.validate("test_files/config_files/users.config", "test_files/allowlist_files/users_multiple_regex_wrong_attributes.list")

def test_allowlist_users_only_groups_non_valid():
    assert not validator.validate("test_files/config_files/users.config", "test_files/allowlist_files/users_only_groups.list")

def test_allowlist_users_not_sorted_valid():
    assert validator.validate("test_files/config_files/users.config", "test_files/allowlist_files/users_not_sorted.list")

def test_allowlist_sources_valid():
    assert validator.validate("test_files/config_files/sources.config", "test_files/allowlist_files/sources.list")

def test_allowlist_sources_multiple_regex_valid():
    assert validator.validate("test_files/config_files/sources.config", "test_files/allowlist_files/sources_multiple_regex.list")

def test_allowlist_sources_multiple_regex_not_valid():
    assert not validator.validate("test_files/config_files/sources.config", "test_files/allowlist_files/sources_multiple_regex_wrong_url.list")

def test_allowlist_files_valid():
    assert validator.validate("test_files/config_files/files.config", "test_files/allowlist_files/files.list")

def test_allowlist_files_only_content_valid():
    assert validator.validate("test_files/config_files/files_only_content.config", "test_files/allowlist_files/files_only_content.list")

def test_allowlist_files_multiple_regex_valid():
    assert validator.validate("test_files/config_files/files.config", "test_files/allowlist_files/files_multiple_regex.list")

def test_allowlist_files_multiple_regex_not_valid():
    assert not validator.validate("test_files/config_files/files.config", "test_files/allowlist_files/files_multiple_regex_one_missing.list")

def test_allowlist_command_valid():
    assert validator.validate("test_files/config_files/command.config", "test_files/allowlist_files/command.list")

def test_allowlist_command_list_valid():
    assert validator.validate("test_files/config_files/command_only_list.config", "test_files/allowlist_files/command_only_regex.list")

def test_allowlist_command_block_valid():
    assert validator.validate("test_files/config_files/command_only_block.config", "test_files/allowlist_files/command_only_regex.list")

def test_allowlist_command_multiple_commands_valid():
    assert validator.validate("test_files/config_files/command_multiple_commands.config", "test_files/allowlist_files/command_multiple_regex_match.list")

def test_allowlist_command_multiple_commands_not_valid():
    # cwd attribute swapped
    assert not validator.validate("test_files/config_files/command_multiple_commands.config", "test_files/allowlist_files/command_multiple_regex_no_match.list")

def test_allowlist_command_single():
    assert validator.validate("test_files/config_files/command_single.config", "test_files/allowlist_files/command_single_both_match.list")
    assert not validator.validate("test_files/config_files/command_single.config", "test_files/allowlist_files/command_single_first_match.list")
    assert not validator.validate("test_files/config_files/command_single.config", "test_files/allowlist_files/command_single_last_match.list")
    assert not validator.validate("test_files/config_files/command_single.config", "test_files/allowlist_files/command_single_none_match.list")

def test_allowlist_services_valid():
    assert validator.validate("test_files/config_files/services.config", "test_files/allowlist_files/services.list")

def test_allowlist_services_match_multiple_files_to_one_regex_valid():
    assert validator.validate("test_files/config_files/services_only_multiple_files.config", "test_files/allowlist_files/services_only_file_regex.list")

def test_allowlist_services_match_multiple_files_to_one_regex_not_valid():
    assert not validator.validate("test_files/config_files/services_only_multiple_files.config", "test_files/allowlist_files/services_only_file_regex_no_match.list")

def test_allowlist_services_match_multiple_files_one_match_not_valid():
    assert not validator.validate("test_files/config_files/services_only_multiple_files.config", "test_files/allowlist_files/services_multiple_files_one_match.list")

def test_allowlist_services_match_multiple_sources_to_one_regex_valid():
    assert validator.validate("test_files/config_files/services_only_multiple_sources.config", "test_files/allowlist_files/services_only_sources_regex.list")

def test_allowlist_services_match_multiple_commands_to_one_regex_valid():
    assert validator.validate("test_files/config_files/services_only_multiple_commands.config", "test_files/allowlist_files/services_only_commands_regex.list")

def test_allowlist_services_multiple_regex_valid():
    assert validator.validate("test_files/config_files/services.config", "test_files/allowlist_files/services_multiple_regex.list")

def test_allowlist_services_multiple_regex_not_valid():
    assert not validator.validate("test_files/config_files/services.config", "test_files/allowlist_files/services_multiple_regex_no_match.list")

def test_allowlist_container_commands_valid():
    assert validator.validate("test_files/config_files/container_commands.config", "test_files/allowlist_files/container_commands.list")

def test_allowlist_container_commands_only_command_array_to_array_valid():
    assert validator.validate("test_files/config_files/container_commands_only_command_array.config", "test_files/allowlist_files/container_commands_only_command_array.list")

def test_allowlist_container_commands_normal_command_and_array_allowlist_valid():
    assert not validator.validate("test_files/config_files/container_commands.config", "test_files/allowlist_files/container_commands_only_command_array.list") 

def test_allowlist_container_commands_normal_command_and_array_allowlist_not_valid():
    assert validator.validate("test_files/config_files/container_commands_only_command_array.config", "test_files/allowlist_files/container_commands_only_command_array.list") 

def test_allowlist_container_commands_only_command_array_to_regex_valid():
    assert validator.validate("test_files/config_files/container_commands_only_command_array.config", "test_files/allowlist_files/container_commands_only_command_regex.list")

def test_allowlist_container_commands_only_command_array_to_regex_not_valid():
    assert not validator.validate("test_files/config_files/container_commands_only_command_array.config", "test_files/allowlist_files/container_commands_only_command_regex_no_match.list")

def test_allowlist_container_commands_multiple_regex_valid():
    assert validator.validate("test_files/config_files/container_commands.config", "test_files/allowlist_files/container_commands_multiple_regex.list")

def test_allowlist_container_commands_multiple_regex_not_valid():
    assert not validator.validate("test_files/config_files/container_commands.config", "test_files/allowlist_files/container_commands_multiple_regex_one_missing.list")

def test_allowlist_resources_valid():
    assert validator.validate("test_files/config_files/resources.config", "test_files/allowlist_files/resources.list")

def test_allowlist_resources_missing_SecurityGroup_not_valid():
    assert not validator.validate("test_files/config_files/resources.config", "test_files/allowlist_files/resources_missing_SecurityGroup.list")

def test_allowlist_resources_with_properties_valid():
    assert validator.validate("test_files/config_files/resources_with_properties.config", "test_files/allowlist_files/resources.list")

def test_allowlist_resources_missing_properties_not_valid():
    assert not validator.validate("test_files/config_files/resources_with_properties.config", "test_files/allowlist_files/resources_missing_properties.list")

def test_allowlist_configuration_not_present_in_list():
    assert not validator.validate("test_files/config_files/packages.config", "test_files/allowlist_files/resources.list")

def test_invalid_file():
    assert not validator.validate("test_files/allowlist_files/command_multiple_regex_no_match.list", "test_files/config_files/command.config")
