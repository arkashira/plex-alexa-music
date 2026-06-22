from plex_alexa_music import MusicControl, Room

def test_control_music():
    music_control = MusicControl([])
    music_control.add_room("Living Room", ["Device 1", "Device 2"])
    assert music_control.control_music("Living Room", "play") == "Playing music in Living Room"
    assert music_control.control_music("Living Room", "pause") == "Pausing music in Living Room"
    assert music_control.control_music("Living Room", "stop") == "Stopping music in Living Room"

def test_control_music_invalid_action():
    music_control = MusicControl([])
    music_control.add_room("Living Room", ["Device 1", "Device 2"])
    try:
        music_control.control_music("Living Room", "invalid_action")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Invalid action"

def test_control_music_room_not_found():
    music_control = MusicControl([])
    try:
        music_control.control_music("Non-existent Room", "play")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Room not found"

def test_integrate_plex_emby():
    music_control = MusicControl([])
    assert music_control.integrate_plex_emby() == "Plex/Emby integration successful"

def test_control_music_in_multiple_rooms():
    music_control = MusicControl([])
    music_control.add_room("Living Room", ["Device 1", "Device 2"])
    music_control.add_room("Bedroom", ["Device 3", "Device 4"])
    results = music_control.control_music_in_multiple_rooms(["Living Room", "Bedroom"], "play")
    assert results == ["Playing music in Living Room", "Playing music in Bedroom"]

def test_control_music_in_multiple_rooms_invalid_room():
    music_control = MusicControl([])
    music_control.add_room("Living Room", ["Device 1", "Device 2"])
    results = music_control.control_music_in_multiple_rooms(["Living Room", "Non-existent Room"], "play")
    assert results == ["Playing music in Living Room", "Room not found"]
