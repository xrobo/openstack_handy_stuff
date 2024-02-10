#!/bin/bash

set_array(){
    local array_prefix=$1
    local output
    set -- $2
    local i=1
    while [ "$#" -gt 0 ]; do
        xecho -n '.'
        eval ${array_prefix}_id[$i]=$1
        eval ${array_prefix}_name[$i]=$2
        if [[ $array_prefix == stack ]]; then
            output=$(openstack stack show -f value $1 2>/dev/null | grep cluster_uuid | cut -d'"' -f 4)
            eval stack_cluster[$i]=$output
        fi
        (( i++ ))
        shift 2
    done
    xecho
}

sh_results(){
    local at_least_one_lb
    for i in $(seq 1 ${#lb_id[*]}); do
        if [[ -n "${lb_kube[$i]}" ]]; then
            if [[ "${lb_kube[$i]}" == '[ abandoned ]' ]]; then
                mark='x'
                # at_least_one_lb=1
                : ${at_least_one_lb:=1}
            else
                mark=' '
            fi
        else
            mark='-'
            lb_kube[$i]='[ not a kube-loadbalancer ]'
        fi
            xecho "    [$mark] ${lb_name[$i]}"
            xecho "          id:   ${lb_id[$i]}"
            xecho "          kube: ${lb_kube[$i]}"
        xecho
    done
    return $at_least_one_lb
}

update_array_lb(){
    for i in $(seq 1 ${#lb_id[*]}); do
        lb_kube[$i]="[ abandoned ]"
        for j in $(seq 1 ${#stack_id[*]}); do
            if [[ "${lb_name[$i]}" == "kube_service_"* ]]; then
                if [[ "${lb_name[$i]}" == "kube_service_${stack_cluster[$j]}_"* ]]; then
                    lb_kube[$i]="${stack_name[$j]}"
                    break
                fi
            else
                lb_kube[$i]=
                break
            fi
        done
    done
}

rm_lb(){
    xecho
    [[ -n "$SILENT" ]] && REPLY=y || read -p "Delete abandoned loadbalancers? [y/N]: "
    case $REPLY in
        [Yy]*) for i in $(seq 1 ${#lb_id[*]}); do
                   [[ "${lb_kube[$i]}" == '[ abandoned ]' ]] \
                   && openstack loadbalancer delete --cascade ${lb_id[$i]} 2>/dev/null \
                   || continue
               done ;;
    esac
}

xecho(){
    [[ -n "$SILENT" ]] || echo "$@"
}

main(){
    xecho -n "Gathering loadbalancer info"
    output=$(openstack loadbalancer list -f value -c id -c name 2>/dev/null) || return 1
    [[ -n $output ]] && set_array lb "$output" || { xecho -e "\nNo loadbalancer are found"; return 0; }
    
    xecho -n "Gathering kubernetes info"
    output=$(openstack stack list -f value -c ID -c "Stack Name" 2>/dev/null) || return 1
    set_array stack "$output"
    
    update_array_lb
    sh_results || rm_lb
}

SILENT=${1:+1}
main $silent || exit 1

# vim: ts=4
