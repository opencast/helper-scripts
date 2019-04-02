from flask import Flask, render_template_string
from lti.tool_consumer import ToolConsumer
app = Flask(__name__)

TPL = '''<!doctype html>
<html>
<title>LTI Test Consumer</title>
<body style="width: 100px; margin: 100px auto;">
<form action="{{ launch_url }}"
      name="ltiLaunchForm"
      id="ltiLaunchForm"
      method="POST"
      encType="application/x-www-form-urlencoded">
  {% for key, value in launch_data.items() %}
    <input type="hidden" name="{{ key }}" value="{{ value }}"/>
  {% endfor %}
  <button type="submit">Launch the tool</button>
</form>
</body>
</html>
'''

@app.route('/')
def consumer(name=None):
    consumer = ToolConsumer(
        consumer_key='CONSUMERKEY',
        consumer_secret='CONSUMERSECRET',
        launch_url='http://localhost:8080/lti',
        params={
            'lti_message_type': 'basic-lti-launch-request',
            'lti_version': 'LTI-1p0',
            'resource_link_id': 37865823,
            'user_id': 'lkiesow',
            'roles': 'Instructor'
        }
    )
    print(consumer.generate_launch_data())
    return render_template_string(TPL,
                                  launch_data=consumer.generate_launch_data(),
                                  launch_url=consumer.launch_url)


if __name__ == '__main__':
    app.run()
