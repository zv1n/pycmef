
class SelfText
  constructor: ->
    try
      @check_cmef()
    catch Exception
      @fail()

    @validated()

  validated: ->
    $(".show-on-valid").show()

  fail: ->
    $(".show-on-failure").show()

  check_cmef: ->
    unless cmef.initialized
      throw new Exception('CMEF failed to initialized.')

cmef.ready ->
  window.selftest = new SelfText()