
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
      participant = $('#pid').val()
      condition = $('#condition').val()
      return unless participant > 0
      cmef.emit 'start', {
        participant: participant,
        condition: condition
      }

  fail: ->
    $(".show-on-failure").show()

  check_cmef: ->
    unless cmef.initialized
      throw new Exception('CMEF failed to initialized.')

cmef.ready ->
  window.selftest = new SelfText()
