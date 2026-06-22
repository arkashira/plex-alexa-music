import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class VoicePlexSkill:
    name: str
    description: str
    account_linking: bool

class VoicePlex:
    def __init__(self):
        self.skills = {}

    def add_skill(self, skill: VoicePlexSkill):
        self.skills[skill.name] = skill

    def enable_skill(self, skill_name: str) -> Dict:
        if skill_name in self.skills:
            skill = self.skills[skill_name]
            if skill.account_linking:
                return {"account_linking": True, "skill_name": skill_name}
            else:
                return {"error": "Account linking not enabled"}
        else:
            return {"error": "Skill not found"}

    def get_skill(self, skill_name: str) -> VoicePlexSkill:
        return self.skills.get(skill_name)

def main():
    voiceplex = VoicePlex()
    voiceplex.add_skill(VoicePlexSkill("VoicePlex", "A skill for Plex/Emby server", True))
    print(voiceplex.enable_skill("VoicePlex"))

if __name__ == "__main__":
    main()
