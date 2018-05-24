import getpass
from collections import namedtuple

DigestLogin = namedtuple('DigestLogin', ['user', 'password'])


def read_digest_password():
    """
    Read in digest password until it isn't empty.
    :return:
    """

    digest_pw = getpass.getpass('No password provided, enter digest password:')
    while not digest_pw:
        digest_pw = getpass.getpass('Password cannot be empty, please try again:')
    return digest_pw
