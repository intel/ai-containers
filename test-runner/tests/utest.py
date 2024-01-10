import pytest
import yaml

from test_runner import Test

@pytest.fixture
def test_input():
    tests_list = []
    with open("tests.yaml", "r", encoding="utf-8") as test_file:
        try:
            tests_json = yaml.full_load(test_file)
        except yaml.YAMLError as yaml_exc:
            pytest.raises(yaml_exc)
            for test in tests_json:
                tests_list[test] = tests_json[test]
    return [Test(test, tests_list[test]) for test in tests_list]


def test_container_run(test_input):
    for idx, test in enumerate(test_input):
        if hasattr(test, "img") and not hasattr(test, "serving") and idx == 0:
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
