
import os
import datetime
import json

class ResponseMixin:
  def init_response(self, output):
    self.response = {}
    self.output = output
    self.output_path = None

  def add_core_response(self, args):
    self.response.update(args)
    self.record_response()

  def add_response(self, args):
    if self.current_section is None:
      sec_name = 'invalid'
    else:
      sec_name = self.current_section.name

    if self.current_subsection is None:
      subsec_name = 'invalid'
    else:
      subsec_name = self.current_subsection.name

    sec = self.get_or_create(self.response, sec_name, {})
    sub_sec = self.get_or_create(sec, subsec_name, [])

    sub_sec.append(args)

    self.record_response()

  def get_or_create(self, dic, name, new):
    res = dic.get(name, None)

    if res is None:
      dic[name] = new
      return dic[name]

    return res

  def ensure_path(self):
    if self.output_path is None:
      self.output_path = os.path.join(self.output, self.participant)

      if not os.path.exists(self.output_path):
        os.mkdir(self.output_path)
      elif not os.path.isdir(self.output_path):
        raise Exception('Participant directory is not a directory!')

  def record_response(self):
    self.ensure_path()

    file = "%s_%s.json" % (self.name, datetime.date.today())
    f = open(os.path.join(self.output_path, file), 'w')
    f.write(json.dumps(self.response, indent=2, sort_keys=True))
    f.close()