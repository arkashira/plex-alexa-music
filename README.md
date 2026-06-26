# Plex Alexa Music

A Python project for handling Alexa music intents and streaming audio from a Plex library.

## Usage

1. Create a `PlexAlexaMusic` instance with a dictionary of playlists.
2. Call the `handle_play_music_intent` method with an intent dictionary containing the playlist name.
3. The method will return a response string indicating whether the playlist was found and played.

## Testing

Run the tests using `pytest` in the `tests` directory.
