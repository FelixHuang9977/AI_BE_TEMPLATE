# API Specification (diagbe)

## Summary
The **diagbe** service provides a RESTful API to manage the cable assembly test process. It serves as a bridge between the Cable Assembly Assist System (VI_BE) and the backend test execution, as well as providing status updates to the Shop Floor System (SFC).

The API runs on port **9000**.

## API List

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/assemble_test` | Create a new assembly test |
| `GET` | `/api/v1/assemble_test/{test_id}` | Get status of an assembly test |
| `DELETE` | `/api/v1/assemble_test/{test_id}` | Cancel/Delete an assembly test |
| `POST` | `/api/v1/assemble_test_clear_old_result` | Clear old result files |

## APIs

### 1. Create Assemble Test
Creates a new assembly test, generates a test ID, and launches the test process in the background.

- **Name**: Create Assemble Test
- **Method**: `POST`
- **URL**: `/api/v1/assemble_test`
- **Description**: This endpoint initiates a new test session. It forks a non-blocking process to run the `assemble_test` script and returns immediately with a `pending` status.

#### Request Body
```json
{
    "cable_uid": "string",
    "test_data": "string"
}
```

#### Response Body
```json
{
    "cable_uid": "string",
    "test_id": "string",
    "process_id": "string",
    "test_status": "string"   // "pending", "in_progress", "completed", "error"
}
```

#### Example
**Request:**
```http
POST /api/v1/assemble_test HTTP/1.1
Content-Type: application/json

{
    "cable_uid": "CABLE-2024-001",
    "test_data": "config_v1"
}
```

**Response:**
```json
{
    "cable_uid": "CABLE-2024-001",
    "test_id": "550e8400-e29b-41d4-a716-446655440000",
    "process_id": "12345",
    "test_status": "pending"
}
```

---

### 2. Get Assemble Test Status
Retrieves the current status of a specific assembly test.

- **Name**: Get Assemble Test Status
- **Method**: `GET`
- **URL**: `/api/v1/assemble_test/{test_id}`
- **Description**: Checks the status of the test by reading the result file `.tmp.result_assemble_test_{test_id}.txt`.

#### Request Parameters
- `test_id`: The unique identifier of the test.

#### Response Body
```json
{
    "cable_uid": "string",
    "test_id": "string",
    "process_id": "string",
    "test_status": "string"   // "pending", "in_progress", "completed", "failed"
}
```

#### Example
**Request:**
```http
GET /api/v1/assemble_test/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
```

**Response:**
```json
{
    "cable_uid": "CABLE-2024-001",
    "test_id": "550e8400-e29b-41d4-a716-446655440000",
    "process_id": "12345",
    "test_status": "completed"
}
```

---

### 3. Delete/Cancel Assemble Test
Cancels a running test or removes test records.

- **Name**: Delete Assemble Test
- **Method**: `DELETE`
- **URL**: `/api/v1/assemble_test/{test_id}`
- **Description**: Reads the process ID from `.tmp.{test_id}.pid`, terminates the process if running, deletes the PID file, and renames the result file to indicate deletion.

#### Request Parameters
- `test_id`: The unique identifier of the test.

#### Example
**Request:**
```http
DELETE /api/v1/assemble_test/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
```

**Response:**
*Status Code: 200 OK* (or specific message)

---

### 4. Clear Old Results
Cleans up old result files and PID files from the system.

- **Name**: Clear Old Results
- **Method**: `POST`
- **URL**: `/api/v1/assemble_test_clear_old_result`
- **Description**: Deletes result files and PID files older than the specified number of days.

#### Request Body
```json
{
    "days": "int"
}
```
*   `days`: (Optional) Number of days to retain files. Default is 1. If 0, deletes all.

#### Example
**Request:**
```http
POST /api/v1/assemble_test_clear_old_result HTTP/1.1
Content-Type: application/json

{
    "days": 7
}
```

**Response:**
*Status Code: 200 OK*
