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

    def play_music(self, room_names: List[str]):
        """Play music in specified rooms"""
        playing_rooms = [room for room in self.rooms if room.name in room_names]
        if not playing_rooms:
            raise ValueError("No rooms found with the given names")
        return [room.name for room in playing_rooms]

    def stop_music(self, room_names: List[str]):
        """Stop music in specified rooms"""
        stopping_rooms = [room for room in self.rooms if room.name in room_names]
        if not stopping_rooms:
            raise ValueError("No rooms found with the given names")
        return [room.name for room in stopping_rooms]
