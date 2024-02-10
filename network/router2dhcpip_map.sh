#!/bin/bash

sh_router_ids(){
        openstack router list -c ID -f value
}

sh_router_subnetid(){
        local ip_address
        local subnet_id
        local fixed_ip_address=$(openstack port list \
        --device-owner network:router_gateway --router $1 -c "Fixed IP Addresses" -f json 2>/dev/null \
        | jq -Mr '.[]."Fixed IP Addresses"')
        eval ${fixed_ip_address/,/;}
        echo $subnet_id
}

sh_subnet_networkid(){
        openstack subnet show $1 -c "network_id" -f value
}

sh_dhcp_ip(){
        local ip_address
        local subnet_id
        local fixed_ip_address=$(openstack port list \
        --device-owner network:dhcp --network $1 -c "Fixed IP Addresses" -f json 2>/dev/null \
        | jq -Mr '.[0]."Fixed IP Addresses"')
        eval ${fixed_ip_address/,/;}
        echo $ip_address
}

rids=$(sh_router_ids)

for rid in $rids; do
        nid=
        dip="not_connetcted"
        sid=$(sh_router_subnetid $rid)
        [ -n "$sid" -a "$sid" != "null" ] && nid=$(sh_subnet_networkid $sid)
        [ -n "$nid" -a "$nid" != "null" ] && dip=$(sh_dhcp_ip $nid)
        echo "$rid $dip"
done
