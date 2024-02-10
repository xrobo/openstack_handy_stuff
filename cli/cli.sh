clear
OS_PROJECT_ID='2d4a551f-fc1e-4093-8e20-02e3ffa08cec'


lab(){
	#eval v='${!'${project_prefix}'*}'
	#echo "Var: ${v}"
	#echo "Var p_*: ${!p_*}"
	declare -a projects
	projects=(${!p_*})
	eval projects=('${!'${project_prefix}'*}')
	echo "Projects: ${projects[*]}"
	echo "Projects length: ${#projects[*]}"
	i=1
	echo "Project $i: ${!projects[((--i))]}"
}

setp(){
	[ -f $1 ] && source $1 || return

	local project_name
	local project_id
	local menu_index=0
	local project_index=0

	declare -a projects
	eval projects=( '${!'${project_prefix}'*}' )

	echo -e "Project list:"
	echo

	for project_name in ${projects[*]}; do
		project_id=${!project_name}
		project_name=${project_name#$project_prefix}
		((menu_index++))
		if [ "x$project_id" = "x$OS_PROJECT_ID" ]; then
			project_name+=' *'
			project_index=$menu_index
		fi
		echo -e "\t[${menu_index}] ${project_id} ${project_name}"
	done

	echo
	read -p "Select project [$project_index]: " -n 1 project_index
	echo
	case $project_index in
		[1-9])	[ $project_index -le ${#projects[*]} ] && \
				export OS_PROJECT_ID=${!projects[((--project_index))]}
			;;
	esac

	unset ${projects[*]}
	unset project_prefix

}

echo $OS_PROJECT_ID
setp ./projects.rca
echo $OS_PROJECT_ID

# vim: ft=sh
