import os, sys

class ScriptPlayer:
  def play(self, file):
    audio_script = './audio.sh'

    if os.name != 'posix':
      if os.path.exists('./audio.bat'):
        audio_script = 'audio.bat'
      else:
        print "Unable to find Window audio script."
        return False

    if os.path.exists(audio_script):
      os.system("%s \"%s\" &" % (audio_script, file))
      return True

    return False

  def stop(self):
    return False

  def set_volume(self, volume):
    return False

  def get_volume(self):
    return 100
