
import sys, os

from pycmef.event_handler import returns_dictionary

# cmef.emit('play_audio', { clip: './cmef/Fall.wav' }, function(r) { console.log(r); });

class PyAudioHandler:
  def __init__(self, player):
    self.player = player

  def register(self, event_manager):
    self.file_path = event_manager.directory
    event_manager.register_events({
      'play_audio': self.play_audio,
      'stop_audio': self.stop_audio,
      'get_volume': self.get_volume,
      'set_volume': self.set_volume
    })

  @returns_dictionary
  def play_audio(self, args):
    status = False

    self.clip = args.get('clip', None)

    if self.clip is not None:
      if not os.path.exists(self.clip):
        self.clip = os.path.abspath(os.path.join(self.file_path, self.clip))
      else:
        self.clip = os.path.abspath(self.clip)
      try:
        status = self.player.play(self.clip)
      except IOError as error:
        print error
        status = False

    return { 'status': status, 'clip': self.clip }

  @returns_dictionary
  def stop_audio(self, args):
    return { 'status': self.player.stop(), 'clip': self.clip }

  @returns_dictionary
  def set_volume(self, args):
    return {
             'status': self.player.set_volume(args.get('volume', None)),
             'volume': self.player.get_volume()
           }

  @returns_dictionary
  def get_volume(self, args):
    return { 'volume': self.player.get_volume() }
