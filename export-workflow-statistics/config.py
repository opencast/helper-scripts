# Configuration

#Set this to your global admin node
url = "https://stable.opencast.org"
#If you have multiple tenants use something like
#url_pattern = "https://{}.example.org"
#otherwise, url_pattern should be the same as the url variable above
url_pattern = "https://stable.opencast.org"

digest_user = "opencast_system_account"
digest_pw = "CHANGE_ME"

workflow_definitions = ["import", "fast"]

exclude_tenants = []

start_date = "2020-01-06"
end_date = "2020-11-29"
week_offset = 1

export_dir = "."
