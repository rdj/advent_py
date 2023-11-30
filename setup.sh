#!/usr/bin/env bash

ME=$(basename "$0")
MY_DIR=$(dirname "$0")
DAY=$1
YEAR=${2:-$(date "+%Y")}

if [ "${DAY}" == "" ]; then
    echo "usage: ${ME} day [year]" 1>&2
    exit 1
fi

DAY_2D=$(printf '%02d' ${DAY})

PROJECT="${YEAR}-${DAY_2D}"
PROJECT_DIR="${MY_DIR}/${PROJECT}"

mkdir -p "${PROJECT_DIR}"
"${MY_DIR}/aoc-input.sh" "${DAY}" "${YEAR}" > "${PROJECT_DIR}/input.txt"

cp "${MY_DIR}"/template/* "${PROJECT_DIR}"

cd "${PROJECT_DIR}"
emacsclient --no-wait *.py

