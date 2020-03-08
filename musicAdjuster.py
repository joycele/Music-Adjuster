# musicAdjuster.py

import os
from pydub import AudioSegment, effects
from pydub.playback import play
from pydub.utils import mediainfo


class MusicAdjuster:
    def __init__(self, playlist):
        self.playlist = {}
        for i, track in enumerate(playlist):
            self.playlist[i] = track
        print("refer to track keys:", self.playlist)

    def show_playlist(self, volumes=False):
        for track in self.playlist:
            if volumes:
                s = AudioSegment.from_mp3(self.playlist[track])
                print("track", track, ", song:", os.path.basename(self.playlist[track]), "loudness:", s.max_dBFS)
            else:
                print("track", track, ", song:", os.path.basename(self.playlist[track]))

    def play(self, track):
        s = AudioSegment.from_mp3(self.playlist[track])
        play(s)

    def extract_segment(self, track: int, beginning=None, end=None) -> AudioSegment:
        '''
        return a splice of AudioSegment s starting at beginning and ending at end (in seconds)

        sample usages : ASSUME 30 SECONDS OF AUDIO LENGTH
          - to extract first ten seconds of audio: extract_segment(s, end=10) OR extract_segment(s, end=-20)
          - to extract last ten seconds of audio: extract_segment(s, beginning=20) OR extract_segment(s, beginning=-10)
          - to extract a middle chunk, ie. from 00:10 - 00:20 of audio: extract_segment(s, beginning=10, end=20)
                    -  DO NOT USE NEGATIVES FOR EXTRACTING MIDDLE
        '''
        s = AudioSegment.from_mp3(self.playlist[track])
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


    def remove_segment(self, track: int, beginning=None, end=None) -> AudioSegment:
        '''
        return AudioSegment s with a splice removed starting at beginning and ending at end (in seconds)
        for usage: see extract_segment docstring
           - beginning == None --> remove starting chunk
           - end == None --> removing ending chunk
        '''
        s = AudioSegment.from_mp3(self.playlist[track])
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

    def splice_and_dice(self, track):
        # do audio trimming and splicing here
        s = AudioSegment.from_mp3(self.playlist[track])
        s = self.remove_segment(track, beginning=-8) # remove from end
        #s = self.remove_segment(track, end=3) # remove from beginning
        #s = self.extract_segment(track, end=270)
        #s = self.extract_segment(track, beginning=3, end=-20)
        print("start play")
        play(s[:10000]) # play first 10 seconds of track
        play(s[-10000:]) # play last 10 seconds of track
        print(s.duration_seconds)
        print(s.rms)
        #play(s)
        #s.export(str(self.playlist[track]), format="mp3", tags=mediainfo(str(self.playlist[track])).get('TAG', {}))

    def normalize_playlist_volume(self, target_dBFS):
        # adjust amplitude to the same level across all tracks in playlist
        for track in self.playlist:
            s = AudioSegment.from_mp3(self.playlist[track])
            change_in_volume = target_dBFS - s.dBFS
            normalized_track = s.apply_gain(change_in_volume)
            print(self.playlist[track], "new volume:", normalized_track.dBFS)
            normalized_track.export(str(self.playlist[track]), format="mp3", tags=mediainfo(str(self.playlist[track])).get('TAG', {}))

    def normalize_single_file_volume(self, track):
        # adjust and normalize audio within a single mp3 file
        s = AudioSegment.from_mp3(self.playlist[track])
        normalized_s = effects.normalize(s)
        normalized_s.export(str(self.playlist[track]), format="mp3", tags=mediainfo(str(self.playlist[track])).get('TAG', {}))


