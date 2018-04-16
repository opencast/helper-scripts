from script.ingest import createMediapackage, addAttachment, addCatalog, addTrack, ingest
from script.get_mediapackage_elements import get_mediapackage_elements

def recover_mp(mp, base_url, digest_login, workflow_id):
    """
    Recover a mediapackage by first creating a new mediapackage, then adding tracks, catalogs and attachments to it and
    finally ingesting it.

    :param mp: The mediapackage to be recovered.
    :type mp: MediaPackage
    :param base_url: The base url for the rest requests.
    :type base_url: str
    :param digest_login: User and password for digest authentication.
    :type digest_login: DigestLogin
    :param workflow_id: The workflow to be run on ingest.
    :type workflow_id: str
    :raise MediaPackageError:
    """


    new_mp = createMediapackage(base_url, digest_login)

    tracks, catalogs, attachments = get_mediapackage_elements(mp)

    for track in tracks:

        new_mp = addTrack(base_url, digest_login, new_mp, track)

    for attachment in attachments:

        new_mp = addAttachment(base_url, digest_login, new_mp, attachment)

    for catalog in catalogs:

        new_mp = addCatalog(base_url, digest_login, new_mp, catalog)

    workflow = ingest(base_url, digest_login, new_mp, workflow_id)
    return workflow

