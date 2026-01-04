# Design Specification - DIAGBE

## 1. Introduction
This project (**diagbe**) is a backend service for the AI Diagnosis System. It functions as a manager to handle the assemble test process and serves as an interface for legacy diagnosis scripts (DIAG_SW) to communicate with the Shop Floor System (SFC).

## 2. Technical Stack
- **Type**: RESTful API Service
- **Framework**: FastAPI (Python)
- **Port**: 9000
- **Process Model**: Daemon process
- **OS Support**: Windows and Linux
- **Deployment**: Pip / Wheel
- **CI/CD**: GitHub Actions

## 3. System Operations

### 3.1 Participants
- **DIAG_BE**: This backend service (AI Diagnosis Backend).
- **VI_BE**: Cable Assembly Assist System.
- **SFC**: Shop Floor System.
- **DIAG_SW**: Legacy diagnosis scripts.

### 3.2 Operations
**Operation 1: Cable Assembly Test (Initiated by VI_BE)**
1.  **Check/Delete Old Test**: VI_BE calls DIAG_BE to check if a test ID exists (decides to delete/stop/abort).
2.  **Create Test**: VI_BE calls DIAG_BE `POST /api/v1/assemble_test` to create a new test.
3.  **Process Fork**: DIAG_BE returns a `test_id` immediately and forks a non-blocking process to run the actual test (calling `assemble_test.py`, `.bat`, or `.sh`).
4.  **Monitor**: DIAG_BE monitors the process status (via result file polling or other mechanisms).

**Operation 2: Status Check (Initiated by SFC)**
1.  **Get Status**: SFC calls DIAG_BE `GET /api/v1/assemble_test/{test_id}`.
2.  **Response**: DIAG_BE checks the result file (`.tmp.result_assemble_test_{test_id}.txt`) and returns the status.

## 4. API Specification

### 4.1 Create Assemble Test
- **Endpoint**: `/api/v1/assemble_test`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "cable_uid": "string",
      "test_data": "string"
  }
  ```
- **Response Body**:
  ```json
  {
      "cable_uid": "string",
      "test_id": "string",
      "test_status": "string"
  }
  ```
- **Description**: Creates a test, forks a process, and returns immediately.

### 4.2 Get Assemble Test Status
- **Endpoint**: `/api/v1/assemble_test/{test_id}`
- **Method**: `GET`
- **Response Body**:
  ```json
    {
        "cable_uid": "string",
        "test_id": "string",
        "test_status": "string"
    }
  ```
- **Description**: checks `.tmp.result_assemble_test_{test_id}.txt` for status.

## 5. Implementation Details
- The backend must call the external script (`assemble_test.py/bat/sh`) in a **non-blocking** mode.
- The script is searched for in the service directory (priority: py > bat > sh).
- **Verification**: 
    - `tests/test_mock_integration_states.py` uses mock scripts (`scripts/mock_*.py`) to verify state transitions.
    - `tests/test_real_assemble_test.py` uses the real `scripts/assemble_test.py` to verify the full non-blocking lifecycle without mocks.
