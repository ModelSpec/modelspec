Here are the steps to create the virtual environment and run the tests:
from root directory (modelspec) run the following:
1. python3 -m venv .venv (this creates the virtual environment)
2. source .venv/bin/activate (activate the venv)
3. python -m pip install --upgrade pip
4. pip install -r requirements-dev.txt (includes the pytest dependency)
now cd into tools/middleware/test and run the following to test the happy path test file
5. python -m pytest -q --pyargs test_happy_path 