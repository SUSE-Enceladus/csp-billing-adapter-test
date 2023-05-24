# CSP Billing Adapter Test Plugin

This is a plugin for
[csp-billing-adapter](https://github.com/SUSE-Enceladus/csp-billing-adapter)
that provides CSP and get usage data hook implementations. This includes the
hooks defined in the
[csp_hookspecs.py module](https://github.com/SUSE-Enceladus/csp-billing-adapter/blob/main/csp_billing_adapter/csp_hookspecs.py).

## Meter billing

The `meter_billing` function accepts a dictionary mapping of dimension name
to usage quantity. This information is used to mock a metered bill. This
function is mocked to fail 5% of the time.

## Get CSP Name

The `get_csp_name` function returns a mocked name of *local*.

## Get Account Info

The `get_account_info` function provides mocked metadata information.
The structure of this information is as follows:

```
{
    "account_id": "123456789",
    "arch": "x86_64",
    "cloud_provider": "local"
}
```

## Get Usage Data

The `get_usage_data` function returns a usage dictionary with a random
usage count for the usage value `managed_node_count`.

There are 6 possible weighted usage values that can be returned. The
format of the return dictionary is as follows:

```
{
    "managed_node_count": 25,
    "reporting_time": "2023-03-10T20:50:00.000000+00:00",
    "base_product": "cpe:/o:suse:product:v1.2.3"
}
```
