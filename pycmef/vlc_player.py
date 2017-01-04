import os, sys, vlc

class VlcPlayer:
  def __init__(self):
    self.instance = vlc.Instance()
    self.mediaplayer = self.instance.media_player_new()
    self.clip = None

  def play(self, path):
    if self.clip is None or path == self.clip:
        self.media = self.instance.media_new(unicode("file://%s" % path))
        self.mediaplayer.set_media(self.media)
        self.clip = path

    self.mediaplayer.play()
    return not self.mediaplayer.is_playing()

  def stop(self):
    self.mediaplayer.stop()
    return not self.mediaplayer.is_playing()

  def get_volume(self):
    return self.mediaplayer.audio_get_volume()

  def set_volume(self, volume):
    return self.mediaplayer.audio_set_volume(volume)
