# OpenStack configuration
# (credentials are kept in a separate file for the sake of security)
os = {
    'user_domain_name': "users",
    'project_id': "adcb5812d18e4ef8910099d310fc45a1",
    'auth_url': "http://openstack-api.xrobo.lab:35357/v3",
    'identity_api_version': 3
    }

# Volumes will be created with the specified description
# Do not create new volumes if there are a 'stucked' number of them
volumes = {
    'description': 'Created by a script for Cinder check.',
    'stucked': 6
    }

# Test scopes
# { 'availability_zone': [ 'volume_type' ] }
tests = {
    'az-one': [ 'ssd', 'hdd' ],
    'another-zone': [ 'ceph', '3par' ]
    }

zabbix = {
    'server': 'zabbix.xrobo.lab',
    'hostname': 'Zabbix server',
    'key': 'xrobo.cinder.volumescreating'
    }

# SQLite3 database file. Need to collect statistics
dbfile = '/opt/script/statistics.db'

# How long to keep the snapshots
# Examples: '6 hours', '14 days', '1 month'
depth = '1 day'

# vim: expandtab
