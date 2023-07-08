#!/bin/bash


# sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
# sudo apt-get install ffmpeg libav-tools


# install virtualenv
virtualenv -p python3 env

PWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
PYTHONPATH=$PWD 

# activate environment
source "env/bin/activate"
# install dependencies
pip3 install -r requirements.txt
# deactivate environmen
deactivate
