# Migrate Published Recordings to Another Opencast

This script lets you quickly migrate your published series and recordings from one to another Opencast.
It will not migrate any asset manager content.

For the migration, please ensure that static files are served without authentication and without job context evaluation.
The easiest way of doing this is to add a rule like this to you reverse proxy configuration
(this example is for Nginx):

```py
location ^~ /static/ {
	alias /srv/opencast/opencast-dist-allinone/data/opencast/downloads/;
	sendfile           on;
}
```

Next, install a suitable import workflow in your target Opencast.
You can use any workflow you want and even reprocess videos,
but if you just want to import and publish media as they were in the old system,
you may want to use the workflow [import.yaml](import.yaml).

Update the credentials and the workflow in the `migrate.py` to configure your Opencast source and target systems. If you have a distributed installation of Opencast ensure that the URLs match your admin and presentation node. With an AllInOne installation you'll have the same URL for admin and presentation. You can configure with `ONLY_SMALL_VIDEO_TRACKS` whether only the smallest video with a low resolution should be migrated.

Finally, start the migration:

```
❯ python migrate.py
Importing ID-wiki-commons
Create series response: 201
…
Importing e85fcb07-6943-4d09-b739-60daa756d769
Ingest response: 200
…
```
