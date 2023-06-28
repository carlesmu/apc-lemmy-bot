# apc-lemmy-bot
Post supabase database events to a Lemmy instance.

## License
GNU Affero General Public License 3.

## Development

### Main dependencies
- python3
- supabase
- pythorhead 
- typing-extension

### Development dependencies
- poetry
- commitizen 
- black
- pylint
- pre-commit

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
4. Merge the branch in main and, later, delete the development branc.
5. Release new version (it will autogenerate the changelog and create the tag)
   ```
   .venv/bin/poetry run cz bump
   ```
