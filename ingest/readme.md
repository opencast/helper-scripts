Ingest Scripts
==============

ingest-single-request.sh
------------------------

Repeatedly ingest files using a single request ingest. Parameters can be
adjusted at the top of the file. If the video file does not exist, the user is
asked to enter a file name.

ingest-addtrack.sh
------------------

Ingest files using multiple requests, ingesting metadata, audio and video files
separately. Parameters can be adjusted at the top of the file.

ingest-with-smil.sh
-------------------

A small extension to the ingest-addtrack script. SMIL cutting information is
ingested along with the video track, allowing workflows to immediately trim
videos if the editor step is included. The end result is similar to a
publication subject to the user's editing preference.
