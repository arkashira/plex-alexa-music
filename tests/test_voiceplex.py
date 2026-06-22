from voiceplex import VoicePlex, VoicePlexSkill

def test_add_skill():
    voiceplex = VoicePlex()
    skill = VoicePlexSkill("VoicePlex", "A skill for Plex/Emby server", True)
    voiceplex.add_skill(skill)
    assert voiceplex.get_skill("VoicePlex") == skill

def test_enable_skill():
    voiceplex = VoicePlex()
    skill = VoicePlexSkill("VoicePlex", "A skill for Plex/Emby server", True)
    voiceplex.add_skill(skill)
    result = voiceplex.enable_skill("VoicePlex")
    assert result == {"account_linking": True, "skill_name": "VoicePlex"}

def test_enable_skill_account_linking_disabled():
    voiceplex = VoicePlex()
    skill = VoicePlexSkill("VoicePlex", "A skill for Plex/Emby server", False)
    voiceplex.add_skill(skill)
    result = voiceplex.enable_skill("VoicePlex")
    assert result == {"error": "Account linking not enabled"}

def test_enable_skill_not_found():
    voiceplex = VoicePlex()
    result = voiceplex.enable_skill("NonExistentSkill")
    assert result == {"error": "Skill not found"}

def test_get_skill():
    voiceplex = VoicePlex()
    skill = VoicePlexSkill("VoicePlex", "A skill for Plex/Emby server", True)
    voiceplex.add_skill(skill)
    assert voiceplex.get_skill("VoicePlex") == skill

def test_get_skill_not_found():
    voiceplex = VoicePlex()
    assert voiceplex.get_skill("NonExistentSkill") is None
