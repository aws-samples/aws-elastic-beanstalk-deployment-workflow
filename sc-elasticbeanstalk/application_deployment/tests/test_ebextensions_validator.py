#!/usr/bin/env python

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from ebextensions_validator.validation import application_valid # Lambda function code

def test_ebextensions_validator():
    path_allowlist = "test_files/allow.list"
    path_zip_valid = "test_files/application_valid.zip"
    path_zip_not_valid = "test_files/application_not_valid.zip"
    path_zip_no_ebextensions = "test_files/application_no_ebextensions.zip"
    path_zip_empty_valid = "test_files/application_empty_valid.zip"
    path_zip_empty_not_valid = "test_files/application_empty_not_valid.zip"
    assert application_valid(path_zip_valid, path_allowlist)
    assert not application_valid(path_zip_not_valid, path_allowlist)
    assert application_valid(path_zip_no_ebextensions, path_allowlist)
    assert application_valid(path_zip_empty_valid, path_allowlist)
    assert not application_valid(path_zip_empty_not_valid, path_allowlist)
