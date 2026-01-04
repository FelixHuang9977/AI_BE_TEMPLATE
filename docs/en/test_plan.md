# Test Plan

## 1. Objective
To verify the functionality, performance, and reliability of the AI Diagnosis Backend Service (DIAG_BE).

## 2. Scope
- **Assemble Test API**: Verify POST (Create), GET (Status), DELETE (Cancel) endpoints.
- **FIM State API**: Verify GET (All/Rack/Round), POST (Update), DELETE (Remove) endpoints.
- **Process Management**: Verify process spawning and non-blocking behavior.
- **Integration**: Verify interaction with legacy scripts/files.

## 3. Test Strategy
- **Mock Testing (Unit)**: 
    - Use `pytest` with `unittest.mock`.
    - Files: `tests/test_mock_api.py`, `tests/test_mock_fim_state.py`.
    - Focus: API logic, Pydantic validation, correct calling of utils.
- **Real Testing (Integration)**: 
    - Use `pytest` with temporary directories.
    - Files: `tests/test_real_assemble_test.py`, `tests/test_real_fim_state.py`.
    - Focus: End-to-end flow, file system I/O, script execution.
    - **Configuration**: Use variables from `.env` (python-dotenv) for API URLs and Keys.

## 4. Test Environment
- **OS**: Windows / Linux
- **Python**: 3.8+
- **Dependencies**: `requirements.txt`

## 5. Automation
- Run all tests via `python -m pytest tests/`.
