class CMEF
  constructor: ->
    @events = {}
    @event_count = 0

  initialize_experiment: ->
    console.log("Initializing...")

    _experiment.on_event_response.connect (event, response) =>
      console.log("Recieved event(#{@event_count}): #{event} -> #{response}")
      @event_count++
      @handle_event_response(event, response)

    @initialized = true
    @handle_event_response('ready', {})

  ready: (cb) ->
    @add_event_callback('ready', cb)

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

window.cmef = new CMEF()

# Callback triggered when the Python ThinClient is ready.
window.on_python_ready = ->
  load_jquery = (callback) ->
    
    unless window.jQuery
      console.log('Force loading JQuery...')

      # Adding the script tag to the head as suggested before
      head = document.getElementsByTagName("head")[0]
      script = document.createElement("script")
      script.type = "text/javascript"
      script.src = "jquery.js"
      
      # Then bind the event to the callback function.
      # There are several events for cross browser compatibility.
      script.onreadystatechange = callback
      script.onload = callback
      
      # Fire the loading
      head.appendChild script
      return
    else
      callback()

  instantiate_cmef = ->
    cmef.initialize_experiment()

    cmef.emit "show", (response) ->
      $(".show-on-load").show()

  load_jquery(instantiate_cmef)

# (->
#   if navigator.userAgent.search(/Python/i) is -1
#     console.log "disease"
#   else
#     console.log "disease"
#   return
# )()