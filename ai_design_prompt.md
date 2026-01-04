# Project Name:
    - diagbe

# Objective: 
    - this project is a backend service for AI diagnosis system.
    - it provide a restful api service for other projects to call (such as Cable Assembly Assist System, or Shop floor system)
    - this backend plays a role of a manager to manage the assemble test process. Developer will implement the assemble test process in assemble_test.py or assemble_test.bat or assemble_test.sh later.
    - this backend plays an interface for legacy diagnosis scripts (DIAG_SW) to send test state to SFC. 

# Technical stack:
    - it is a restful api service.
    - implement by python, fastapi.
    - create python virtual environment by venv
    - it listen on port 9000
    - should be a daemon process
    - should be able to run on windows and linux
    - should be able to run as a service in linux;  (ignore this in windows)
    - should be able to deploy by pip by wheel
    - support CI by github actions

# Deployment:
    - should be able to deploy by pip by wheel
    - should be able to run as a service in linux
    - should be able to run on windows

# Implementation:

    1. create a README.md for how to launch, install, and deploy
    2. create requirements.txt for dependencies
    3. create a systemd service file for the backend service
    4. create a standard python project structure (refer: https://retailtechinnovationhub.com/home/2024/2/29/the-ultimate-guide-to-structuring-a-python-package)
    5. create test cases by pytest
    6. create .gitignore file
    7. create .github/workflows/ci.yml for github actions
    8. create pyproject.toml for project metadata
    9. the backend should call the assemble_test.py or assemble_test.bat or assemble_test.sh in not-block mode. the API should return immediately after the process is started.
    10. if folder not exist, create it.

# system operations
    - Participant:
        * diagbe (DIAG_BE)
        * cable assembly assist system (VI_BE)
        * shop floor system (SFC)
        * legacy diagnosis scripts (DIAG_SW)
    - Operation 1: (initiator: VI_BE)  
        * cable assembly assist system call DIAG_BE api to test if old test id exist; if exist, VI_BE to decide to delete or stop the old test or abort.
        * VI_BE call DIAG_BE api to create a assemble test
        * DIAG_BE create a assemble test and return the test_id
        * DIAG_BE call the assemble_test.py or assemble_test.bat or assemble_test.sh in not-block mode
        * DIAG_BE return immediately after the process is started
        * DIAG_BE will monitor the assemble test process by call API to check test status and update the test status

    - Operation 2: 
        * shop floor system call DIAG_BE api to get a assemble test status


# Test:
    - create test cases by pytest
    - for test case, should emulate a long run process(like sleep 5 seconds); 

# Document:
    - for each document, create both english version and chinese version; save the documents in docs folder; if exist, update it according to language.
    - create/update system architecture in drawio xml format (system_architecture.drawio)
    - create/update operation sequence diagram in markdown format (operation_sequence_{operation_name}.md) for each operation
    - create/update test plan in markdown format (test_plan.md)
    - create/update test case in markdown format (test_case_{test_case_name}.md) for each test case
    - create/update design spec in markdown format (design_spec.md)
    - create/update README.md in markdown format (README.md, README_zh.md)
        - should include how to launch, install, and deploy 
        - should include how to check if port 9000 is used
        - should include how to start/stop the backend service
        - should include how to use git to checkout to specific branch
    - create/update LICENSE.md in markdown format (LICENSE.md)
    - for drawio format document, use black font color and white background color.

# api list:

    1. /api/v1/assemble_test
        - method: post
        - request body: 
        {
            "cable_uid": "string",
            "test_data": "string"
        }
        - response body: 
        {
            "cable_uid": "string",
            "test_id": "string",
            "process_id": "string",
            "test_status": "string"   // "pending", "in_progress", "completed", "error"
        }
        - description: create a assemble test for specific cable_uid
        - the backend will create a test_id (start from 1 and increment by 1) and pass it to the assemble test script
        - it will fork a process to run the assemble test script, record the process id, save process_id to .tmp.{test_id}.pid
        - it will return the test_id and process_id to the API caller
        - in first version, it will call assemble_test.py or assemble_test.bat or assemble_test.sh with test_id, cable_uid and test_data as arguments to run the assemble test
            - assemble_test.py is a python script to run the assemble test
            - assemble_test.bat is a batch script to run the assemble test
            - assemble_test.sh is a shell script to run the assemble test
            - search the assemble_test.py or assemble_test.bat or assemble_test.sh in the same directory as the backend service
            - if found, run it
            - if not found, return error

    2. /api/v1/assemble_test/{test_id}
        - method: get
        - response body: 
        {
            "cable_uid": "string",
            "test_id": "string",
            "process_id": "string",
            "test_status": "string"   // "pending", "in_progress", "completed", "failed"
        }
        - description: get a assemble test for specific test_id
        - it check the result of the assemble test from result_assemble_test_{test_id}.txt

    3. /api/v1/assemble_test/{test_id}
        - method: delete
        - description: delete or cancel a assemble test for specific test_id
        - read process_id from .tmp.{test_id}.pid, try to kill the process if it is running.
        - delete the .tmp.{test_id}.pid file
        - rename the result_assemble_test_{test_id}.txt to result_assemble_test_{test_id}_deleted.txt

    4. /api/v1/assemble_test_clear_old_result
        - method: post
        - request body: 
        {
            "days": "int"
        }
        - description: delete old result files
        - it will delete the result files and pid files which is older than {days} days
        - if not specify days, default to 1 days
        - if days is 0, delete all old result files and pid files.

# Implementation Addon:
    - for get /api/v1/assemble_test/ test case, should implement independent files to check different test_status; especially for "pending" and "in_progress", the dummy function should sleep for a while to simulate the test process
    - add verbose option to pytest to show more detailed information
    - for mock scripts, add mock to file name prefix. such as mock_assemble_test.py
    - for mock-based test cases, add mock to file name prefix. such as test_mock_xxx.py
    - create a test case, name as test_real_xxx.py, to test the real assemble test process; don't use mock scripts; use real assemble test scripts; don't use unittest.mock module; call the API to perform the assemble test process; use simple http client to call the API:  get /api/v1/assemble_test/ and post /api/v1/assemble_test/ 

# Update Doc after implementation:
    - I already use git to do version control, if you modified any code, you are free to recheck all related documents and update all documents without asking me.