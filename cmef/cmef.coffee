class CMEF
  constructor: ->
    @events = {}
    @event_count = 0
    @times = {}

    @mark('load')

  initialize_experiment: ->
    # console.log("Initializing...")

    _experiment.on_event_response.connect (event, response) =>
      # console.log("Recieved event(#{@event_count}): #{event} -> #{response}")
      @event_count++
      @handle_event_response(event, response)

    @load_data()

    @initialized = true
    @handle_event_response('ready', {})

    @default_methods()

    @auto_populate('attribute', (target, value) ->
      attr = target.data('attribute')
      target.attr(attr, value)
    )

    @auto_populate('content', (target, value) ->
      target.html(value)
    )

    @auto_template()
    @auto_enable()

  load_data: ->
    @current = JSON.parse(_experiment.current)
    @data = JSON.parse(_experiment.dataset)
    @subsection = JSON.parse(_experiment.subsection)
    @experiment = JSON.parse(_experiment.experiment)

  mark: (name) ->
    @times[name] = new Date()

  default_methods: ->
    console.log $('input').length
    $('#next[data-default="true"]').click (event) =>
      @mark('next')
      @emit('next', @collect_response())

  auto_populate: (type, modifier) ->
    for target in $("[data-#{type}]")
      target = $(target)
      value = target.data('value')
      render = target.data('render')

      if (!render)
        render = Handlebars.compile(value)
        target.data('render', render)

      modifier(target, render({
        data: @current
      }))

    return

  auto_template: ->
    for target in $("[type='text/x-handlebars-template']")
      $target = $(target)

      rendered = $(Handlebars.compile($target.html())({
        data: @current
      }))

      $(target.parentNode).append rendered

  auto_enable: ->
    for target in $("[data-enable-on]")
      $target = $(target)
      $target.addClass('pure-button-disabled')
      selector = $target.data('enable-on')

      $(selector).data('enable-target', target).change ->
        $target.removeClass('pure-button-disabled')


  input_selectors: (@input_selectors) ->

  collect_response: ->
    res = {}
    res.times = @times
    res.data = @data

    for sel in @input_selectors
      $target = $(sel)
      res[$target.attr('name')] = $target.val()

    return res

  ready: (cb) ->
    @add_event_callback('ready', cb)

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
  load_js = (path, callback) ->
    #console.log('Force loading JQuery...')

    # Adding the script tag to the head as suggested before
    head = document.getElementsByTagName("head")[0]
    script = document.createElement("script")
    script.type = "text/javascript"
    script.src = path
    
    # Then bind the event to the callback function.
    # There are several events for cross browser compatibility.
    script.onreadystatechange = callback
    script.onload = callback
    
    # Fire the loading
    head.appendChild script
    return

  instantiate_cmef = ->
    cmef.initialize_experiment()

    cmef.emit "show", (response) ->
      cmef.mark('show')
      $(".show-on-load").show()

  load_js "../cmef/jquery.js", ->
    load_js "../cmef/handlebars.js", instantiate_cmef


# (->
#   if navigator.userAgent.search(/Python/i) is -1
#     console.log "disease"
#   else
#     console.log "disease"
#   return
# )()