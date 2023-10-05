# Generic Test Runner

## Project Structure

```text
test-runner
├── README.md
├── requirements.txt
├── test_runner.py
├── tests
│   ├── __init__.py
│   └── utest.py
└── tests.yaml
```
## Pre-requisite for Jupyter Notebook testing

Install docker-buildx plugin to use the test runner. Refer to the [link](https://github.com/docker/buildx#manual-download) for installation instructions. This is only a pre-requisite if you want to take advantage of papermill testing for jupyter notebooks.

## Usage

```text
$ python test_runner.py --help
usage: test_runner.py [-h] [-f FILE_PATH] [-v] [-l LOGS_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file FILE_PATH
                        -f /path/to/tests.yaml
  -v, --verbose         DEBUG Loglevel
  -l LOGS_PATH, --logs LOGS_PATH
                        -l /path/to/logs
```

### Unit Testing

```bash
$ PYTHONPATH=$PWD/tests pytest tests/utest.py -W ignore::UserWarning
```

## Expected Output

Given a test input:
```yaml
test1:
  img: ${REGISTRY}/aiops/compose-dev:latest
  cmd: bash -c "head -n 1 /workspace/requirements.txt"
# device: /dev/dri
# ipc: host
  notebook: 'true'
  env:
    REGISTRY: ${REGISTRY}
    DEBUG: "true"
  volumes:
    - src: /tf_dataset
      dst: /tmp
    - src: $PWD
      dst: /workspace
test2:
  cmd: echo -n $TEST && python -c 'print(" World", end="")'
  env:
    TEST: Hello
```

```text
$ python test_runner.py -f tests.yaml 
2023-08-25 12:30:53,004 - root - INFO - Setup Completed - Running Tests
2023-08-25 12:30:53,004 - root - INFO - test1 Started
2023-08-25 12:30:53,700 - root - INFO - python_on_whales
2023-08-25 12:30:53,701 - root - INFO - test2 Started
2023-08-25 12:30:53,731 - root - INFO - Test Output: Hello World
2023-08-25 12:30:53,734 - root - INFO - 
|   # | Test   | Status   |
|-----+--------+----------|
|   1 | test1  | Pass     |
|   2 | test2  | Pass     |
```
