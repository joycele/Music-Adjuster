# musicAdjuster.py

import os, glob
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play


class MusicAdjuster:
    def __init__(self, playlist):
        self.playlist = playlist



    def _volumes(self):
        for song in self.playlist:
            s = AudioSegment.from_mp3(song)
            print("song:", os.path.basename(song), "loudness:", s.rms)
            break

os.chdir(r"C:\Users\Joyce\Music")

songs = list(Path(os.getcwd()).rglob('*.mp3'))

for song in songs:
    s = AudioSegment.from_mp3(song)
    print("song:", os.path.basename(song), "loudness:", s.rms)
    break

