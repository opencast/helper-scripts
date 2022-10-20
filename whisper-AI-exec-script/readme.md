# Whisper AI Transcription for Opencast

This folder contains a shell script and a Task workflow to implement Whisper-AI to Opencast as an
external code execution.


## How to use it

While there is a lot of ways to implement Whisper, on this script I implemented as a REST-API server,
with this type of implementation, any worker can use the power of a single GPU, making scaling and configuration easier.

## How to implement it

1. Run the  docker container [whisper-asr-webservice](https://github.com/ahmetoner/whisper-asr-webservice) in a machine with network access to the other workers (Not necessary if the same machine is a Opencast worker), you can use `whisper-generate.sh` as a starting point.
2. Copy the script file [`whisper-getvtt.sh`](whisper-getvtt.sh) into the **scripts folder in opencast** (normally `/etc/opencast/scripts`)
3. Allow `whisper-getvtt.sh` to be run on `org.opencastproject.execute.impl.ExecuteServiceImpl.cfg` configuration file.
4. Copy the `action-transcribe-event.xml` to the opencast `workflows` folder.
5. **Important** Configure the workflow file to your settings and parameters
## Notes

### About the docker container

- The container can be run on CPU mode or GPU mode. GPU is way faster. For example, with the base model the CPU for a 2 hours video takes more than hour, with GPU (Quadro P4000) takes 5 minutes to transcribe.
- Each model reserves a part of the video RAM to work. depending on your GPU could it be possible that you can't run all language models at the same time or can't run at all (for example, the large model **needs more than 10 GB to work!**).
- If you need to look the available REST endpoints, you can go to `{{ your_server }}:{{ port }}/docs`
- More information you can find on the [container's GitHub page](https://github.com/ahmetoner/whisper-asr-webservice)

### About the execution script

The script is very simple, gets the audio from the video, sends the audio to the whisper server and gets the VTT subtitles.

`$ ./whisper-getvtt.sh {whisperServer} {videoFile} {eventId} {outputVttFile} translate*`

Where:
- `whisperServer`: The address where the server is running (EX: `localhost:900`)
- `videoFile`: Video file to transcribe or translate
- `eventId`: Event ID from Opencast
- `outputVttFile`: VTT subtitles file
- `translate`: \* Optional, if is written, it will translate the transcription to english.

Finally, try the script manually to be sure that can reach the whisper server.

### About the Workflow

The workflow is a template, you need to configure first to your setup before to use it. Some things to take into account.

- On the `configuration_panel` field, you can enable or disable models that you will not use. simply add `document.getElementById("ID").disabled = true;` in the script part, for example:

    ```html
    <script>
        document.getElementById("mTiny").disabled = true;
        document.getElementById("mSmall").disabled = true;
        document.getElementById("mLarge").disabled = true;


    </script>
    ```
- Set the correct server in the `conditional-config` WoH for each model
- In the execution WoHs, take note of the captions tag, the normal transcription is set to tag in german `vtt+de`, change the last two letter to your corresponding language before.



## Credits

- OpenAI for Whisper
- ahmetoner, for the creation of the Whisper docker image with REST API endpoints 
- This script brought to you by the University of Cologne RRZK, author: Maximiliano Lira Del Canto.