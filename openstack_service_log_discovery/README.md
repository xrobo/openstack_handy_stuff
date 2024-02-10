Checking if there is a log file for OpenStack service and dump result as JSON.

Run example:
```bash
python openstack_service_log_discovery.py
[{"{#SRVNAME}": "cinder-volume", "{#SRVCONTAINER}": "cinder_volume", "{#SRVLOG}": "/var/log/kolla/cinder/cinder-volume.log"}, {"{#SRVNAME}": "cinder-backup", "{#SRVCONTAINER}": "cinder_backup", "{#SRVLOG}": "/var/log/kolla/cinder/cinder-backup.log"}, {"{#SRVNAME}": "nova-compute", "{#SRVCONTAINER}": "nova_compute", "{#SRVLOG}": "/var/log/kolla/nova/nova-compute.log"}]
```
