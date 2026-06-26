import json
from dataclasses import dataclass
from typing import Dict, List
import urllib.parse

@dataclass
class Playlist:
    name: str
    tracks: List[str]

class PlexAlexaMusic:
    def __init__(self, playlists: Dict[str, Playlist]):
        self.playlists = playlists

    def get_playlist(self, name: str) -> Playlist:
        return self.playlists.get(name)

    def resolve_playlist_to_url(self, playlist: Playlist) -> str:
        # Simulate resolving a playlist to a valid LAN streaming URL
        # In a real implementation, this would involve querying a Plex server
        return f"http://localhost:8080/playlist/{urllib.parse.quote(playlist.name)}"

    def handle_play_music_intent(self, intent: Dict[str, str]) -> str:
        playlist_name = intent.get("playlist_name")
        if not playlist_name:
            return "Sorry, I didn't understand which playlist you wanted to play."

        playlist = self.get_playlist(playlist_name)
        if not playlist:
            return f"Sorry, I couldn't find a playlist named '{playlist_name}'."

        url = self.resolve_playlist_to_url(playlist)
        return f"Playing '{playlist_name}' from your Plex library. {url}"

    def get_audio_stream(self, url: str) -> str:
        # Simulate getting an audio stream from a URL
        # In a real implementation, this would involve streaming audio from a Plex server
        return f"Streaming audio from {url}"
