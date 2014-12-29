
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
      participant = $('#participant_id').val()
      condition = $('#condition').val()

      unless participant > 0
        console.log('Invalid Participant')
        return

      if cmef.experiment.conditions instanceof Array
        unless condition in cmef.experiment.conditions
          console.log('Invalid Condition')
          return

      cmef.emit 'start', {
        participant: participant,
        condition: condition
      }

    # For debug purposes.
    # cmef.emit 'start', {
    #   participant: "1337",
    #   condition: "A"
    # }
  fail: ->
    $(".show-on-failure").show()

  check_cmef: ->
    unless cmef.initialized
      throw new Exception('CMEF failed to initialized.')

cmef.ready ->
  window.selftest = new SelfText()
