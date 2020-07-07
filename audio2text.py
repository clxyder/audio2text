import contextlib, time
import os, subprocess, sys, shutil

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

'''
Python Dependencies
- pydub
- speech_recognition

pip3 install pydub SpeechRecognition

Software Dependencies
- ffmpeg: https://ffmpeg.zeranoe.com/builds/ (windows)

Run Command:    python3 ./audio2text.py

Carlos A. Wong
'''

class ElapsedTime(contextlib.ContextDecorator):
    ''' Measures the elapsed time
    '''
    def __init__(self, msg=None, print_on_exit=True):
        self.start = self.now()
        self.stop = None
        self.msg = msg
        self.print_on_exit = print_on_exit

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop = self.now()
        if self.print_on_exit:
            print('Time elapsed for {}: {}'.format(self.msg, self), file=sys.stderr)

    @staticmethod
    def now():
        # return time.clock_gettime(time.CLOCK_MONOTONIC) # linux
        return time.monotonic() # windows

    @property
    def interval(self):
        return (self.stop - self.start) # seconds

    def __str__(self):
        return '{:0.06f} seconds'.format(self.interval)

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    using google speech recognition API, for offline version
    please refer to the source code link.

    source code:
    https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python

    @return:
    - whole_text: string of all processed chunks seperated by a newline
    - percent_success: percent of successful chunks processed
    """
    # Speech recognition processor
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    err_chunks = 0
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
                err_chunks += 1
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += f'{text}\n'
    percent_success = 1- err_chunks/len(chunks)
    # return the text for all chunks detected
    return whole_text, percent_success

if __name__ == "__main__":
    ffmpeg = 'ffmpeg'
    assert shutil.which(ffmpeg) is not None, '''
    This programs needs ffmpeg please download from:
    https://ffmpeg.zeranoe.com/builds/
    After installation be sure to set PATH variables.
    '''

    # can be either .mp4 or .m4a
    src = r"2020-07-02 13.21.29 FM_ Progress Meeting 92403707938\zoom_0.mp4"

    root, ext = os.path.splitext(src)
    audio_src = root+'.wav'
    txt_file = root+'.txt'

    # Need to convert .mp4 or .m4a to .wav format for sr.Recognizer() to work
    if not os.path.isfile(audio_src):
        cmd_line  = [ffmpeg, '-i', src, audio_src] # ffmpeg -i input.mp4 output.wav
        print('Generating .wav from source') 
        subprocess.run(cmd_line)
    else: print('.wav already exists')

    # start transcribing & measures how long it takes
    with ElapsedTime(msg='transcribing'):
        whole_text, percent_success = get_large_audio_transcription(audio_src)
    print(f'Successfully processed {percent_success*100}% of the audio!')

    # Saves the text to a file
    print(f'Writing processed text to file:\n{txt_file}')
    with open(txt_file,'+w') as f: f.write(whole_text)
    print('Processing complete!')