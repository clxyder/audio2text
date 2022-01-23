import os, subprocess, shutil, sys

from utils import ElapsedTime

from audio2text import get_large_audio_transcription

SUPPORTED_EXTENSIONS = [".mp4", ".m4a"]

if __name__ == "__main__":
    ffmpeg = 'ffmpeg'
    assert shutil.which(ffmpeg) is not None, '''
    This programs needs ffmpeg please download from:
    https://ffmpeg.zeranoe.com/builds/
    After installation be sure to set PATH variables.
    '''

    src = None
    try:
        src = sys.argv[1]
    except Exception as exc:
        pass

    assert src is not None, '''
    Incorrect usage, please try:
        python main.py <path-to-audio>
    '''

    # check if file exists
    assert os.path.exists(src) == True, '''
    Provided file path does not exists, please check path again.
    '''

    # can be either .mp4 or .m4a
    root, ext = os.path.splitext(src)
    assert any([ ext == supported_ext for supported_ext in SUPPORTED_EXTENSIONS ]),'''
    Incorrent, filetype, the file must either mp4 or m4a.
    '''

    audio_src, txt_file = map(lambda _ext : f"{root}.{_ext}", ["wav","txt"])    

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
    dir_to_save = os.path.dirname(src)
    txt_file_path = os.path.join(dir_to_save,txt_file)
    print(f'Writing processed text to file:\n{txt_file_path}')
    with open(txt_file_path,'+w') as f:
        f.write(whole_text)
    print('Processing complete!')