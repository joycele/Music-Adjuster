# main.py

import os, glob
from pathlib import Path
from musicAdjuster import MusicAdjuster


if __name__ == '__main__':
    os.chdir(r"C:\Users\Joyce\Music\mdzs")
    songs = list(Path(os.getcwd()).rglob('*.mp3'))
    adjuster = MusicAdjuster(songs)
    adjuster.loudness_volumes()
    #adjuster.experiment()


