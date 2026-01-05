---
description: setup dev python venv
---

check if python .venv created or not, if not exist, do following actions:
  - create python virtual environment by venv moudule with name ".venv"
if .venv exist, check if required module installed, by following actions:
  - use .venv\bin\pip3 to install requirements_pytest.txt
