## v0.6.0 (2025-11-02)

### Feat

- **lemmy-title**: stop the title after the first doc+space

### Refactor

- **event.py**: add __hash__ method to Event class

## v0.5.8 (2025-07-09)

### Fix

- **event.py**: correct tag line and link creating the post

## v0.5.7 (2025-07-08)

## v0.5.6 (2025-07-08)

### Fix

- **event.py**: remove spaces from tags and their search link
- **s/rel.sh**: execute the `gh` order when confirmed

### Refactor

- add type parameters for generic type `dict` in annotations

## v0.5.5 (2025-06-11)

### Fix

- **s/rel.sh**: execute the gh cmd when confirmed and find the right files for the release

## v0.5.4 (2025-06-11)

### Perf

- **scripts/clean.py**: remove try-except in loop

## v0.5.3 (2025-06-08)

### Fix

- add missed 'i' in tags loop

## v0.5.2 (2025-06-08)

### Fix

- restore required imports

### Refactor

- refactor code
- upgrade the code with `ruff check --select UP --fix`
- add explicit `check` argument to `subprocess.run`
- use list comprehension
- use lowercase function names
- replace LemmyException with LemmyError
- use required argument for the cli
- use pathlib module instead of os
- use unlink from module pathlib
- simplify code
- remove unnecessary else and elif after return
- use a intermediate variable to raise errorsy
- improve dates usage and add missed commas
- use KeyError instead of Exception
- use isort to sort imports
- improve annotations
- remove unused function and improve annotations
- improve documentation
- short long lines
- use the alias project_copyright instead of copyright
- use annonymous variable to explicit ignore returns values
- don't use function call in default function argument
- use 'from' in raised exceptions
- add explicit stacklevel
- move imports at the start of file
- change 'not foo in boo' to 'foo not in boo'
- remove unneeded f-string
- remove unused imports

## v0.5.1 (2025-06-01)

### Fix

- add # 'to' the linked text in tags

## v0.5.0 (2025-05-31)

### Feat

- add a link to the tags to search in the current instance other posts with this tag

### Fix

- **database**: remove the uniqueness of the slugTitle index of the table events

## v0.4.5 (2025-04-05)

### Fix

- Try 3 times to post a message

## v0.4.4 (2025-01-18)

### Fix

- updated commitizen version_provider: "poetry" -> "pep621"

## v0.4.3 (2025-01-16)

### Fix

- Check that a image have imageSrc informed

### Perf

- **post-timeout**: increased from 3 seconds to 10

## v0.4.2 (2024-04-28)

### Perf

- **Lemmy**: use raise_exceptions=True to create the Lemmy object

## v0.4.0 (2023-08-19)

### Feat

- We can now upload images to lemmy when they are not online
- **callbacks**: The supabase options are not required in all cases

### Fix

- **__init__**: No initialize some of the config vars
- **Image**: Missed f" quoted repr

## v0.3.1 (2023-07-18)

### Feat

- **docs**: create documentation using sphinx
- **local-database**: added a new module and cli option to use a local database to track events
- added a local database config file name

### Fix

- **cli**: added envbar for --database option and improved description
- **dependencies**: added missed dependency in sqlalchemy-utils
- **network**: retry to access remote image when we get a URLError
- **langcode**: corrected wrong type

### Refactor

- **mypy**: more typing compilant
- **mypy**: more typing compilant
- added py.typed hint file

## v0.2.0 (2023-07-03)

### Feat

- Added suport to langcode in the events and storing in lemmy
- **event.py**: Use some markdawn in the description (citation)

### Fix

- **cli**: corrected imports, sorted callbacks and added callback for supabase key

### Refactor

- **conf**: move initial values to conf estruct
- **lemmy.py**: don't use protecter member _requestor.nodeinfo
- **cli**: simplified imports
- **cli**: simplified imports

## v0.1.1 (2023-06-29)

### Fix

- **pyproject.toml**: use tags prefixed with v

## v0.1.0 (2023-06-29)
