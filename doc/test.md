# Testing with Pytest

This project uses `pytest` for writing and running tests.

## How to Write Tests

1.  **Create Test Files:** Create Python files in the `tests/` directory. It's a good practice to name your test files starting with `test_` (e.g., `test_my_module.py`).
2.  **Define Test Functions:** Inside your test files, define functions that start with `test_`. These functions will contain your test logic.
3.  **Use Assertions:** Use the `assert` statement to check if a condition is true. If an `assert` statement fails, the test will fail.

**Example:**

```python
# tests/test_example.py

def test_addition():
    # This test checks if 1 + 1 equals 2
    assert 1 + 1 == 2

def test_string_concatenation():
    # This test checks string concatenation
    assert "hello" + " " + "world" == "hello world"

def test_list_length():
    # This test checks the length of a list
    my_list = [1, 2, 3]
    assert len(my_list) == 3
```

## How to Run Tests

To run all tests in the project, navigate to the project's root directory in your terminal and execute the following command:

```bash
uv run pytest
```

`pytest` will automatically discover all test files (files named `test_*.py` or `*_test.py`) and test functions (functions named `test_*`) and execute them.

### Running Specific Tests

You can also run specific tests:

*   **Run tests in a specific file:**
    ```bash
    uv run pytest tests/test_my_module.py
    ```
*   **Run a specific test function:**
    ```bash
    uv run pytest tests/test_my_module.py::test_specific_function
    ```
*   **Run tests matching a keyword expression:**
    ```bash
    uv run pytest -k "addition or concatenation"
    ```

## Test Reporting

After running tests, `pytest` will provide a summary of the test results, indicating how many tests passed, failed, were skipped, etc.
