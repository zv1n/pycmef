
import datetime, json

class ResponseMixin:
  def init_response(self):
    self.response = {}

  def add_core_response(self, args):
    self.response.update(args)
    self.record_response()

  def add_response(self, args):
    sec_name = self.current_section.name
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

  def record_response(self):
    file = "%s_%s_%s.json" % (self.name, self.participant, datetime.date.today())
    f = open(file, 'w')
    f.write(json.dumps(self.response, indent=2, sort_keys=True))
    f.close()