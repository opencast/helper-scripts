Systemd allows you to define timers that are a powerful alternative to cron jobs. With the scripts provided, all Opencast services will be checked regularly and sanitized if necessary.

Provide all hosts that have to be checked (usually admin and worker nodes) and the corresponding user and password in sanitize_services.sh.
As sanitize_services.sh contains all passwords in plain text, this script should be stored at a secure place which is not accessible for other users (e.g. /root/scripts).

Copy ocsanitizeservice.service and ocsanitizeservice.timer to /usr/lib/systemd/system. Provide the path to the sanitize_services.sh script in ocsanitizeservice.service.
In the timer section of ocsanitizeservice.timer, define the time interval in which the service and sanitize check should be executed.
Example: OnUnitActiveSec=1h for an 1 hour interval, OnUnitActiveSec=30m for an 30 minutes interval etc. (refer to https://www.freedesktop.org/software/systemd/man/systemd.time.html#).

Enable and activate the timer unit with the following commands:
systemctl enable ocsanitizeservice.timer
systemctl start ocsanitizeservice.timer