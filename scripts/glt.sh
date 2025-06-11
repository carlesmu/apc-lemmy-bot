#!/bin/sh
# glr: Get last tag
#set -ex

LANG=C

usage() {
  cat >&1 <<'eof'
Usage: glt -s | -l | -h

Get the last tag of a github project.

OPTIONS
  --short, -s   Get the short version.  (e.g.: 0.4.1)
  --long,  -l   Get the long version.  (e.g.: v0.4.1)
  --help,  -h   Show this message.
eof
}

usage_error() {
  cat >&2 <<'eof'
Error. Usage: glt --short | --long | --help
eof
  exit 1
}


get_version() {
# line 1: get a list (with a header) with last released (non draft and not
#         pre-release) sorted from recent to older.
# line 2: get all the file except the first line (the header).
# line 3: get the first line.
# line 4: print the first word of each line (i.e.: the release version).
  ver="$(git tag -l --sort=-creatordate | \
    head -n 1)"
  if [ "$ver" = "" ]; then
    echo >&2 "[get_version] Version not found."
    exit 1
  fi
  echo -n "$ver"
}

get_short_version() {
  ver="$(echo $(get_version) | sed 's/^v//')"
  if [ "$ver" = "" ]; then
    echo >&2 "[get_short_version] Version not found."
    exit 1
  fi
  echo -n "$ver"
}

get_long_version() {
  ver="$(get_version)"
  if [ "$ver" = "" ]; then
    echo >&2 "[get_long_version] Version not found."
    exit 1
  fi
  echo -n "$ver"
}


# Only 1 argument:
if test $# -eq 0 ; then
  usage_error
fi
if test $# -gt 1 ; then
  usage_error
fi

while test $# -gt 0; do
  case "$1" in
    "--long" | "-l")
      ver="$(get_long_version)"
      echo -n "$ver"
    ;;
    "--short" | "-s")
      ver="$(get_short_version)"
      echo -n "$ver"
    ;;
    "--help" | "-h") usage ;;
    *) usage_error ;;
  esac
  shift
done
