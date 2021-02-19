# Configuration

#Set this to your global admin node
url = "http://tenant1:8080"
#If you have multiple tenants use something like
#url_pattern = "https://{}.example.org"
#otherwise, url_pattern should be the same as the url variable above
url_pattern = "http://{}:8080"

# digest user
digest_user = "opencast_system_account"
digest_pw = "CHANGE_ME"

# path to environment configuration file
env_path = "environment/staging/opencast-organizations.yml"

# workflow_definitions = ["import", "fast"]
# exclude_tenants = []
# export_dir = "."