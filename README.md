# audio2text

This simple repo transcribes audio files (mp4/m4a) into a text file.
It first splits large audio files into chunks and then applies Google's Speech Rrecognition API on each chunk.

Note: For an offline version please refer to the original source code.

## Installation

`pip install -r requirements.txt`

Software Dependencies

- [ffmpeg (windows)](https://ffmpeg.zeranoe.com/builds/)

## Running the script

`python main.py <path-to-audio>`

## Original Source Code

[Using Speech Recognition to convert speech to text in Python](https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python)
