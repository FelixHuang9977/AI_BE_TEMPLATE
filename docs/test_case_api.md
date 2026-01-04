# Test Cases: API

## TC01: Create Assemble Test (Success)
- **Input**: `POST /api/v1/assemble_test` with valid `cable_uid`, `test_data`.
- **Expected**: HTTP 200, returns `test_id`, `test_status="pending"`.

## TC02: Check Status (Assemble Test)
- **Input**: `GET /api/v1/assemble_test/{test_id}`.
- **Expected**: HTTP 200, returns current status.

## TC03: FIM State CRUD
- **Create**: `POST /api/v1/fim_state/{rack}/{round}` -> HTTP 200.
- **Read**: `GET /api/v1/fim_state/{rack}/{round}` -> HTTP 200 with data.
- **Delete**: `DELETE /api/v1/fim_state/{rack}/{round}` -> HTTP 200.

## TC04: Real Integration
- **Scenario**: Run full cycle with real script spawning.
- **Env**: Configure `.env` with `production_url_base`.
