import argparse
import requests
import sys
from requests.auth import HTTPDigestAuth

SERVER_URL = "https://stable.opencast.org"
DIGEST_USER_NAME = "opencast_system_account"
DIGEST_PASSWORD = "CHANGE_ME"


class OpencastException(BaseException):

    def __init__(self, message):
        self.message = message


def start_workflow(mediaPackageId, workflowId, workflowParams=None):
    """
    This method checks the arguments, Download the media package and call an
    internal method for starting a workflow.

    :param mediaPackageId: the media package identifier
    :param workflowId: the workflow definition identifier
    :param workflowParams: workflow configuration list in the form
                           ["key=value", key2=value2]
    :return: workflow instance as XML serialized string

    :raise ValueError: if the input arguments are not valid
    :raise OpencastException: if the communication to the opencast server fails
                              or an unexpected error occures
    """
    if not mediaPackageId:
        raise ValueError("media package ID isn't set")
    if not workflowId:
        raise ValueError("workflow ID isn't set")

    response = requests.get("{}/assets/episode/{}"
                            .format(SERVER_URL, mediaPackageId),
                            auth=HTTPDigestAuth(DIGEST_USER_NAME,
                                                DIGEST_PASSWORD),
                            headers={"X-Requested-Auth": "Digest"})
    if not response.ok:
        raise OpencastException(
            "Failed to get event media package from server "
            "for {}. HTTP request status code {}: {}"
            .format(mediaPackageId, response.status_code, response.reason))

    mediaPackage = response.text
    if "mediapackage" not in mediaPackage or \
            "id=\"{}\"".format(mediaPackageId) not in mediaPackage:
        raise OpencastException("The media package {} is in a malformed format"
                                .format(mediaPackageId))

    return __start_workflow(mediaPackageId, mediaPackage, workflowId,
                            workflowParams)


def __start_workflow(mediaPackageId, mediaPackage, workflowId,
                     workflowParams=None):
    """
    This internal method start an workflow for the given media package

    :param mediaPackageId: the media package identifier
    :param mediaPackage: the XML serialized string of the media package
    :param workflowId: the workflow definition identifier
    :param workflowParams: workflow configuration list in the form
                           ["key=value", key2=value2]
    :return: workflow instance as XML serialized string
    """
    payload = {'mediapackage': mediaPackage,
               'definition': workflowId}
    if workflowParams:
        payload['properties'] = '\n'.join(workflowParams)
    response = requests.post("{}/workflow/start"
                             .format(SERVER_URL, mediaPackageId),
                             auth=HTTPDigestAuth(DIGEST_USER_NAME,
                                                 DIGEST_PASSWORD),
                             headers={"X-Requested-Auth": "Digest"},
                             data=payload)
    if not response.ok:
        raise OpencastException(
            "Couldn't start a workflow {} on media package {}. "
            "The start workflow REST call was terminated with {}: {}"
            .format(workflowId, mediaPackageId, response.status_code,
                    response.reason))

    print("The workflow {} for the media package {} has been started."
          .format(workflowId, mediaPackageId))
    return response.text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mediapackage", type=str, required=True,
                        help="media package identifier")
    parser.add_argument("-w", "--workflow", type=str, required=True,
                        help="workflow definition identifier")
    parser.add_argument("-W", "--properties", dest='properties',
                        action='append', required=False,
                        help="workflow configuration properties (key=value)")
    parser.add_argument("-o", "--opencast", type=str, required=False,
                        help="url of the opencast instance")
    parser.add_argument("-u", "--user", type=str, required=False,
                        help="digest user name")
    parser.add_argument("-p", "--password", type=str, required=False,
                        help="digest password")

    args = parser.parse_args()
    if args.opencast:
        if not args.opencast.startswith("http"):
            SERVER_URL = "https://{}".format(args.opencast)
        else:
            SERVER_URL = args.opencast

    if args.user:
        DIGEST_USER_NAME = args.user

    if args.password:
        DIGEST_PASSWORD = args.password

    try:
        start_workflow(args.mediapackage, args.workflow, args.properties)
    except OpencastException as e:
        print(e.message, file=sys.stderr)
        exit(1)
