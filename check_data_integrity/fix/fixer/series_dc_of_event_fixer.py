from fix.fixer.fixer import Fixer
from fix.io.results_parser import FixableError
from fix.workflows.workflow import get_workflow_definition
from rest_requests.assetmanager_requests import get_media_package
from rest_requests.workflow_requests import start_workflow


class SeriesDCOfEventFixer(Fixer):
    """
    This module can fix events that are missing their series Dublin Core catalog or that have a series Dublin Core
    catalog that isn't up to date by starting a workflow.
    """

    def __init__(self):
        """
        Constructor to load the workflow definition
        """

        self.workflow_definition = get_workflow_definition("add_or_update_series_dc.xml")

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

        media_package = get_media_package(opencast_url, digest_login, event_id)
        start_workflow(opencast_url, digest_login, self.workflow_definition, media_package)

    @staticmethod
    def get_errors():
        """
        Return which errors this fixer can fix.

        :return: A list of errors this fixer can fix
        :rtype: list
        """
        return [FixableError.EVENTS_MISSING_SERIES_DC, FixableError.EVENTS_NONEQUAL_SERIES_DC]

    @staticmethod
    def get_fix_description():
        """
        Return a description of what this fixer does to fix inconsistent data.

        :return: Description of what this fixer does.
        :rtype: str
        """
        return "(re)setting series Dublin Core catalog of event from series service"
