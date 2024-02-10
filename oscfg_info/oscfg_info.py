#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: oscfg_info

short_description: Getting a 'key = value' pair from INI-file of OpenStack projects' settings

version_added: "1.0.0"

description: Retrieving a specified key's value from the settings of OpenStack platform deployed with kolla-ansible and stored in INI files on nodes.

options:
    section:
        description: INI-file section.
        required: False
        type: str
        default: "DEFAULT"
    key:
        description: The key a value to get from.
        required: True
        type: str
    node_kolla_directory:
        description: Path to projects configuration directories.
        required: False
        type: str
        default: "/etc/kolla"
    service_set:
        description: Services to gather information from. Service here includes project(s), e.g. "cinder" includes "cinder-volume" and "cinder-backup".
        required: False
        type: list
        default: [ "aodh", "barbican", "blazar", "ceilometer", "cinder", "cyborg", "designate", "ec2api", "freezer", "glance", "gnocchi", "heat", "horizon", "ironic", "karbor", "keystone", "kibana", "magnum", "manila", "masakari", "mistral", "murano", "neutron", "nova", "panko", "placement", "sahara", "searchlight", "senlin", "solum", "swift", "trove", "vitrage", "zaqar", "zun" ]

author:
    - Timur Ustinov (https://github.com/xrobo/)
'''

EXAMPLES = r'''
- name: Get 'nova' projects settings
  oscfg_info:
    service_set: nova
'''

RETURN = r'''
changed:
    description: Always 'False' since the module's operation mode is 'read only'.
    type: bool
    returned: always
    sample: False
services:
    description: The dictionary containing services and their projects.
    type: dict
    returned: always
    sample: {
        "ceilometer": {
            "ceilometer-compute": {
                "debug": false
            }
        },
        "cinder": {
            "cinder-backup": {
                "debug": false
            },
            "cinder-backup-nova": {
                "debug": false
            }
        }
    }
'''

from ansible.module_utils.basic import AnsibleModule
from pathlib import Path
from configparser import ConfigParser

def run_module():

	module = AnsibleModule(
        argument_spec=dict(
			node_kolla_directory=dict(default='/etc/kolla', required=False, type='str'),
			section=dict(default='DEFAULT', required=False, type='str'),
			key=dict(required=True, type='str'),
			service_set=dict(default=["all"], required=False, type='list', elements='str'),
		),
		supports_check_mode = True
	)

	result = dict(
		changed = False,
		services = {}
	)

	if module.check_mode:
		module.exit_json(**result)

	if module.params['service_set'] == ["all"]:
		service_set = [
			'aodh',
			'barbican',
			'blazar',
			'ceilometer',
			'cinder',
			'cyborg',
			'designate',
			'ec2api',
			'freezer',
			'glance',
			'gnocchi',
			'heat',
			'horizon',
			'ironic',
			'karbor',
			'keystone',
			'kibana',
			'magnum',
			'manila',
			'masakari',
			'mistral',
			'murano',
			'neutron',
			'nova',
			'panko',
			'placement',
			'sahara',
			'searchlight',
			'senlin',
			'solum',
			'swift',
			'trove',
			'vitrage',
			'zaqar',
			'zun',
		]
	else:
		service_set = module.params['service_set']


	def get_services(node_kolla_directory, section, key):
		result = {} 
		for project_config_directory in node_kolla_directory.iterdir():
			if project_config_directory.is_dir():
				project = project_config_directory.name
				for project_config in project_config_directory.glob('*.conf'):
					service = project_config.stem
					if service in service_set:
						if service not in result: result[service] = {}
						result[service][project] = {key: get_ini_value(project_config, section, key)}
		return result
    
	def get_ini_value(inifile, section, key):
		config = ConfigParser()
		config.read(inifile)
		if section in config and key in config[section]:
				return config[section].get(key)
		else:
			return None

	key = module.params['key']
	section = module.params['section']
	node_kolla_directory = module.params['node_kolla_directory']
	result['services'] = get_services(Path(node_kolla_directory), section, key)

	module.exit_json(**result)

def main():
	run_module()

if __name__ == '__main__':
	main()

# vim: ts=4 noexpandtab
