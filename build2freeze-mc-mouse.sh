#!/bin/bash
# date 2019-10-12 11:03:45
# author calllivecn <c-all@qq.com>


TMP="mouse"

safe_exit(){
	echo "clear tmp directory $TMP"
	rm -r "$TMP"
}


mkdir "$TMP"

TMP="$(pwd)/$TMP"

set -e

trap "safe_exit" SIGTERM SIGINT EXIT

cp -rv keyboardmouse/ "$TMP/"
cp -v mouse.py "$TMP/__main__.py"

python3 -m zipapp "$TMP" -c -o mouse.pyz -p "/usr/bin/env python3"

