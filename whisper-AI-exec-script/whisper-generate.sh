#! /usr/bin/sh

#Generate Whisper AI Rest API container
#
# The Quadro P4000 only has 8GB of VRAM, unfortunately it can't run all models at the same time
# The VRAM requiremens for each model are:
# tiny: ~1GB
# base  ~1 GB
# small ~2 GB
# medium ~5 GB
# large ~10 GB 
#
# Uncomment or comment the next lines depending what containers you want to generate
#
# 
# 

#docker run -d --name Whisper_tiny --gpus all -p 9000:9000 -e ASR_MODEL=tiny onerahmet/openai-whisper-asr-webservice-gpu
docker run -d --name Whisper_base --gpus all -p 9001:9000 -e ASR_MODEL=base onerahmet/openai-whisper-asr-webservice-gpu
#docker run -d --name Whisper_small --gpus all -p 9002:9000 -e ASR_MODEL=small onerahmet/openai-whisper-asr-webservice-gpu
docker run -d --name Whisper_medium --gpus all -p 9003:9000 -e ASR_MODEL=medium onerahmet/openai-whisper-asr-webservice-gpu
#docker run -d --name Whisper_large --gpus all -p 9004:9000 -e ASR_MODEL=large onerahmet/openai-whisper-asr-webservice-gpu
