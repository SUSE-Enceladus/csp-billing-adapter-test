import pathlib
import yaml

import pytest

from csp_billing_adapter.config import Config


def pytest_configure(config):
    """Custom pytest configuration."""

    # configure custom markers
    config.addinivalue_line(
        "markers", ('config: the config file path to load')
    )


@pytest.fixture(scope="session")
def data_dir(pytestconfig):
    """
    Fixture returning the path to the data directory under the tests
    area for this pytest run.
    """
    # Get testing root directory, supporting older versions of
    # pytest that don't have rootpath
    if hasattr(pytestconfig, 'rootpath'):
        testroot = pytestconfig.rootpath
    else:
        testroot = pathlib.Path(pytestconfig.rootdir)

    return testroot / "tests/data"


@pytest.fixture
def cba_config_path(data_dir, request):
    """
    Fixture returning the path to the config file to load, as specified
    by the config marker, defaulting to a known good config if none is
    specified.
    """
    config_marker = request.node.get_closest_marker('config')
    if config_marker:
        config_file = config_marker.args[0]
    else:
        config_file = 'good_config.yaml'

    return data_dir / config_file


@pytest.fixture
def cba_config(cba_config_path):
    """
    Fixture returning a Config object loaded from the config
    file specified by the cba_config_path fixture.
    """
    with cba_config_path.open() as conf_fp:
        config = yaml.safe_load(conf_fp)

    return Config(config)
