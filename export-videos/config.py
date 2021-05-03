# Configuration

# server settings
admin_url = "http://develop.opencast.org"  # CHANGE ME
# presentation_url =  # defaults to admin url, configure for separate presentation node
digest_user = "opencast_system_account"
digest_pw = "CHANGE_ME"  # CHANGE ME
stream_security = False

# export settings
export_archived = True
export_search = True
export_publications = ["internal"]
export_mimetypes = ["video/mp4"]
export_flavors = []
export_catalogs = ["smil/cutting", "dublincore/*"]

# target directory settings
target_directory = "/home/user/Desktop/videos"  # CHANGE ME
create_series_dirs = False
original_filenames = False
