# Design Specification

## 1. System Overview
DIAGBE is a backend service for the AI Diagnosis System, managing the fiber cable assembly test process. It acts as an interface between the Cable Assembly Assist System (VI_BE), Shop Floor System (SFC), and legacy diagnosis scripts (DIAG_SW).

## 2. Participants
*   **DIAG_BE**: The backend service (FastAPI).
*   **VI_BE**: Frontend service (Cable Assembly Assist System).
*   **SFC**: Shop Floor System.
*   **DIAG_SW**: Legacy diagnosis scripts.
*   **ADMIN**: System administrator.
*   **OPERATOR**: Assembly operator.

## 3. Operations
*   **Operation 1 (Assemble Test)**: VI_BE requests test creation. DIAG_BE creates a test ID, forks a process to run the test script, and returns immediately.
*   **Operation 2 (Check Status)**: VI_BE polls DIAG_BE for test status (pending, in_progress, completed, error).
*   **Operation 3 (Push Result)**: DIAG_SW pushes results to SFC.
*   **Operation 4 (Admin Ops)**: ADMIN cancels/stops tests or clears old results.
*   **FIM State Management**: Manage FIM state data by Rack SN and Test Round ID (Get/Update/Delete).

## 4. Data Flow
*   VI_BE -> DIAG_BE: Create Test, Get Status.
*   DIAG_BE -> DIAG_SW: Fork Process (Mock/Real).
*   DIAG_SW -> Filesystem: Write status/result.
*   DIAG_BE -> Filesystem: Read status/result.
*   DIAG_BE -> Filesystem: Read/Write FIM State (JSON).
