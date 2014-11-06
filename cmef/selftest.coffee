
class SelfText
  constructor: ->
    try
      @check_cmef()
    catch Exception
      @fail()

    @validated()
    @gtg = true

  validated: ->
    $(".show-on-valid").show()
    $("#begin").click (event) ->
      return unless $('#pid').val() > 0
      cmef.emit 'start', (response) ->
        # console.log("selftest.js - Next: #{response}")

  fail: ->
    $(".show-on-failure").show()

  check_cmef: ->
    unless cmef.initialized
      throw new Exception('CMEF failed to initialized.')

cmef.ready ->
  window.selftest = new SelfText()
