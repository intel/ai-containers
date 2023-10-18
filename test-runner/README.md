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

## Usage
The Test Runner CLI is intended to be used manually to verify that your config file works properly, and then automatically later to verify those changes work in a default validation environment.

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

When running tests, the Test Runner chooses `PASS` or `FAIL` based on the exit code of the application that was run with the `cmd` field in your test config. When writing tests, ensure that the application succeeds/fails according to the expected state of the application. The following code snippet describes the logical flow of the Test Runner Application for each test: 

```python
ERROR = False
for idx, test in enumerate(tests):
  # ...
  try:
      log, returncode = test.container_run() if hasattr(test, "img") else test.run()
  except:
      summary.append([idx + 1, test.name, "FAIL"])
      ERROR = True
      continue # skip next line
  summary.append([idx + 1, test.name, "PASS"])
# ...
if ERROR:
    exit(1)
```

>Note: The Test Runner Application's PASS/FAIL message and exit code are determined by the executed subprocess raising an exception during runtime. If for whatever reason the execution of the `container_run()` or `run()` functions would yield no log outputs, then the state of the host's environment does not match the pre-requisites for `test_runner.py` to be executed with that configuration.

### Unit Testing

```bash
$ PYTHONPATH=$PWD/tests pytest tests/utest.py -W ignore::UserWarning
```

## Composite Action

This action clones a version of this repo with test-runner and runs the application on a given directory.

Inputs for the action:

```yaml
inputs:
  mlops_repo:
    description: 'Test Runner org/repo'
    required: true
    type: string
  mlops_ref:
    description: 'Test Runner Branch/Tag'
    required: false
    default: develop
    type: string
  registry:
    description: 'Container Registry URL'
    required: true
    type: string
  test_dir:
    description: 'Directory with tests.yaml to test'
    required: true
    type: string
  token:
    required: true
    type: string
```

Example Implementation of the action:

```yaml
test-containers:
  runs-on: [ self-hosted, Linux, validation ]
  steps:
    - uses: actions/checkout@v4
    - uses: docker/login-action@v3
      with:
        registry: ${{ vars.REGISTRY }}
        username: ${{ secrets.REGISTRY_USER }}
        password: ${{ secrets.REGISTRY_TOKEN }}
    - name: Test Container Group
      uses: intel/ai-containers/test-runner@main
      with:
        mlops_repo: intel/ai-containers
        registry: ${{ vars.REGISTRY }}
        test_dir: /path/to/test/dir
        token: ${{ github.token }}
```

## Expected Output

Given a test input:
```yaml
test1:
  img: ${REGISTRY}/aiops/compose-dev:latest # var substitution inline
  cmd: bash -c "head -n 1 /workspace/requirements.txt" # volume mounted file
# device: /dev/dri
# ipc: host
  notebook: 'true' # single quotes
  env:
    REGISTRY: ${REGISTRY} # substitute env from host
    DEBUG: "true" # double quotes
  volumes:
    - src: /tf_dataset
      dst: /tmp
    - src: $PWD
      dst: /workspace
test2:
  cmd: echo -n $TEST && python -c 'print(" World", end="")' # var substitution inline
  env:
    TEST: Hello
test3:
  img: ${REGISTRY}/aiops/compose-dev:latest # python 3.10
  cmd: python --version # will return python 3.11
  serving: 'true'
```

```text
$ python test_runner.py -f tests.yaml 
2023-10-17 17:13:24,380 - root - INFO - Setup Completed - Running Tests
2023-10-17 17:13:24,380 - root - INFO - Running Test: test1
2023-10-17 17:13:25,621 - root - INFO - expandvars
2023-10-17 17:13:25,870 - root - INFO - Running Test: test2
2023-10-17 17:13:25,870 - root - INFO - test2 Started
2023-10-17 17:13:25,886 - root - INFO - Test Output: Hello World
2023-10-17 17:13:25,886 - root - INFO - Running Test: test3
2023-10-17 17:13:26,641 - root - INFO - Python 3.11.6
2023-10-17 17:13:27,142 - root - INFO - 
|   # | Test   | Status   |
|-----+--------+----------|
|   1 | test1  | PASS     |
|   2 | test2  | PASS     |
|   3 | test3  | PASS     |
```
