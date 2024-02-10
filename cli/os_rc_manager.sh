#!/bin/bash

RO_FILE="./template.rc"
source $RO_FILE

TMP_FILE="/tmp/$$"

get_vars() {
	for i in ${!OS_*}; do
		echo "${i}=${!i}"
	done
}

show_vars() {
	echo "Here's your vars:"
	echo
	get_vars
	echo
}

edit_vars() {
	get_vars > $TMP_FILE
	vim $TMP_FILE
	clear_vars
	for i in $(cat $TMP_FILE); do export $i; done
}

clear_vars() {
	unset ${!OS_*}
}

CHOICE=9
show_menu() {
	PS3="Make your choice: "
	clear
	show_vars
	echo
	echo "Menu:"
	select CHOICE in "Reload vars" "Edit vars" "Exit"; do
		case $CHOICE in
	    "Reload vars")
				clear
				show_vars
				;;
	    "Edit vars")
				edit_vars
				;;
	    "Exit")
				break
				;;
		esac
	done
}

#until [ "$CHOICE" = "0" ]; do show_menu; done
#clear
#show_vars
#sleep 2
#edit_vars
#show_vars
show_menu

test -f $TMP_FILE && rm -f $TMP_FILE
# vim: ts=2
