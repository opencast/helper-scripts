# MODIFIED 4. Jun 2020: some more information output added 
# MODIFIED 5. Jun 2020: url added to output, as all hosts (admin, worker nodes) has to be considered  

import requests
from requests.auth import HTTPDigestAuth
import sys


def main(argv):
    if len(argv) != 3:
        print('wrong number of arguments. 3 expected : url, username, password')
        return
    sanitize(argv[0], argv[1], argv[2])


def sanitize(url, username, password):
    failedServices = 0
    responseStatus = 1   # set to 0 if something goes wrong
    response = requests.get(url+'/services/services.json', auth=HTTPDigestAuth(username, password), headers={'X-Requested-Auth':'Digest'})
    data = response.json()
    for services in data:
        for service in data[services]:
            for state in data[services][service]:
                if state['service_state'] != 'NORMAL':
                    failedServices = failedServices + 1
                    resp = requests.post(url + '/services/sanitize', files={'serviceType': state['type'], 'host': state['host']}, auth=HTTPDigestAuth(username, password), headers={'X-Requested-Auth': 'Digest'})
                    if resp.status_code > 204:
                        print('something went wrong on node '+url)
                        responseStatus = 0
                    else:
                        print('service on node '+ url +' sanitized')
    if (failedServices > 0 and responseStatus == 1):
        print('one or more Opencast service(s) on node '+ url +'has/have been sanitized')
    elif (failedServices > 0 and responseStatus == 0):
        print('Attention: one or more Opencast service(s) on node '+ url +'is/are in fail state, but could not be sanitized!')
    else:
        print('all Opencast services on node '+ url +' are OK - nothing to do')

if __name__ == '__main__':
    main(sys.argv[1:])
