"""Music and sound playback behind two on/off switches."""

from pgzero.builtins import music, sounds

MUSIC_VOLUME = 0.5

SOUND_VOLUMES = {
    "shoot": 0.30,
    "hit": 0.45,
    "hurt": 0.80,
    "enemy_die": 0.55,
    "pickup": 0.70,
    "door": 0.55,
    "select": 0.45,
    "dodge": 0.40,
    "boss_roar": 0.80,
    "win": 0.75,
    "lose": 0.75,
}

DEFAULT_SOUND_VOLUME = 0.5


class AudioManager:
    """Plays the tracks and effects, and remembers what is switched off."""

    def __init__(self, music_on=True, sound_on=True):
        self.music_on = music_on
        self.sound_on = sound_on
        self.current_track = None
        self._playing_track = None

    # ------------------------------------------------------------ music

    def play_music(self, name):
        """Start a track unless it is already playing or music is off."""
        self.current_track = name
        if not self.music_on:
            self.stop_music()
            return
        if self._playing_track == name:
            return
        music.play(name)
        music.set_volume(MUSIC_VOLUME)
        self._playing_track = name

    def stop_music(self):
        if self._playing_track is not None:
            music.stop()
            self._playing_track = None

    def toggle_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            track, self._playing_track = self.current_track, None
            if track is not None:
                self.play_music(track)
        else:
            self.stop_music()
        return self.music_on

    # ------------------------------------------------------------ effects

    def play_sound(self, name):
        if not self.sound_on:
            return
        effect = getattr(sounds, name)
        effect.set_volume(SOUND_VOLUMES.get(name, DEFAULT_SOUND_VOLUME))
        effect.play()

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        return self.sound_on

    # ------------------------------------------------------------ labels

    def music_label(self):
        return "Music: ON" if self.music_on else "Music: OFF"

    def sound_label(self):
        return "Sound: ON" if self.sound_on else "Sound: OFF"
