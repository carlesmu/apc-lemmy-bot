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
