[![License: GPLv3+](https://img.shields.io/badge/License-AGPLv3+-blue.svg)](https://www.gu.org/licenses/agpl-3.0)
[![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fcarlesmu%2Fapc-lemmy-bot%2Fmain%2Fpyproject.toml)](#)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)

[![GitHub Release](https://img.shields.io/github/v/release/carlesmu/apc-lemmy-bot)](https://github.com/carlesmu/apc-lemmy-bot/releases/latest)
[![GitHub Release Date](https://img.shields.io/github/release-date/carlesmu/apc-lemmy-bot)](#)
[![GitHub commits since latest release](https://img.shields.io/github/commits-since/carlesmu/apc-lemmy-bot/latest)](#)

# apc-lemmy-bot
Post supabase database events to a Lemmy instance.

## License
GNU Affero General Public License 3.

## Development

### Main dependencies
- [python3](https://www.python.org):
  [source code](https://github.com/python/).
- [supabase](https://supabase.com/docs/reference/python/introduction):
  [source code](https://github.com/supabase-community/supabase-py).
- pythorhead:
  [source code](https://github.com/db0/pythorhead).
- [typing-extension](https://typing-extensions.readthedocs.io/):
  [source code](https://github.com/python/typing_extensions).
- [sqlalchemy](https://www.sqlalchemy.org/):
  [source code](https://github.com/sqlalchemy/sqlalchemy).
- sqlalchemy-utils:
  [source code](https://github.com/kvesteri/sqlalchemy-utils)


### Development dependencies
- [commitizen](https://commitizen-tools.github.io/commitizen/):
  [source code](https://github.com/commitizen-tools/commitizen).
- [mypy](https://www.mypy-lang.org/):
  [source code](https://github.com/python/mypy).
- [poetry](https://python-poetry.org/):
  [source code](https://github.com/python-poetry/poetry)
- [pre-commit](https://pre-commit.com/):
  [source code](https://github.com/pre-commit/pre-commit).
- [pydocstyle](http://www.pydocstyle.org/):
  [source code](https://github.com/PyCQA/pydocstyle).
- [pylint](https://pylint.org/):
  [source code](https://github.com/pylint-dev/pylint).
- [ruff](https://docs.astral.sh/ruff/)
  [source code](https://github.com/astral-sh/ruff)
- taskipy:
  [source code](https://github.com/taskipy/taskipy).


### Initial clone
Note: depending of the OS, you should use or a `Script` or a `bin` directory.
1. Clone the rep as stated
2. Create a virtual environment environment and install poetry in it with pip:
   ```
   cd apc-lemmy-bot
   python -m venv .venv
   .venv/bin/pip install poetry
   ```

3. We will use that `venv` for development and update the dependencies and
   the build system:
   ```
   .venv/bin/poetry install --no-root
   ```
4. We have definied in our pyproject 3 groups:
   - The main dependencies, needed to run `apc-lemmy-bot`, and installed in
     step 3.
   - The dev dependencies, useful utilities to build and mantain the package,
     and installed in step 3.
   - an optional IDE dependencies for `spyder`. SOme times they are not
    autoupload with poetry, ig you are stuck with this problem, you can use:
    `.venv/bin/pip install spyder`
5. Install the precommit hooks:
   ```
   .venv/bin/poetry run pre-commit install
   .venv/bin/poetry run pre-commit install-hooks
   ```

### Development cycle
1. Create a new branch for the development:
   ```
   git branch dev
   git switch dev
   ```
2. Optimize/modify/test chanches.
3. Add changes and commit them
   ```
   git add [files]
   .venv/bin/poetry run cz commit
   ```
4. If you want to add this change to the changelog, generate it:
   ```
   .venv/bin/poetry run cz changelog
   ```
5. Merge the branch in main and, later, delete the development branch (see
   points 2 and 3 of the next section).

### Release a new version
It will generate the changelog and create the tag.
1. Test this order and modify options ( remember to remove `--dry-run`
   when it's ok):
   ```
   .venv/bin/poetry run cz bump -cc --dry-run
   ```
2. Create a pull request and get it merged with main.
   You can use the *CLI* to do it, if you are working in the branch
   `dev`, you can do:
   ```
   git switch main
   git merge dev
   git push
   ```
3. Build the distribution:
   ```
   .venv/bin/poetry run task build
   ```
   **Note:** Use `build-all` to build also the html pages.
4. Create the release and tag it. The order will add the dist files and the
   changelog to the gitlab distribution:
   ```
   .venv/bin/poetry run task release
   ```
