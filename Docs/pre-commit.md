# Pre-commit

Pre-commit is very useful tool for identifying simple issues before submission to code review.

You can check the official documentation [here](https://pre-commit.com/).

## Installation
1. Via pip, run:

    `pip install pre-commit`
2. On macOS, run:

    `brew install pre-commit`.

## Using it

On the project root folder run:

    pre-commit install
    pre-commit install-hooks
    pre-commit install --hook-type commit-msg

## Hooks

On the file `.pre-commit-config.yaml` you will find the hooks that the project is currently using, you can add/remove hooks as you want. By default you will be using the following hooks:

  - Conventional commit lint.
  - Code linter using Black.
  - Import sorter using Isort.
  - Trailing white spaces checker.
  - End of file fixer.
