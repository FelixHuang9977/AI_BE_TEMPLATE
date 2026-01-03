# Project Name:
    - diagbe

# Objective: 
    - this project is a backend service for AI diagnosis system.
    - it provide a restful api service for other projects to call (such as Cable Assembly Assist System, or Shop floor system)
    - this backend plays a role of a manager to manage the assemble test process. Developer will implement the assemble test process in assemble_test.py or assemble_test.bat or assemble_test.sh later.
    - this backend plays an interface for legacy diagnosis scripts (DIAG_SW) to send test state to SFC. 

# Technical stack:
    - it is a restful api service.
    - implement by fastapi.
    - it listen on port 9000
    - should be a daemon process
    - should be able to run on windows and linux
    - should be able to run as a service in linux
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
    - for each document, create both english version and chinese version; save the documents in docs folder; if exist, update it.
    - create/update system architecture in drawio xml format (system_architecture.drawio)
    - create/update operation sequence diagram in markdown format (operation_sequence_{operation_name}.md) for each operation
    - create/update test plan in markdown format (test_plan.md)
    - create/update test case in markdown format (test_case_{test_case_name}.md) for each test case
    - create/update design spec in markdown format (design_spec.md)

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
            "test_status": "string"   // "pending", "in_progress", "completed", "error"
        }
        - description: create a assemble test for specific cable_uid
        - it will fork a process to run the assemble test ()
        - it will return the test_id
        - in first version, it will call assemble_test.py or assemble_test.bat or assemble_test.sh with cable_uid and test_data as arguments to run the assemble test
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
            "test_status": "string"   // "pending", "in_progress", "completed", "failed"
        }
        - description: get a assemble test for specific test_id
        - it check the result of the assemble test from result_assemble_test_{test_id}.txt




