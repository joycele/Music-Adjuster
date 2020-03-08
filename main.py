# main.py

import os
from pathlib import Path
from musicAdjuster import MusicAdjuster


if __name__ == '__main__':
    os.chdir(r"C:\Users\Joyce\Music\queue")
    songs = list(Path(os.getcwd()).rglob('*.mp3'))
    if len(songs) > 0:
        adjuster = MusicAdjuster(songs)
        #adjuster.show_playlist(volumes=False)
        specific_track = 0  # set variable according tracks shown in show_playlist
        #adjuster.normalize_single_file_volume(specific_track)
        adjuster.normalize_playlist_volume(-13.0)  # normal dBFS measures for music are between -10.0 and -15.0
        #adjuster.play(specific_track)
        #adjuster.splice_and_dice(specific_track)
    else:
        print("Playlist is empty")


