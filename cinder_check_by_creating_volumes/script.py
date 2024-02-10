import conf
import cred
import sqlite3
from keystoneauth1 import loading
from keystoneauth1 import session
from cinderclient import client
from subprocess import run


### Database

def db_table(connection, table):
    cu = connection.cursor()

    q = '''
        SELECT name
        FROM sqlite_master
            WHERE type == 'table'
            AND name='{}'
        '''.format(table)
    cu.execute(q)

    return ( len(cu.fetchall()) != 0 )

def db_init(connection):
    cu = connection.cursor()
    q = '''
        CREATE TABLE sessions (
            db_session INTEGER PRIMARY KEY,
            created TEXT,
			sender_exit_code INT
            )
        '''
    db_table(connection, 'sessions') or cu.execute(q)

    q = '''
        CREATE TABLE volumes (
            db_session INTEGER NOT NULL REFERENCES sessions,
            availability_zone TEXT,
            volume_type TEXT,
            volume_id TEXT,
            last_action TEXT
            )
        '''
    db_table(connection, 'volumes') or cu.execute(q)

def db_new_session(connection):
    cu = connection.cursor()

    q = '''
        INSERT INTO sessions (
            created
            ) VALUES (
            datetime('now', 'localtime')
            )
        '''
    cu.execute(q)

    return cu.lastrowid

def db_truncate(connection):
    cu = connection.cursor()
    q = '''
        SELECT db_session
        FROM 'sessions'
            WHERE created < datetime('now', '-{}', 'localtime')
        '''.format(conf.depth)
    cu.execute(q)

    for db_session in cu.fetchall():
        for table in ('sessions', 'volumes'):
            q = '''DELETE FROM '{}' WHERE db_session == {}
                '''.format(table, db_session[0])
            cu.execute(q)

def db_volumes_create(connection, session, volumes):
    cu = connection.cursor()

    q = '''
        INSERT INTO 'volumes'
            VALUES ({}, ?, ?, ?, 'create')
        '''.format(session)
    cu.executemany(q, volumes)

def db_volumes_delete(connection, volumes):
    cu = connection.cursor()
    for volume in volumes:
        volume_id = volume[3]

        q = '''
            UPDATE 'volumes'
                SET last_action = 'delete'
                WHERE volume_id = '{}'
            '''.format(volume_id)
        cu.execute(q)

def db_get_volumes(connection):
    cu = connection.cursor()

    q = '''
        SELECT * FROM 'volumes'
            WHERE last_action = 'create'
    '''
    cu.execute(q)

    return cu.fetchall()

def db_session_update(connection, db_session, sender_exit_code):
    cu = connection.cursor()

    q = '''
        UPDATE 'sessions'
            SET sender_exit_code = {}
            WHERE db_session = '{}'
        '''.format(sender_exit_code, db_session)
    cu.execute(q)

### Cinder

def create_volumes(cinder):
    volumes = []
    for availability_zone in conf.tests:
        for volume_type in conf.tests[availability_zone]:
            os_volume = cinder.volumes.create(
                availability_zone=availability_zone,
                volume_type=volume_type,
                description=conf.volumes['description'],
                size=1,
                name='cinder_monitoring__dbrecord' +
                    '__' + availability_zone + '__'+ volume_type)
            volumes.append((
                availability_zone,
                volume_type,
                os_volume.id
                ))
    return volumes

def check_delete_volumes(cinder, volumes):
    v_success = []
    v_fail = []

    for volume in volumes:
        availability_zone = volume[1]
        volume_type = volume[2]
        volume_id = volume[3]

        try:
            os_volume = cinder.volumes.get(volume_id)

            v = v_success if (os_volume.availability_zone == availability_zone and
               os_volume.volume_type == volume_type and
               os_volume.status == 'available') else v_fail
            v.append(availability_zone + '/' + volume_type)
            os_volume.delete()
        except:
            print('Volume {} not found'.format(volume_id))

    return ', '.join(v_success).upper(), ','.join(v_fail).upper()

def if_volumes_stucked(cinder):
    volumes = cinder.volumes.list()
    count = 0
    for volume in volumes:
        if volume.description == conf.volumes['description']: count += 1 
    return count >= conf.volumes['stucked']

# Zabbix
def sender(value):
    process = run(["zabbix_sender",
                    "-z", conf.zabbix['server'],
                    "-s", conf.zabbix['hostname'],
                    "-k", conf.zabbix['key'],
                    "-o", str(value)])
    return process.returncode

##

def main():
    db_connection = sqlite3.connect(conf.dbfile)

    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=conf.os['auth_url'],
	                                username=cred.os['username'],
	                                password=cred.os['password'],
	                                project_id=conf.os['project_id'],
	                                user_domain_name=conf.os['user_domain_name'])
    api_session = session.Session(auth=auth,verify=False)
    cinder = client.Client(conf.os['identity_api_version'], session=api_session)

    if not if_volumes_stucked(cinder):
        db_init(db_connection)

        volumes_status_create = db_get_volumes(db_connection)
        volume_success, volume_fail  = check_delete_volumes(cinder, volumes_status_create)
        db_volumes_delete(db_connection, volumes_status_create)

        db_session = db_new_session(db_connection)
        new_volumes = create_volumes(cinder)
        db_volumes_create(db_connection, db_session, new_volumes)

        sender_message = '{"success": "' + volume_success + '", "fail": "' + volume_fail + '"}'
        #print(sender_message)
        sender_exit_code = sender(sender_message)
        db_session_update(db_connection, db_session, sender_exit_code)

        db_truncate(db_connection)

        db_connection.commit()
        db_connection.close()
    else:
        print("Check stucked volumes in the script's project")

if __name__ == '__main__':
    main()

# vim: set expandtab
