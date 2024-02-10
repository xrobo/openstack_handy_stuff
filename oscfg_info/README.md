Ansible module for retrieving a specified key's value from the settings of OpenStack platform deployed with kolla-ansible and stored in INI files on nodes.

How to use:
```bash
ANSIBLE_LIBRARY=path_to_my_modules ansible-doc oscfg_info
ANSIBLE_LIBRARY=path_to_my_modules ansible -m oscfg_info -a "node_kolla_directory=/opt/openstack/etc/ key=debug service_set=cinder"
```

