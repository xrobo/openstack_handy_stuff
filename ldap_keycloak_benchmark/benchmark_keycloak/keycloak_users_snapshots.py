import cred
import conf
import requests

def get_token():
    url = ''.join((
        conf.SCHEME, '://',
        conf.SOCKET, '/auth/realms/',
        conf.REALM, '/protocol/openid-connect/token'
        ))

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'cache-control': 'no-cache'
        }

    data = {
        'grant_type': 'password',
        'client_id': 'admin-cli',
        'username': cred.USERNAME,
        'password': cred.PASSWORD,
        }
    
    req = requests.post(
        url,
        headers = headers,
        data = data
        )
    
    if req.status_code == requests.codes.ok:
        return req.json()['access_token']
    else:
        req.raise_for_status()

def get_users(token):
    url = ''.join((
        conf.SCHEME, '://',
        conf.SOCKET, '/auth/admin/realms/',
        conf.REALM, '/users'
        ))

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token,
        }

    params = {
        'max': conf.LIMIT,
        'first': 0,
        'briefRepresentation': True,
        }

    session = requests.Session()
    session.headers.update(headers)

    users = []
    req_len = conf.LIMIT
    timecount = 0

    while req_len >= conf.LIMIT:
        req = session.get(
            url,
            params = params
            )

        if req.status_code == requests.codes.ok:

            req_len = len(req.json())

            if req_len != 0:
                users.extend(req.json())
                print(f'+{req.elapsed.total_seconds()}\t+{req_len} items')
                timecount += req.elapsed.total_seconds()

            params['first'] += params['max']

        else:
            req.raise_for_status()

    return users, timecount

def main():
    token = get_token()
    users, time = get_users(token)
    print('--')
    print(f'{time}\t{len(users)} items')

if __name__ == '__main__':
    main()
