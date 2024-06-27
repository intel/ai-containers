# Contributing

Thank you for considering contributing to Intel® AI Containers! We welcome your help to make this project better.

## Getting Started

Before you start contributing, submit a request to be added to the [Intel](https://github.com/intel) Organization on GitHub by contacting one of the [`mlops-maintain`](https://github.com/orgs/intel/teams/mlops-maintain) members.

Once assigned to the [`mlops-write`](https://github.com/orgs/intel/teams/mlops-write) or [`mlops-maintain`](https://github.com/orgs/intel/teams/mlops-maintain) team depending on the scope of your contributions, you will be able to create branches and submit pull requests.

Once you are added to the organization, you will be given acces to ai-containers' Azure Container Registry (ACR).

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Please review it to understand the expectations for participant behavior.

### How to Contribute

1. Create a new branch for your contribution: `git checkout -b username/your-feature`.
2. Install [pre-commit](https://pre-commit.com/), [Docker](https://docs.docker.com/engine/install/), and [Python 3.8+](https://www.python.org/downloads/).
   1. `pre-commit install`
   2. `sudo usermod -aG docker $USER`
   3. `sudo apt-get install -y python3-venv`
3. Follow the [Project Setup](README.md#project-setup) steps.
4. Install the third-party python dependencies necessary for pre-commit depending on the type of contribution you are making:
   1. Always install the documentation hook requirements: `pip install -r docs/requirements.txt`.
   2. If you are contributing to Test Runner, run `pip install -r test-runner/dev-requirements.txt`.
   3. If you are contributing to helm charts, run `pip install -r workflows/charts/dev-requirements.txt`. Install [Helm](https://helm.sh/docs/intro/install/) and then the [Chart Testing](https://github.com/helm/chart-testing) tool.
5. Make your changes, commit, and [sign](#sign-your-work) your changes: `git commit -s -m 'Add your feature'`.
6. Push to the branch: `git push origin username/your-feature`.
7. Submit a pull request.

### Code Review

All submissions, including submissions by project members, require review. We use GitHub pull requests for this purpose. Consult the [GitHub Help](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) for more information on using pull requests.

In order to complete the review process, the following steps are required:

1. All status checks pass.
2. All third-party dependencies are approved by the maintainers and no new vulnerabilities are introduced to the codebase.
3. At least one approval from a [codeowner](https://github.com/intel/ai-containers/blob/main/.github/CODEOWNERS) that maintains the area of the code you are changing.

Depending on the size and complexity of the change, additional reviews may be required and it may be subject to additional requirements, for example, if you are submitting a contribution to [Test Runner](https://github.com/intel/ai-containers/tree/main/test-runner) you may be required to write unit tests that satisfy our coverage requirements.

### Merge Queue

Once your pull request has been approved, it will be added to the merge queue. The merge queue is a list of pull requests that are ready to be merged. The merge queue runs additional CI over your code to make sure no regressions were introduced into other areas of the codebase.

If your pull request passes the merge queue, it will be merged into the main branch. Otherwise, it will be removed from the merge queue, and you will need to address the issues that caused the failure.

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

### Sign your work

Please use the sign-off line at the end of the patch. Your signature certifies that you wrote the patch or otherwise have the right to pass it on as an open source patch. The rules are pretty simple: if you can certify
the below (from [developercertificate.org](http://developercertificate.org/)):

```text
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
660 York Street, Suite 102,
San Francisco, CA 94110 USA

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

Then you just add a line to every git commit message:

```text
Signed-off-by: Joe Smith <joe.smith@email.com>
```

Use your real name (sorry, no pseudonyms or anonymous contributions.)

If you set your `user.name` and `user.email` git configs, you can sign your
commit automatically with `git commit -s`.

## License

Intel® AI Containers is licensed under the terms in [LICENSE](./LICENSE). By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.
