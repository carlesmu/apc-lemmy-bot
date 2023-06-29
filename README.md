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

### Development dependencies
- [poetry](https://python-poetry.org/):
  [source](https://github.com/python-poetry/poetry)
- [commitizen](https://commitizen-tools.github.io/commitizen/):
  [source code](https://github.com/commitizen-tools/commitizen).
- [black](https://black.readthedocs.io/):
  [source code](https://github.com/psf/black).
- [pylint](https://pylint.org/):
  [source code](https://github.com/pylint-dev/pylint).
- [pre-commit](https://pre-commit.com/):
  [source code](https://github.com/pre-commit/pre-commit).

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
4. Merge the branch in main and, later, delete the development branch.

### Release a new version
It will autogenerate the changelog and create the tag. 
1. You should change the version number to the new version in the
   example code:
   ```
   .venv/Scripts/poetry run cz bump  -cc --major-version-zero 0.1.0
   git add CHANGELOG.md apc_lemmy_bot/__init__.py
   git commit -m "bump: release version 0.1.0"
   ```
3. Create a pull request  and, after it get merged with main,
4. Create the release and tag `v0.1.0`.
