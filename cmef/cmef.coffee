class CMEF
  constructor: ->
    console.log("Initializing...")

    @events = {}

    _experiment.on_event_response.connect (event, response) =>
      console.log("Recieved event: #{event} -> #{response}")
      @handle_event_response(event, response)

    @initialized = true

  experiment: ->
    JSON.parse _experiment.experiment

  handle_event_response: (event, response) ->
    cbs = @events[event] if @events.hasOwnProperty(event)
    @events[event] = []
    return if !cbs

    for cb in cbs
      cb(response)

  add_event_callback: (event, cb) ->
    @events[event] = [] unless @events.hasOwnProperty(event)

    if cb instanceof Function
      @events[event].push cb

    return

  emit: (event, cb_or_args, cb) ->
    if cb_or_args instanceof Function
      cb = cb_or_args
      cb_or_args = ''
    else if cb_or_args instanceof Object
      cb_or_args = JSON.stringify(cb_or_args)

    args = cb_or_args

    @add_event_callback(event, cb)
    _experiment.emit(event, args)
    return

# Callback triggered when the Python ThinClient is ready.
window.on_python_ready = ->
  load_jquery = (callback) ->
    
    # Adding the script tag to the head as suggested before
    head = document.getElementsByTagName("head")[0]
    script = document.createElement("script")
    script.type = "text/javascript"
    script.src = "cmef/jquery.js"
    
    # Then bind the event to the callback function.
    # There are several events for cross browser compatibility.
    script.onreadystatechange = callback
    script.onload = callback
    
    # Fire the loading
    head.appendChild script
    return

  instantiate_cmef = ->
    return if window.cmef
    window.cmef = new CMEF()

    cmef.emit "show", (response) ->
      $(".hidden-until-load").show()

  load_jquery(instantiate_cmef)

# (->
#   if navigator.userAgent.search(/Python/i) is -1
#     console.log "disease"
#   else
#     console.log "disease"
#   return
# )()