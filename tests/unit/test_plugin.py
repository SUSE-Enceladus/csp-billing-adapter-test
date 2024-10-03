# Copyright 2023 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Unit tests for the csp_billing_adapter_test
#

import uuid

from unittest import mock
from datetime import datetime

from pytest import raises

from csp_billing_adapter_test.plugin import (
    get_usage_data,
    get_account_info,
    get_csp_name,
    meter_billing
)


def test_memory_get_cache(cba_config):
    possible_node_counts = [9, 10, 11, 25, 30, 100]

    usage = get_usage_data(cba_config)

    assert 'managed_node_count' in usage
    assert usage['managed_node_count'] in possible_node_counts
    assert 'reporting_time' in usage


def test_meter_billing_ok(cba_config):
    test_dimensions = {}
    test_timestamp = datetime.now()
    test_uuid = uuid.uuid4()
    test_randval = 1

    with mock.patch(
        'csp_billing_adapter_test.plugin.uuid.uuid4',
        return_value=test_uuid
    ):
        with mock.patch(
            'csp_billing_adapter_test.plugin.randrange',
            return_value=test_randval
        ):
            billing_id = meter_billing(
                cba_config,
                test_dimensions,
                test_timestamp,
                '2024-10-02T17:58:09.985794+00:00',
                '2024-10-02T17:58:09.985794+00:00',
                dry_run=False
            )

            assert billing_id == str(test_uuid.hex)


def test_meter_billing_error(cba_config):
    test_dimensions = {}
    test_timestamp = datetime.now()
    test_randval = 4

    with mock.patch(
        'csp_billing_adapter_test.plugin.randrange',
        return_value=test_randval
    ):
        with raises(Exception):
            meter_billing(
                cba_config,
                test_dimensions,
                test_timestamp,
                '2024-10-02T17:58:09.985794+00:00',
                '2024-10-02T17:58:09.985794+00:00',
                dry_run=False
            )


def test_get_csp_name(cba_config):
    # ensure this matches what is specified in local_csp module.
    test_csp_name = 'local'

    csp_name = get_csp_name(cba_config)
    assert csp_name == test_csp_name


def test_get_account_info(cba_config):
    # ensure this matches what is specified in local_csp module.
    test_account_info = {
        'account_id': '123456789',
        'arch': 'x86_64',
        'cloud_provider': 'local'
    }

    account_info = get_account_info(cba_config)
    assert account_info == test_account_info
