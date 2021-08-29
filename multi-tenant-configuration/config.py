# Configuration

# Set this to your admin node
base_url = "http://localhost:8080"

# If you have multiple tenants, use an URL pattern.
# example:
# tenant_url_pattern = "https://{}.example.org"
tenant_url_pattern = "http://{}:8080"

# You can also define a dictionary of tenant URLs, which will be prioritized over the URL pattern:
# example:
# tenant_urls = {
#     'tenant1': 'http://tenant1:8080',
#     'tenant2': 'http://tenant2:8080'
# }

# Digest User login
digest_user = "opencast_system_account"
digest_pw = "CHANGE_ME"

# path to environment configuration file
env_path = "environment/{}/opencast-organizations.yml"
# path to group configuration file
group_path = "configurations/group_configuration.yaml"
