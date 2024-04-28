## Unreleased

### Perf

- **Lemmy**: use raise_exceptions=True to create the Lemmy object

## v0.4.1 (2024-03-05)

## v0.4.0 (2023-08-19)

### Feat

- We can now upload images to lemmy when they are not online
- **callbacks**: The supabase options are not required in all cases

### Fix

- **__init__**: No initialize some of the config vars
- **Image**: Missed f" quoted repr

## v0.3.1 (2023-07-18)

### Fix

- **cli**: added envbar for --database option and improved description
- **dependencies**: added missed dependency in sqlalchemy-utils
- **network**: retry to access remote image when we get a URLError

## v0.3.0 (2023-07-16)

### Feat

- **docs**: create documentation using sphinx
- **local-database**: added a new module and cli option to use a local database to track events
- added a local database config file name

### Fix

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

## v0.1.1 (2023-06-30)

### Fix

- **pyproject.toml**: use tags prefixed with v

## v0.1.0 (2023-06-29)
