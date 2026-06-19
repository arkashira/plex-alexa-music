import pytest
from plex_alexa_music import MusicControl, Room

def test_play_music():
    rooms = [Room("Living Room", ["Device 1"]), Room("Kitchen", ["Device 2"])]
    music_control = MusicControl(rooms)
    result = music_control.play_music(["Living Room"])
    assert result == ["Living Room"]

def test_play_music_multiple_rooms():
    rooms = [Room("Living Room", ["Device 1"]), Room("Kitchen", ["Device 2"])]
    music_control = MusicControl(rooms)
    result = music_control.play_music(["Living Room", "Kitchen"])
    assert result == ["Living Room", "Kitchen"]

def test_play_music_no_rooms():
    rooms = [Room("Living Room", ["Device 1"]), Room("Kitchen", ["Device 2"])]
    music_control = MusicControl(rooms)
    with pytest.raises(ValueError):
        music_control.play_music(["Bedroom"])

def test_stop_music():
    rooms = [Room("Living Room", ["Device 1"]), Room("Kitchen", ["Device 2"])]
    music_control = MusicControl(rooms)
    result = music_control.stop_music(["Living Room"])
    assert result == ["Living Room"]

def test_stop_music_multiple_rooms():
    rooms = [Room("Living Room", ["Device 1"]), Room("Kitchen", ["Device 2"])]
    music_control = MusicControl(rooms)
    result = music_control.stop_music(["Living Room", "Kitchen"])
    assert result == ["Living Room", "Kitchen"]

def test_stop_music_no_rooms():
    rooms = [Room("Living Room", ["Device 1"]), Room("Kitchen", ["Device 2"])]
    music_control = MusicControl(rooms)
    with pytest.raises(ValueError):
        music_control.stop_music(["Bedroom"])
