
import sys, os

from pycmef.event_handler import returns_dictionary

# import pyaudio
# import wave

# cmef.emit('play_audio', { clip: './cmef/Fall.wav' }, function(r) { console.log(r); });

class PyAudioHandler:
  def __init__(self):
    self.streams = []
    # self.audio = pyaudio.PyAudio()

  def play_file(self, file):
    #define stream chunk
    # chunk = 1024

    file = os.path.join(self.file_path, file)

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

    # #open a wav format music
    # f = wave.open(file, "rb")

    # #open stream
    # stream = self.audio.open(
    #                 format = self.audio.get_format_from_width(
    #                   f.getsampwidth()
    #                 ),
    #                 channels = f.getnchannels(),
    #                 rate = f.getframerate(),
    #                 output = True)

    # #read data
    # data = f.readframes(chunk)

    # #paly stream
    # while data != '':
    #     stream.write(data)
    #     data = f.readframes(chunk)

    # idx = len(self.streams)
    # self.streams.append(stream)

    # return idx

  def register(self, event_manager):
    self.file_path = event_manager.directory
    event_manager.register_events({
      'play_audio': self.play_audio,
      'stop_audio': self.stop_audio
    })

  @returns_dictionary
  def play_audio(self, args):
    result = {}

    clip = args.get('clip', None)

    if clip is not None:
      try:
        result['playing'] = self.play_file(clip)
      except IOError as error:
        print error
        result['play_failed'] = clip

    return result

  @returns_dictionary
  def stop_audio(self, args):
    return { stop_failed: args.get('stop', None) }
    # result = {}
    # handle = args.get('stop', None)

    # if handle is not None:
    #   try:
    #     self.streams[handle].stop_stream()
    #     result['stopped'] = handle
    #   except IndexError:
    #     result['stop_failed'] = handle

    # return result
