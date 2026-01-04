# AI Diagnosis Backend Service

This is a RESTful API service for the AI diagnosis system, built with FastAPI.

## Requirements

- Python 3.8+
- `pip`

## Installation

### From Source

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Via Pip (Wheel)

To build the wheel:
```bash
pip install build
python -m build
```
This will create a `.whl` file in the `dist/` directory, which can be installed via pip:
```bash
pip install dist/ai_diagbe-0.1.0-py3-none-any.whl
```

## Deployment

### Check Port Usage
Ensure port 9000 is free before starting.
- **Windows**: `netstat -ano | findstr :9000`
- **Linux**: `ss -lptn | grep :9000`

### Running the Service

#### Manual Start

Start the backend server on port 9000:
```bash
python -m app.main
```
Or using uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

#### Systemd Service (Linux)
1. Copy service file: `sudo cp ai_diagbe.service /etc/systemd/system/`
2. Reload daemon: `sudo systemctl daemon-reload`
3. Enable service: `sudo systemctl enable ai_diagbe`
4. Start service: `sudo systemctl start ai_diagbe`
5. Stop service: `sudo systemctl stop ai_diagbe`
6. Check status: `sudo systemctl status ai_diagbe`

### Basic Test (Curl)

You can perform a simple test using `curl`. 
> **Note for Windows PowerShell Users**: PowerShell aliases `curl` to `Invoke-WebRequest`. To use native curl, use `curl.exe`.  
> **Important**: When using `curl.exe` in PowerShell, you must wrap the JSON body in single quotes and **escape internal double quotes with a backslash**.  
> Example: `-d '{\"key\": \"value\"}'`

1. **Create a test**:
   
   **Bash / Command Prompt**:
   ```bash
   curl -X POST "http://localhost:9000/api/v1/assemble_test" -H "Content-Type: application/json" -d "{\"cable_uid\": \"CABLE-TEST-01\", \"test_data\": \"demo\"}"
   ```

   **PowerShell**:
   ```powershell
   curl.exe -X POST "http://localhost:9000/api/v1/assemble_test" -H "Content-Type: application/json" -d '{\"cable_uid\": \"CABLE-TEST-01\", \"test_data\": \"demo\"}'
   ```

2. **Check status** (replace `{test_id}` with the ID from the response):
   ```bash
   curl "http://localhost:9000/api/v1/assemble_test/{test_id}"
   ```

3. **Get all tests**:
   ```bash
   curl "http://localhost:9000/api/v1/assemble_test"
   ```

4. **Stop/Delete a test**:
   ```bash
   curl -X DELETE "http://localhost:9000/api/v1/assemble_test/{test_id}"
   ```

## Development

### Git Workflow
Checkout specific branch:
```bash
git checkout <branch_name>
```

### Running Tests
Run pytest with verbose output:
```bash
pytest -v
```

#### Real Process Verification
Run the real assemble test process verification (no mocks):
```bash
pytest -v tests/test_real_assemble_test.py
```

## API Endpoints

### 1. Create Assemble Test
**POST** `/api/v1/assemble_test`

Request Body:
```json
{
    "cable_uid": "string",
    "test_data": "string"
}
```

Response:
```json
{
    "cable_uid": "string",
    "test_id": "uuid-string",
    "test_status": "pending"
}
```

### 2. Get Test Status
**GET** `/api/v1/assemble_test/{test_id}`

Response:
```json
{
    "cable_uid": "string",
    "test_id": "string",
    "test_status": "pending | in_progress | completed | error"
}
```
