from os.path import exists
from json import dumps

ROOT = '/var/log/kolla'
SRVDATA = {
    'barbican': ['api', 'worker'],
    'manila': ['api', 'scheduler'],
    'cinder': ['api', 'volume', 'backup'],
    'trove': ['api', 'conductor'],
    'nova': ['api', 'scheduler', 'conductor', 'compute']
}

def main():
    found = []
    for srv,units in SRVDATA.items():
        for unit in units:
            log = ROOT + '/' + srv + '/' + srv + '-' + unit + '.log'
            if exists(log):
                found.append({
                    '{#SRVNAME}': '-'.join((srv,unit)),
                    '{#SRVCONTAINER}': '_'.join((srv,unit)),
                    '{#SRVLOG}': log})
    print(dumps(found))

if __name__ == '__main__':
    main()
