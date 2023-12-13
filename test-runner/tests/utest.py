import pytest
import yaml

from test_runner import Test

@pytest.fixture
def test_input():
    with open("tests.yaml", "r", encoding="utf-8") as test_file:
        try:
            tests_json = yaml.full_load(test_file)
        except yaml.YAMLError as yaml_exc:
            pytest.raises(yaml_exc)
    return [Test(test, tests_json[test]) for test in tests_json]


def test_container_run(test_input):
    for test in test_input:
        if hasattr(test, "img") and not hasattr(test, "serving"):
            log, returncode = test.container_run()
            assert returncode == 0
            assert log == "expandvars"

def test_container_run_serving(test_input):
    for test in test_input:
        if hasattr(test, "img") and hasattr(test, "serving"):
            log, returncode = test.container_run()
            assert returncode == 0
            assert log == "Python 3.11.7"

def test_run(test_input):
    for test in test_input:
        if not hasattr(test, "img"):
            log, returncode = test.run()
            assert returncode == 0
            assert log == "Hello World"
