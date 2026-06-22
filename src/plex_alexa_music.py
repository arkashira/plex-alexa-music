import json
from dataclasses import dataclass
from typing import List

@dataclass
class Room:
    name: str
    devices: List[str]

@dataclass
class MusicControl:
    rooms: List[Room]

    def control_music(self, room_name: str, action: str):
        room = next((r for r in self.rooms if r.name == room_name), None)
        if room:
            if action == "play":
                return f"Playing music in {room_name}"
            elif action == "pause":
                return f"Pausing music in {room_name}"
            elif action == "stop":
                return f"Stopping music in {room_name}"
            else:
                raise ValueError("Invalid action")
        else:
            raise ValueError("Room not found")

    def add_room(self, room_name: str, devices: List[str]):
        self.rooms.append(Room(room_name, devices))

    def remove_room(self, room_name: str):
        self.rooms = [r for r in self.rooms if r.name != room_name]

    def get_rooms(self):
        return [r.name for r in self.rooms]

    def integrate_plex_emby(self):
        # Simulate Plex/Emby integration
        return "Plex/Emby integration successful"

    def control_music_in_multiple_rooms(self, room_names: List[str], action: str):
        results = []
        for room_name in room_names:
            try:
                result = self.control_music(room_name, action)
                results.append(result)
            except ValueError as e:
                results.append(str(e))
        return results
