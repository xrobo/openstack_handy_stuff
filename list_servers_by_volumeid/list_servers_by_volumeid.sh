#!/bin/bash

echo_volume_info() {
  VOLUME_ID=$1
  SERVER_ID=
  SERVER_NAME="-"
  PROJECT_ID="[       Failed to detect       ]"

  set_project_id

  if set_server_id; then
    if [ -n "$SERVER_ID" ]; then
      set_server_name
    else
      SERVER_ID="[           NOT ATTACHED           ]"
    fi
  else
    SERVER_ID="[         Failed to detect         ]"
  fi

  echo "${PROJECT_ID} ${VOLUME_ID} ${SERVER_ID} ${SERVER_NAME}"
}

set_server_id() {
  local attachment
  local var
  attachment=$(openstack volume show -c attachments -f value $VOLUME_ID 2>/dev/null) || return 1
  SERVER_ID=$(echo "$attachment" | grep -Eo "server_id': u'[[:alnum:]]{8}(-[[:alnum:]]{4}){3}-[[:alnum:]]{12}" | grep -Eo '[[:alnum:]]{8}(-[[:alnum:]]{4}){3}-[[:alnum:]]{12}' | head -n 1)
}

set_server_name() {
  SERVER_NAME="[ Failed to detect ]"
  local var
  var=$(openstack server show -f value -c name $SERVER_ID 2>/dev/null) && SERVER_NAME=$var
}

set_project_id() {
  local var
  var=$(openstack volume show -f value -c os-vol-tenant-attr:tenant_id $VOLUME_ID 2>/dev/null) && PROJECT_ID=$var
}

echo "ProjectID                        VolumeID                             ServerID                             ServerName"

test -n "$1" && for i in $(cat $1); do echo_volume_info $i; done || echo "No file with volumes supplied"
