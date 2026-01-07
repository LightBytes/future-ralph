# Agent & Developer Guide

This document outlines the standards and workflows for contributing to **Future-Ralph**. All human and AI agents are expected to adhere to these guidelines to ensure code quality, maintainability, and history readability.

## 1. Code Quality & Standards

### Docstrings
*   Use **NumPy-style** docstrings for all functions, classes, and modules.
*   Ensure every public method and class has a docstring explaining its purpose, parameters, and return values.

**Example:**
```python
def calculate_velocity(distance, time):
    """
    Calculate velocity based on distance and time.

    Parameters
    ----------
    distance : float
        The distance traveled in meters.
    time : float
        The time taken in seconds.

    Returns
    -------
    float
        The velocity in meters per second.
    """
    return distance / time
```

### Static Analysis
*   We use **Ruff** for linting and formatting.
*   We use **MyPy** for static type checking.
*   Ensure strictly typed code (no implicit `Any` where possible).

## 2. Commit Convention

We follow the **Conventional Commits** specification.

### Format
```
<type>(<scope>): <short summary>

<detailed description>

<footer (optional)>
```

### Types
*   `feat`: A new feature
*   `fix`: A bug fix
*   `docs`: Documentation only changes
*   `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
*   `refactor`: A code change that neither fixes a bug nor adds a feature
*   `perf`: A code change that improves performance
*   `test`: Adding missing tests or correcting existing tests
*   `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

### Detailed Description
*   Always include a body paragraph after the short summary if the change is non-trivial.
*   Explain **why** the change was made, not just **what** changed.
*   Reference issues using `Ref: #123` or `Closes: #123`.

**Example:**
```
feat(engine): implement async future execution

Introduced the --detach flag to the CLI and refactored the execution logic
to run in a background process. This allows users to continue working while
Future-Ralph explores futures.

- Added subprocess.Popen spawning in main.py
- Created internal-run hidden command
- Updated RunManager to handle detached state

Closes: #42
```

## 3. Pull Request Workflow

1.  **Local Verification**: Before pushing or updating a PR, ensure all tests pass locally.
    ```bash
    pytest
    ```
2.  **Pre-commit Hooks**: We use `pre-commit` to ensure code quality matches our CI pipeline.
    *   Install: `pip install pre-commit`
    *   Setup: `pre-commit install`
    *   Run manually: `pre-commit run --all-files`

3.  **PR Description**: Copy the commit message format. Provide context on the changes and any specific areas needing review.

## 4. Environment Setup

To match the CI environment:
```bash
pip install -e .[dev]
```
