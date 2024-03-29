#!/usr/bin/env bash

whisperServer=${1}
videoFile=${2}
eventId=${3}
outputVTT=${4}
translate=${5:-0}

# detach audio from video for a faster transfer
ffmpeg -y -nostdin -nostats -i "$videoFile" -vn -acodec copy "/tmp/$eventId.aac"

if [[ "$translate" == "translate" ]]
then
    echo "Translating into english"
    curl --max-time 7200 --location --request POST "$whisperServer/asr?task=translate&output=vtt" \
    --form 'audio_file=@"/tmp/'"$eventId"'.aac"' -o "$outputVTT"
else
    # Send audio for transcription
    echo "Transcribing audio"
    curl --max-time 7200 --location --request POST "$whisperServer/asr?task=transcribe&output=vtt" \
    --form 'audio_file=@"/tmp/'"$eventId"'.aac"' -o "$outputVTT"
fi

rm -f "/tmp/$eventId.aac"
