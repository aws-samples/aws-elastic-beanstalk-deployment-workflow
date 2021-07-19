#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from io import StringIO
import ebextensions_validator.main as main
from unittest.mock import patch

def test_main_not_valid():
    expected_output = "Configuration NOT in allowlist\n"
    with patch('sys.stdout', new=StringIO()) as fake_out:
        main.main(["test_files/config_files/command.config", "test_files/allowlist_files/command_multiple_regex_no_match.list", "-v"])
        assert fake_out.getvalue() == expected_output
    
def test_main_valid():
    expected_output = "Configuration is in allowlist\n"
    with patch('sys.stdout', new=StringIO()) as fake_out:
        main.main(["test_files/config_files/packages.config", "-v", "test_files/allowlist_files/packages_valid.list"])
        assert fake_out.getvalue() == expected_output

def test_main_non_args():
    try:
        main.main()
    except SystemExit as e:
        assert str(e) == "2"

