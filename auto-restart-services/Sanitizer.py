import requests
from requests.auth import HTTPDigestAuth
import sys


def main(argv):
    if len(argv) != 3:
        print('wrong number of arguments. 3 expected : url, username, password')
        return
    sanitize(argv[0], argv[1], argv[2])


def sanitize(url, username, password):
    response = requests.get(url+'/services/services.json', auth=HTTPDigestAuth(username, password), headers={'X-Requested-Auth':'Digest'})
    data = response.json()
    for services in data:
        for service in data[services]:
            for state in data[services][service]:
                if state['service_state'] != 'NORMAL':
                    resp = requests.post(url + '/services/sanitize', files={'serviceType': state['type'], 'host': state['host']}, auth=HTTPDigestAuth(username, password), headers={'X-Requested-Auth': 'Digest'})
                    if resp.status_code > 204:
                        print('sth went wrong')


if __name__ == '__main__':
    main(sys.argv[1:])
