Fake HLS Streaming
======================

This script uses ffmpeg (use the Opencast release, or something very recent), and nginx's docker image to create a fake
HLS streaming source.  This can be used to test that your live-streaming workflow and player work as expected.

This script requires minor configuration of Opencast's `LiveScheduleServiceImpl.cfg`:
 - `live.streamingUrl=http://localhost:8888/`
 - `live.streamName=master.m3u8`

Your workflow also needs to have `publishLive` set to true for the live streaming event to be properly listed in the
search index.  Stream should be playable via VLC, ffplay, or other video players from http://localhost:8888/master.m3u8.
You may need to wait a minute or two after starting the stream before it is properly playable.

Usage:

    bash fake-hls.sh
