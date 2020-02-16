# musicAdjuster.py

import os, glob
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play


class MusicAdjuster:
    def __init__(self, playlist):
        self.playlist = {}
        for i in range(len(playlist)):
            self.playlist[i] = playlist[i]
        print("refer to track keys:", self.playlist)

    def loudness_volumes(self):
        for track in self.playlist:
            s = AudioSegment.from_mp3(self.playlist[track])
            print("track", track, ", song:", os.path.basename(self.playlist[track]), "loudness:", s.rms)

    def extract_segment(self, s: AudioSegment, beginning=None, end=None) -> AudioSegment:
        '''
        return a splice of AudioSegment s starting at beginning and ending at end (in seconds)

        sample usages : ASSUME 30 SECONDS OF AUDIO LENGTH
          - to extract first ten seconds of audio: extract_segment(s, end=10) OR extract_segment(s, end=-20)
          - to extract last ten seconds of audio: extract_segment(s, beginning=20) OR extract_segment(s, beginning=-10)
          - to extract a middle chunk, ie. from 00:10 - 00:20 of audio: extract_segment(s, beginning=10, end=20)
                    -  DO NOT USE NEGATIVES FOR EXTRACTING MIDDLE
        '''
        if not beginning and not end:
            return s
        if beginning and end:
            start_e = beginning * 1000
            end_e = end * 1000
            return s[start_e:end_e]
        elif beginning and not end:
            # extract end chunk
            start_e = beginning * 1000
            return s[start_e:]
        elif end and not beginning:
            # extract starting chunk
            end_e = end * 1000
            return s[:end_e]


    def remove_segment(self, s: AudioSegment, beginning=None, end=None) -> AudioSegment:
        '''
        return AudioSegment s with a splice removed starting at beginning and ending at end (in seconds)
        for usage: see extract_segment docstring
           - DO NOT USE NEGATIVES FOR REMOVING MIDDLE
        '''
        if not beginning and not end:
            return s
        if beginning and end:
            # remove middle chunk
            start_r = beginning * 1000
            end_r = end * 1000
            beginning_chunk = s[:start_r]
            ending_chunk = s[end_r:]
            return beginning_chunk + ending_chunk
        elif beginning and not end:
            # remove end chunk
            start_r = beginning * 1000
            return s[:start_r]
        elif end and not beginning:
            # remove starting chunk
            end_r = end * 1000
            return s[end_r:]


    def experiment(self):
        #s = AudioSegment.from_mp3(self.playlist[track])
        s = AudioSegment.from_mp3(self.playlist[37])
        print(s.rms)
        play(s)
        #louder_s = s - 12
        #print(louder_s.rms)
        #play(louder_s)

    def modify_song(self):
        s = AudioSegment.from_mp3(self.playlist[44])
