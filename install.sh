#!/usr/bin/env bash

set -e

which python3 1>/dev/null 2>&1
if [ $? -ne 0 ];then
	echo "Currently TDDISH only works with python3"
	exit 1
fi

import_path=`python3 -c "import sys;print(sys.path[-1] + '/tddish')"`
cli_path="/usr/local/bin/"

# copy the tddish.py as module
mkdir $import_path
if [ $? -ne 0 ];then
	echo "Unable to copy files to "$import_path\
			 ". Try running the script as sudo e.g. > sudo ./install.sh"
	exit 1
fi
import_path=$import_path"/"

cp ./tddish.py __init__.py $import_path
if [ $? -ne 0 ];then
	echo "Unable to copy files to "$import_path\
			 ". Try running the script as sudo e.g. > sudo ./install.sh"
	exit 1
fi
echo "Files copied to "$import_path":"
echo "__init__.py"
echo "tddish.py"

# copy tddish as cli app to the cli_path
cp ./tddish.py ./tddish
chmod 777 ./tddish
cp ./tddish $cli_path
if [ $? -ne 0 ];then
	echo "Unable to copy files to "$cli_path\
	   	 ". Try running the script as sudo e.g. > sudo ./install.sh"
	exit 1
fi
echo "Files copied to "$cli_path":"
echo "tddish"
rm ./tddish
echo "Installation done!."

