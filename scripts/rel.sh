#!/bin/sh
# rel: Release a new version on github
# Needs: gh
#set -ex

LANG=C

usage() {
  cat >&1 <<'eof'
Usage: rel [-h]

Release a new version on github based in the last tag

OPTIONS
  --help,  -h   Show this message.
eof
}

usage_error() {
  cat >&2 <<'eof'
Error. Usage: rel [--help]
eof
  exit 1
}


# Only 0 or 1 argument:
if test $# -gt 1 ; then
  usage_error
fi

while test $# -gt 0; do
  case "$1" in
    "--help" | "-h")
      usage
      exit 0
    ;;
    *) usage_error ;;
  esac
  shift
done

echo ""
echo "notes"
echo "-----"
echo "If you not confirm it. You can copy paste the \`cmd\` to call it"
echo "directy."
echo ""

# tmpfile and tmpfile content ------------------------------------------------
echo -n "- Changelog: "
tmpfile=$(mktemp) || ( echo >2& "Can not create tmpfile." && exit 1 )
echo -n "${tmpfile}"

vtagl="$(scripts/glt.sh -l)" && echo -n " …" || exit 1
vrell="$(scripts/glr.sh -l)" && echo -n " …" || exit 1

txt="**Full Changelog**: https://github.com/carlesmu/apc-lemmy-bot/compare/"
echo "${txt}${vrell}...${vtagl}" > ${tmpfile}
echo "" >> ${tmpfile}

txt="$(.venv/bin/poetry run cz changelog --dry-run $vrell)" && \
  echo -n " …" || exit 1
echo "${txt}" >> ${tmpfile}

echo " Done."

echo "- Upgrading: ${vrell} -> ${vtagl}"
echo ""

# gh release cmd -------------------------------------------------------------
echo "cmd"
echo "---"

vtags="$(scripts/glt.sh -s)" && echo -n " …" || exit 1
vrels="$(scripts/glr.sh -s)" && echo -n " …" || exit 1

txt="gh release create ${vtagl} --target main -F ${tmpfile}"

files="$(find dist -maxdepth 1 -type f -name apc_lemmy_bot-${vtags}*)" && \
  echo -n " …" || exit 1

for file in $files; do
  txt="${txt} \"${file}\""
done

echo " Done."
echo ""
echo "${txt}"
echo ""

# prompt and execute ---------------------------------------------------------
echo -n "Are you sure to execute the cmd? [yN]"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
  eval "${txt}" && echo "Done." || exit 1
fi
