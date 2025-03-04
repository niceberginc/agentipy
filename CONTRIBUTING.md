# Contributing to AgentiPy

We welcome contributions to AgentiPy! This document outlines the guidelines for contributing to the project, ensuring a smooth and collaborative process.

## 🚀 Getting Started

1.  **Fork the Repository:** Start by forking the AgentiPy repository on GitHub.
    [<img src="https://img.shields.io/github/forks/niceberginc/agentipy?style=social" alt="GitHub Forks">](https://github.com/niceberginc/agentipy)

2.  **Clone Your Fork:** Clone your forked repository to your local machine.

    ```bash
    git clone https://github.com/<your_username>/agentipy.git
    cd agentipy
    ```

3.  **Set Up a Virtual Environment:** (Recommended) Create and activate a virtual environment to isolate your dependencies.

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows
    ```

4.  **Install Dependencies:** Install the necessary dependencies using `pip`.

    ```bash
    pip install -e .[dev]  # Installs agentipy in editable mode with development dependencies
    ```

    This installs AgentiPy in editable mode, allowing you to make changes to the codebase directly and have them reflected without reinstalling.  The `[dev]` extra installs dependencies for development, such as linters and test runners.

## ✨ Contribution Types

We welcome various types of contributions, including:

*   **Bug Fixes:**  Fixes for reported issues or identified bugs.
*   **New Features:**  Implementation of new functionality and tools.
*   **Documentation Improvements:**  Enhancements to the documentation, including tutorials, examples, and API references.
*   **Protocol Integrations:**  Adding support for new blockchain protocols.
*   **Tests:**  Writing unit tests, integration tests, and end-to-end tests to improve code coverage and reliability.
*   **Examples:**  Creating example scripts and notebooks to showcase the capabilities of AgentiPy.
*   **Code Refactoring:**  Improving the code's structure, readability, and performance.

## 💻 Development Workflow

1.  **Create a Branch:** Create a new branch for your contribution.  Use descriptive branch names, such as `fix-typo-in-readme` or `add-new-jupiter-action`.

    ```bash
    git checkout -b <your_branch_name>
    ```

2.  **Make Changes:** Implement your changes, adhering to the coding style and best practices outlined below.

3.  **Write Tests:**  Ensure your changes are covered by tests.  New features should include corresponding tests to verify their functionality.

4.  **Run Tests:** Run the tests to ensure that your changes don't break existing functionality.

    ```bash
    pytest
    ```

5.  **Linting and Formatting:**  Use `flake8` and `black` to ensure your code adheres to the project's style guidelines.

    ```bash
    flake8 agentipy tests
    black agentipy tests
    ```

6.  **Commit Changes:** Commit your changes with clear and concise commit messages.  Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

    ```bash
    git add .
    git commit -m "feat: Add new Jupiter swap action"
    ```

7.  **Push to Your Fork:** Push your branch to your forked repository on GitHub.

    ```bash
    git push origin <your_branch_name>
    ```

8.  **Create a Pull Request:** Create a pull request (PR) from your branch to the main `main` branch of the AgentiPy repository.  Provide a detailed description of your changes in the PR, including the motivation, implementation details, and any relevant context.

## 📝 Coding Style and Best Practices

*   **Python Style:**  Follow the PEP 8 style guide.
*   **Docstrings:**  Write clear and comprehensive docstrings for all functions, classes, and modules.  Use reStructuredText format for docstrings.
*   **Type Hints:**  Use type hints to improve code readability and maintainability.
*   **Asynchronous Programming:** AgentiPy heavily relies on asynchronous programming.  Ensure you understand and utilize `async` and `await` correctly.
*   **Error Handling:**  Implement robust error handling to gracefully handle potential issues during blockchain interactions.
*   **Security:**  Pay close attention to security considerations, especially when dealing with private keys and sensitive data.  **Never hardcode private keys in your code.**
*   **Testing:** Write comprehensive unit tests and integration tests to ensure the reliability and correctness of your code.
*   **Documentation:** Keep the documentation up-to-date with any changes you make.

## 📜 Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for commit messages. This helps automate release notes and versioning.

A commit message consists of a **type**, an optional **scope**, a **description**, and an optional **body** and **footer**.




**Type:**

*   `feat`: A new feature.
*   `fix`: A bug fix.
*   `docs`: Documentation only changes.
*   `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
*   `refactor`: A code change that neither fixes a bug nor adds a feature.
*   `perf`: A code change that improves performance.
*   `test`: Adding missing tests or correcting existing tests.
*   `build`: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm).
*   `ci`: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs).
*   `chore`: Other changes that don't modify src or test files.
*   `revert`: Reverts a previous commit.

**Scope:**

The scope could be anything specifying place of the commit change. For example `use_raydium`, `trade`, `agent`.

**Description:**

The description contains a succinct description of the change:

*   use the imperative, present tense: "change" not "changed" nor "changes"
*   don't capitalize first letter
*   no dot (.) at the end

**Body:**

Just as in the description, use the imperative, present tense: "change" not "changed" nor "changes"
The body should include the motivation for the change and contrast this with previous behavior.

**Footer:**

The footer should contain any information about Breaking Changes and is also the place to reference GitHub issues that this commit Closes.


## 🛡️ Security Considerations

*   **Never Hardcode Secrets:** Avoid hardcoding private keys, API keys, or other sensitive information in your code. Use environment variables or secure configuration management.
*   **Input Validation:** Validate all user inputs to prevent injection attacks and other security vulnerabilities.
*   **Dependencies:** Keep your dependencies up-to-date to mitigate security risks.

## ❓ Getting Help

If you have any questions or need assistance, please don't hesitate to:

*   Open an issue on GitHub.
*   Contact us on [support@agentipy.com](mailto:support@agentipy.com).
*   Join our community on [Discord](https://discord.com/invite/agentipy).
*   Follow us on [X (Twitter)](https://x.com/AgentiPy).

Thank you for contributing to AgentiPy!