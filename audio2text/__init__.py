import os

import speech_recognition as sr

from pydub import AudioSegment
from pydub.silence import split_on_silence

def get_large_audio_transcription(path:str):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    using google speech recognition API, for offline version
    please refer to the source code link.

    source code:
    - https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python

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
    basename = os.path.basename(path)
    dir_to_save = os.path.dirname(path)
    folder_name = os.path.join(dir_to_save,f"{basename}-audio-chunks")
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