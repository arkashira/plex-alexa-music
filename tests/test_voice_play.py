from voice_play import VoicePlay, MusicTrack

def test_add_track():
    voice_play = VoicePlay()
    track = MusicTrack("Happy", "Pharrell Williams")
    voice_play.add_track(track)
    assert voice_play.get_tracks() == ["Happy"]

def test_play_track():
    voice_play = VoicePlay()
    track = MusicTrack("Happy", "Pharrell Williams")
    voice_play.add_track(track)
    assert voice_play.play_track("Happy") == "Now playing: Happy by Pharrell Williams"

def test_play_track_not_found():
    voice_play = VoicePlay()
    assert voice_play.play_track("Unknown") == "Track not found"

def test_get_tracks():
    voice_play = VoicePlay()
    track1 = MusicTrack("Happy", "Pharrell Williams")
    track2 = MusicTrack("Uptown Funk", "Mark Ronson ft. Bruno Mars")
    voice_play.add_track(track1)
    voice_play.add_track(track2)
    assert voice_play.get_tracks() == ["Happy", "Uptown Funk"]
