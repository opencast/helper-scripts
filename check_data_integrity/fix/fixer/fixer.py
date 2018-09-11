from abc import ABCMeta, abstractmethod


class Fixer:
    """
    Abstract class defining the methods every subclass has to implement for fixing inconsistent data.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def fix(self, opencast_url, digest_login, event_id):
        """
        Fix the given event.

        :param opencast_url: URL to opencast instance
        :type opencast_url: str
        :param digest_login: User and password for digest authentication
        :type digest_login: DigestLogin
        :param event_id: ID of event to be fixed
        :type event_id: str
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_errors():
        """
        Return which errors this fixer can fix.

        :return: A list of errors this fixer can fix
        :rtype: list
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_fix_description():
        """
        Return a description of what this fixer does to fix inconsistent description.

        :return: Description of what this fixer does.
        :rtype: str
        """
        raise NotImplementedError
