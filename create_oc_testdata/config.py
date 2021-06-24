# Configuration

# target url for the Opencast system
# "https://tenant1.opencast.com"
target_url = "http://localhost:8080"

# path to a test video
test_video_path = '/home/malte/IdeaProjects/helper-scripts/create_oc_testdata/video_test.mp4'

# default value for the number of events to be created
number_of_events = 2

# digest login
digest_user = "opencast_system_account"
digest_pw = "CHANGE_ME"

# workflow config
workflow_id = "reimport-workflow"
workflow_config = {"autopublish": "false"}
