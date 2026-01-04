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

    1. create a README.md for how to launch, install, run, stop, and deploy, and basic test
       - explain how to do simple test by curl to create a test, get all pending tests, stop the test.
       - add example for how to use predefined test_id=1 to create a test and get the test status and stop the test. let all steps in single session. one section for linux user; another section for windows powershell user.

    2. create requirements.txt for dependencies
    3. create a systemd service file for the backend service
    4. create a standard python project structure (refer: https://retailtechinnovationhub.com/home/2024/2/29/the-ultimate-guide-to-structuring-a-python-package)
    5. create test cases by pytest
    6. create .gitignore file
    7. create .github/workflows/ci.yml for github actions
    8. create pyproject.toml for project metadata
    9. the backend should call the assemble_test.py or assemble_test.bat or assemble_test.sh in not-block mode. the API should return immediately after the process is started.
    10. if folder not exist, create it.
    11. create vscode launch.json for debugging
    12. create .env for environment variables
        - production_url_base: the production url base for API test
            * example: http://192.168.1.100:9000
            * use http://localhost:9000 by default
        - production_api_key: the production api key for API test
            * example: 123456
            * use 123456 by default

# system operations
    - Participant:
        * diagbe (DIAG_BE): the backend service
        * cable assembly assist system (VI_BE): the frontend service
        * shop floor system (SFC): the shop floor system
        * legacy diagnosis scripts (DIAG_SW): the legacy diagnosis scripts
        * admin (ADMIN): the person who maintain the system
        * operator (OPERATOR): the person who assemble the fiber cables

    - Operation 1: (initiator: VI_BE)  
        * cable assembly assist system call DIAG_BE api to test if old test id exist; if exist, VI_BE to decide to delete or stop the old test or abort.
        * VI_BE call DIAG_BE api to create a assemble test
        * DIAG_BE create a assemble test and return the test_id
        * DIAG_BE call the assemble_test.py or assemble_test.bat or assemble_test.sh in not-block mode
        * DIAG_BE return immediately after the process is started
        * DIAG_BE will monitor the assemble test process by call API to check test status and update the test status

    - Operation 2: (initiator: VI_BE)  
        * VI_BE will check test status by call API to check test status and update the test status 
        * if test status is completed, VI_BE will ask operator assemble next fiber cables
        * if test status is error, VI_BE will ask operator/ADMIN to decide to delete or stop the test
        * if test status is pending/in_progress, VI_BE will notify operator to wait for the test to complete

    - Operation 3: (initiator: DIAG_SW)  
        * legacy diagnosis scripts call DIAG_BE api to push test result to SFC to save test state for next test rounds.

    - Operation 4: (initiator: ADMIN)  
        * admin call DIAG_BE api to cancel or stop a assemble test or clear old test result
        * DIAG_BE cancel or stop the assemble test or clear old test result

    - Operation 5: (initiator: ADMIN)  
        * ADMIN will monitor all running assemble test process by call API (/api/v1/assemble_test) to get test status.

# Test:
    - create test cases by pytest
    - for test case, should emulate a long run process(like sleep 5 seconds); 

# Document:
    - for each document, create both english version and chinese version; save the documents in docs folder; if exist, update it according to language.
    - create/update system architecture in drawio xml format (docs/[en|zh]/system_architecture.drawio)
    - create/update operation sequence diagram in markdown format (docs/[en|zh]/operation_sequence_{seq}_{operation_name}.md) for each operation
    - create/update test plan in markdown format (docs/[en|zh]/test_plan.md)
    - create/update test case in markdown format (docs/[en|zh]/test_case_{test_case_name}.md) for each test case
    - create/update design spec in markdown format (docs/[en|zh]/design_spec.md)
    - create/update README.md in markdown format (docs/[en|zh]/README.md)
        - should include how to launch, install, and deploy 
        - should include how to check if port 9000 is used
        - should include how to start/stop the backend service
        - should include how to use git to checkout to specific branch
    - create/update LICENSE.md in markdown format (LICENSE.md)
    - for drawio format document, no background color (labelBackgroundColor=none).
    - create/update the API spec in markdown format (docs/[en|zh]/api_spec.md); i will provide this to other team members to implement the API. should have below sections:
        - API Goals and Use Case
        - API list (all support APIs in a table format)
        - individual API: name, method, request body, response body, description, and example.

# api list:
    1. /api/v1/assemble_test
        - method: get
        - response body: 
        {
            "all_test": [
                {
                    "cable_uid": "string",
                    "test_id": "string",
                    "process_id": "string",
                    "test_status": "string"   // "pending", "in_progress", "completed", "error"
                }
            ]
        }
        - description: get all assemble test
        - it will read all .tmp.{test_id}.pid files and return the test_id, process_id, test_status

    2. /api/v1/assemble_test
        - method: post
        - request body: 
        {
            "cable_uid": "string",
            "test_data": "string",
            "test_id": "string"  // if exist, use it; if not exist, create a new test_id; if exist, return error
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

    3. /api/v1/assemble_test/{test_id}
        - method: get
        - response body: 
        {
            "cable_uid": "string",
            "test_id": "string",
            "process_id": "string",
            "test_status": "string"   // "pending", "in_progress", "completed", "error"
        }
        - description: get a assemble test for specific test_id
        - it check the result of the assemble test from .tmp.result_assemble_test_{test_id}.txt

    4. /api/v1/assemble_test/{test_id}
        - method: delete
        - description: delete or cancel a assemble test for specific test_id
        - read process_id from .tmp.{test_id}.pid, try to kill the process if it is running.
        - delete the .tmp.{test_id}.pid file
        - rename the .tmp.result_assemble_test_{test_id}.txt to .tmp.result_assemble_test_{test_id}_deleted.txt

    5. /api/v1/assemble_test_clear_old_result
        - method: post
        - request body: 
        {
            "days": "int"
        }
        - description: delete old result files
        - it will delete the result files and pid files which is older than {days} days
        - if not specify days, default to 1 days
        - if days is 0, delete all old result files and pid files.

    6. /api/v1/fim_state
        - method: get
        - response body: 
        {
            "all_rack": [
                {
                    "rack_sn": "string",
                    "test_round": [
                        {
                            "test_round_id": "int",
                            "fim_state": "dict object"
                        },
                        {
                            "test_round_id": "int",
                            "fim_state": "dict object"
                        }
                    ]
                }
            ]
        }
        - description: get fim state for all rack_sn

    7. /api/v1/fim_state/{rack_sn}
        - method: get
        - response body: 
        {
            "rack_sn": "string",
            "test_round": [
                {
                    "test_round_id": "int",
                    "fim_state": "dict object"
                },
                {
                    "test_round_id": "int",
                    "fim_state": "dict object"
                }
            ]
        }
        - description: get fim state for specific rack_sn

    8. /api/v1/fim_state/{rack_sn}/{test_round_id}
        - method: get
        - response body: 
        {
            "rack_sn": "string",
            "test_round": [
                {
                    "test_round_id": "int",
                    "fim_state": "dict object"
                }
            ]
        }
        - description: get fim state for specific rack_sn
        - note: keep the redundant data (rack_sn, test_round_id) for get/set; the caller can parse it easily

    9. /api/v1/fim_state/{rack_sn}/{test_round_id}
        - method: post
        - request body: 
        {
            "rack_sn": "string",
            "test_round": [
                {
                    "test_round_id": "int",
                    "fim_state": "dict object"
                }
            ]
        }
        - description: update fim state for specific rack_sn and specific test_round_id
        - if rack_sn doesn't exist, create it
        - if test_round_id doesn't exist, create it and append to the rack_sn
        - if item with test_round_id exist, update it
        - save the fim state to fim_state_{rack_sn}_{test_round_id}.json
        - fim_state will be defined by DIAG_SW, just treat it as raw json data
        - note: keep the redundant data (rack_sn, test_round_id) for get/set; the caller can parse it easily
        
    10. /api/v1/fim_state/{rack_sn}/{test_round_id}
        - method: delete
        - description: delete fim state for specific rack_sn and specific test_round_id
        - delete the fim_state_{rack_sn}_{test_round_id}.json

# Implementation Addon:
    - for get /api/v1/assemble_test/ test case, should implement independent files to check different test_status; especially for "pending" and "in_progress", the dummy function should sleep for a while to simulate the test process
    - add verbose option to pytest to show more detailed information
    - for mock scripts, add mock to file name prefix. such as mock_assemble_test.py
    - for mock-based test cases, add mock to file name prefix. such as test_mock_xxx.py
    - create a test case, name as test_real_xxx.py, to test the real assemble test process; don't use mock scripts; use real assemble test scripts; don't use unittest.mock module; call the API to perform the assemble test process; use simple http client to call the API:  get /api/v1/assemble_test/ and post /api/v1/assemble_test/ 

# Update Testcase and do sanity check after implementation:
    - I already use git to do version control, if you modified any code or add/del any operations, you add test cases to test the modified code or operations.
    - for test cases, you should implement independent files to mock-based and real cases.
    - for mock-based test cases, add mock to file name prefix. such as test_mock_xxx.py
    - for real cases, add real to file name prefix. such as test_real_xxx.py
    - for real cases, read .env file to get production_url_base and production_api_key to call the API        

# Sanity check after implementation:
    - should use pytest to run the test cases after implementation
    - if any test case failed, you should review your design and fix it and run the test cases again
    - if all test cases passed, you should update the documents and notify me

# Update Doc after implementation:
    - if docs folder not exist, it means that I would like to rebuild all documents, you should create the docs folder and rebuild all documents I requested.
    - I already use git to do version control, if you modified any code, you are free to recheck all related documents and update all documents without asking me.
