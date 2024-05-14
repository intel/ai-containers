# Contributing

Thank you for considering contributing to Intel® AI Containers! We welcome your help to make this project better.

## Getting Started

Before you start contributing, please take a moment to review the following guidelines.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Please review it to understand the expectations for participant behavior.

### How to Contribute

1. Fork the repository.
2. Create a new branch for your contribution: `git checkout -b feature/your-feature`.
3. Install [pre-commit](https://pre-commit.com/), [Docker](https://docs.docker.com/engine/install/), and [Python 3.8+](https://www.python.org/downloads/).
4. Follow the [Project Setup](README.md#project-setup) steps.
5. Install the third-party python dependencies necessary for pre-commit with `pip install -r test-runner/dev-requirements.txt && pip install -r docs/requirements.txt`.
6. Make your changes, commit, and sign your changes: `git commit -s -m 'Add your feature'`.
7. Push to the branch: `git push origin feature/your-feature`.
8. Submit a pull request.

## Contribution Guidelines

To ensure a smooth and effective contribution process, please follow these guidelines:

### Reporting Issues

- Before creating a new issue, check if it already exists.
- Use a clear and descriptive title for the issue.
- Provide a detailed description of the issue, including steps to reproduce it.

### Making Changes

- Fork the repository and create a new branch for your changes.
- Keep each pull request focused on a single feature or bugfix.
- Write clear and descriptive commit messages.
- Keep code changes concise and well-documented.
- Ensure that your code adheres to the project's coding standards.

### Testing

- Include tests for your changes, if applicable. Utilize the [test-runner](./test-runner/README.md) test framework for creating your tests
- Ensure that all existing tests pass before submitting a pull request.
- Provide information on how to test your changes.
- Utilize automated testing by following the [Pull Request Template](./.github/pull_request_template.md)'s guidelines on how to run your container tests using GitHub Actions.

### Documentation

- If you make changes that affect the project's documentation, update it accordingly.
- Document new features and functionalities.

### Code Style

- Follow the established [code style](https://google.github.io/styleguide/pyguide.html) for this project.
- Consistent and clean code is highly appreciated.

### Pull Requests

- Include a summary of your changes in your pull request.
- Reference the relevant issue(s) if applicable.
- Be responsive to feedback and be ready to make further changes if necessary.

## License

Intel® AI Containers is licensed under the terms in [LICENSE](#license). By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.
