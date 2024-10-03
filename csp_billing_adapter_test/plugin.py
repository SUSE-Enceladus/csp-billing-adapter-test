#
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

"""
Pluggy hook implementations emulating CSP interactions.

Note that the meter_billing can fail with a generic exception raised
5% of the time.
"""

import logging
import uuid

from random import choices, randrange
from datetime import datetime

import csp_billing_adapter

from csp_billing_adapter.config import Config
from csp_billing_adapter.utils import get_now, date_to_string

log = logging.getLogger('CSPBillingAdapter')


@csp_billing_adapter.hookimpl(trylast=True)
def meter_billing(
    config: Config,
    dimensions: dict,
    timestamp: datetime,
    billing_period_start: str,
    billing_period_end: str,
    dry_run: bool
) -> str:
    """Simulate a CSP metering operation with a 5% chance of failure."""
    log.info('Mock CSP received metering of: %s', dimensions)
    seed = randrange(20)

    if seed == 4:
        log.warning("Simulating failed metering operation")
        raise Exception('Unable to submit meter usage. Payment not billed!')
    else:
        return str(uuid.uuid4().hex)


@csp_billing_adapter.hookimpl(trylast=True)
def get_csp_name(config: Config) -> str:
    """Return the 'local' CSP's name."""
    return 'local'


@csp_billing_adapter.hookimpl(trylast=True)
def get_account_info(config: Config) -> str:
    """Return the 'local' CSP's account info."""
    return {
        'account_id': '123456789',
        'arch': 'x86_64',
        'cloud_provider': 'local'
    }


@csp_billing_adapter.hookimpl(trylast=True)
def get_usage_data(config: Config) -> dict:
    """
    Simulate a CSP usage data retrieval returning one of four possible
    usage values.
    """

    quantity = choices(
        [9, 10, 11, 25, 30, 100],
        weights=(.19, .19, .19, .19, .19, .05),
        k=1
    )[0]

    usage = {
        'managed_node_count': quantity,
        'reporting_time': date_to_string(get_now()),
        'base_product': 'cpe:/o:suse:product:v1.2.3'
    }

    log.info("Simulated Usage data: %s", usage)

    return usage
