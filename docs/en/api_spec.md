# API Specification

## 1. API Goals and Use Case
The DIAGBE API serves as the backend interface for the AI Diagnosis System. Its primary goals are:
*   **Test Management**: Create, monitor, and manage fiber cable assembly tests initiated by the frontend (VI_BE).
*   **Process Orchestration**: Spawn and manage asynchronous test processes.
*   **State Persistence**: Store and retrieve FIM (Fiber Interface Module) states for legacy diagnosis scripts.
*   **Result Handling**: Provide access to test results and facilitate cleanup operations.

Common use cases include:
*   VI_BE requesting a new test run for a specific cable.
*   VI_BE polling for the status of an ongoing test.
*   Legacy scripts saving intermediate states during testing.
*   Admin clearing old logs and results.

## 2. API List

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/assemble_test` | POST | Create a new assemble test. |
| `/api/v1/assemble_test/{test_id}` | GET | Get status of an assemble test. |
| `/api/v1/assemble_test/{test_id}` | DELETE | Cancel a test. |
| `/api/v1/assemble_test_clear_old_result` | POST | Clear old test results. |
| `/api/v1/fim_state` | GET | Get all FIM states. |
| `/api/v1/fim_state/{rack_sn}` | GET | Get FIM state for a specific rack. |
| `/api/v1/fim_state/{rack_sn}/{test_round_id}` | GET | Get FIM state for a specific round. |
| `/api/v1/fim_state/{rack_sn}/{test_round_id}` | POST | Update FIM state. |
| `/api/v1/fim_state/{rack_sn}/{test_round_id}` | DELETE | Delete FIM state. |

## 3. Individual API Details

### /api/v1/assemble_test

#### **POST** /api/v1/assemble_test
Create a new assemble test.
*   **Request Body**:
    ```json
    {
        "cable_uid": "string",
        "test_data": "string",
        "test_id": "string"  // Optional. If exist, use it; if not exist, create a new test_id; if exist and conflict, return error
    }
    ```
*   **Response Body**:
    ```json
    {
        "cable_uid": "string",
        "test_id": "string",
        "test_status": "string" // "pending", "in_progress", "completed", "error"
    }
    ```
*   **Description**: Creates a new test ID, forks the assemble test process, and returns immediately.

### /api/v1/assemble_test/{test_id}

#### **GET** /api/v1/assemble_test/{test_id}
Get status of an assemble test.
*   **Response Body**:
    ```json
    {
        "cable_uid": "string",
        "test_id": "string",
        "test_status": "string"
    }
    ```
*   **Description**: Checks the result file to determine the current status.

#### **DELETE** /api/v1/assemble_test/{test_id}
Cancel a test.
*   **Description**: Attempts to kill the process and marks the result as deleted.

### /api/v1/assemble_test_clear_old_result

#### **POST** /api/v1/assemble_test_clear_old_result
Clear old test results.
*   **Request Body**:
    ```json
    {
        "days": 1
    }
    ```

### /api/v1/fim_state

#### **GET** /api/v1/fim_state
Get all FIM states.
*   **Response Body**:
    ```json
    {
        "all_rack": [
            {
                "rack_sn": "string",
                "test_round": [ ... ]
            }
        ]
    }
    ```

#### **GET** /api/v1/fim_state/{rack_sn}
Get FIM state for a specific rack.
*   **Response Body**:
    ```json
    {
        "rack_sn": "string",
        "test_round": [ ... ]
    }
    ```

#### **GET** /api/v1/fim_state/{rack_sn}/{test_round_id}
Get FIM state for a specific round.
*   **Response Body**: `FimStateRackItem` (similar to above but 1 round)

#### **POST** /api/v1/fim_state/{rack_sn}/{test_round_id}
Update FIM state.
*   **Request Body**:
    ```json
    {
        "rack_sn": "string",
        "test_round": [
            {
                 "test_round_id": 1,
                 "fim_state": { ... }
            }
        ]
    }
    ```
*   **Description**: Creates or updates the FIM state file `fim_state_{rack_sn}_{test_round_id}.json`.

#### **DELETE** /api/v1/fim_state/{rack_sn}/{test_round_id}
Delete FIM state.
*   **Description**: Deletes the corresponding JSON file.
