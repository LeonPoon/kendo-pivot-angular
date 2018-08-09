#!/bin/bash


PREFIX="$(dirname "$0")"
if [ -z "$PREFIX" ]; then
	PREFIX="$(dirname "$(which "$0")")"
fi
if [ -z "$PREFIX" ]; then echo no prefix >&2 && exit 1; fi
PREFIX="$(cd "$PREFIX" && pwd)"
if [ -z "$PREFIX" ]; then echo cannot get prefix >&2 && exit 1; fi

set | egrep ^PREFIX=

virtualenv -p $(which python3) "$PREFIX"

"$PREFIX/bin/pip3" install Flask pylint flask_cors
