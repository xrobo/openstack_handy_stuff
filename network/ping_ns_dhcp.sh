#!/bin/bash

# "router_id-dhcp_ip-file" file example:
#
# 041cb758-8b29-43e8-80f4-0d42417ab483 10.0.0.3
# 99666142-18b4-4a44-be74-b3575481dc93 10.0.2.6
# fa6bf2b4-7034-44de-9441-0dff0fac7020 10.0.1.9
#

usage(){
    echo "Usage: $0 router_id-dhcp_ip-file"
}

coloring(){
    echo "\\033[${1}m${2}\\033[0m"
}

set_pairs(){
    declare -Ag PAIRS
    while read router_id dhcp_ip; do
        PAIRS[${router_id}]=${dhcp_ip}
    done < $1
}

set_result(){
    declare -Ag RESULT
    for router_id in ${!PAIRS[*]}; do
        dhcp_ip=${PAIRS[$router_id]}
        RESULT[${router_id}]="ping_fail"
        ns_name=qrouter-$router_id
        if [ -f "/run/netns/$ns_name" ]; then
            ip netns exec $ns_name \
                ping -4 -n -W 1 -c 1 \
                ${dhcp_ip} 2>&1 1>/dev/null \
            && RESULT[${router_id}]="ping_okay"
        else
            RESULT[${router_id}]="not_found"
        fi
    done
}

sh_result(){
    for router_id in ${!RESULT[*]}; do
        case ${RESULT[$router_id]} in
            ping_okay)
                echo -e "$router_id ${PAIRS[$router_id]} $(coloring ${ping_okay[color]} ${ping_okay[label]})"
                ;;
            ping_fail)
                echo -e "$router_id ${PAIRS[$router_id]} $(coloring ${ping_fail[color]} ${ping_fail[label]})"
                ;;
            not_found)
                echo -e $(coloring ${not_found[color]} "$router_id ${PAIRS[$router_id]} ${not_found[label]}")
                ;;
        esac
    done
}

declare -A ping_okay=([color]='00;92' [label]=PONG)
declare -A ping_fail=([color]='00;31' [label]=LOSS)
declare -A not_found=([color]='00;02' [label]=SKIP) # Network Name Space not found on this system

main(){
    set_pairs $1
    set_result
    sh_result
}

[ -n "$1" -a -f "$1" ] && main $1 || { usage; exit 1; }

# vim: relativenumber ts=4 expandtab
