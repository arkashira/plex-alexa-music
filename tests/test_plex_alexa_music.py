from plex_alexa_music import PlexAlexaMusic, Playlist
import pytest

def test_get_playlist():
    playlists = {
        "jazz": Playlist("jazz", ["track1", "track2"]),
        "rock": Playlist("rock", ["track3", "track4"]),
    }
    music = PlexAlexaMusic(playlists)
    assert music.get_playlist("jazz").name == "jazz"
    assert music.get_playlist("nonexistent") is None

def test_resolve_playlist_to_url():
    playlists = {
        "jazz": Playlist("jazz", ["track1", "track2"]),
    }
    music = PlexAlexaMusic(playlists)
    playlist = music.get_playlist("jazz")
    assert music.resolve_playlist_to_url(playlist).startswith("http://localhost:8080/playlist/")

def test_handle_play_music_intent():
    playlists = {
        "jazz": Playlist("jazz", ["track1", "track2"]),
    }
    music = PlexAlexaMusic(playlists)
    intent = {"playlist_name": "jazz"}
    assert music.handle_play_music_intent(intent).startswith("Playing 'jazz'")

def test_handle_play_music_intent_nonexistent_playlist():
    playlists = {
        "jazz": Playlist("jazz", ["track1", "track2"]),
    }
    music = PlexAlexaMusic(playlists)
    intent = {"playlist_name": "nonexistent"}
    assert music.handle_play_music_intent(intent).startswith("Sorry, I couldn't find a playlist named 'nonexistent'.")

def test_get_audio_stream():
    playlists = {
        "jazz": Playlist("jazz", ["track1", "track2"]),
    }
    music = PlexAlexaMusic(playlists)
    url = "http://localhost:8080/playlist/jazz"
    assert music.get_audio_stream(url).startswith("Streaming audio from http://localhost:8080/playlist/jazz")
