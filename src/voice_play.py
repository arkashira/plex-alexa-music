import json
from dataclasses import dataclass
from typing import List

@dataclass
class MusicTrack:
    title: str
    artist: str

class VoicePlay:
    def __init__(self):
        self.music_library = []

    def add_track(self, track: MusicTrack):
        self.music_library.append(track)

    def play_track(self, title: str):
        for track in self.music_library:
            if track.title == title:
                return f"Now playing: {track.title} by {track.artist}"
        return "Track not found"

    def get_tracks(self):
        return [track.title for track in self.music_library]
