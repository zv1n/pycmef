
class CMEF
  constructor: ->
    @events = {}
    @responses = {}
    @event_count = 0
    @times = {}
    @iselectors = []
    @on_next = []
    @loadables = 0
    @want_screencap = false

    @mark('load')

  initialize_experiment: ->
    # console.log("Initializing...")

    _experiment.on_event_response.connect (event, response) =>
      # console.log("Recieved event(#{@event_count}): #{event} -> #{response}")
      @event_count++
      @handle_event_response(event, response)

    @load_data()
    @init_handlebars()

    @initialized = true

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
    @auto_input()
    @auto_eyetracker()

    @handle_event_response('ready', {})
    @emit "show", (response) =>
      @mark('show')
      $(".show-on-load").show()
      if $('body').data('eyetracker')
        setTimeout(=>
          @screencap()
        , 500)

    return

  load_data: ->
    @current = JSON.parse(_experiment.current || '{}')
    @data = JSON.parse(_experiment.dataset || '{}')
    @subsection = JSON.parse(_experiment.subsection)
    @experiment = JSON.parse(_experiment.experiment)

    return

  mark: (name) ->
    @times[name] = (new Date()).getTime()

  default_methods: ->
    $('#next[data-default="true"]').click (event) =>
      @mark('submit')
      @submit(@collect_response())

    return

  submit: (content) ->
    for cb in @on_next
      cb()

    @emit('next', content)

  auto_input: ->
    for target in $('[data-input]')
      @input_selectors($(target).data('input').split(','))

    return

  auto_eyetracker: ->
    if $('body').data('eyetracker')
      @emit('start_eyetracker')
      @before_submit => @emit('stop_eyetracker')

    return

  auto_populate: (type, modifier) ->
    for target in $("[data-#{type}]")
      target = $(target)
      value = target.data('value')
      render = target.data('render')

      if (!render)
        render = Handlebars.compile(value)
        target.data('render', render)

      @track_loadables modifier(target, render({
        data: @current
      }))

    return

  handlebars: ($target) ->
    html = Handlebars.compile($target.html())({
      data: @current
    })

    rendered = $(html)
    @track_loadables rendered
    rendered

  auto_template: ->
    for target in $("[type='text/x-handlebars-template']")
      $target = $(target)

      rendered = @handlebars($target)
      rendered.insertBefore($target)
    return

  auto_enable: ->
    for target in $("[data-enable-on]")
      $target = $(target)
      $target.addClass('pure-button-disabled').attr('disabled', true)
      selector = $target.data('enable-on')

      $(selector).data('enable-target', target).change ->
        $target.removeClass('pure-button-disabled').attr('disabled', false)

    return

  track_loadable: (img) ->
    @loadables++
    $(img).ready =>
      @loadables--
      @handle_event_response 'load:complete', {} if @loadables == 0

  track_loadables: (html)->
    if html.is('img, svg, canvas')
      @track_loadable html
    else
      for img in $('img, svg, canvas', html)
        @track_loadable img

    return

  input_selectors: (sels) ->
    unless sels instanceof Array
      sels = [sels]

    for f in sels
      @iselectors.push f

    return

  collect_response: ->
    res = @responses
    res.times = @times
    res.data = @current

    for sel in @iselectors
      for target in $(sel)
        $target = $(target)
        res[$target.attr('name')] = $target.val()

    for sel in $('[data-collect=true]')
      $target = $(sel)
      val = $target.val()
      val = $target.attr('value') unless val
      res[$target.attr('name')] = val

    try
      cor = res.data.question.correct.toString() == res.answer.toString()
      res.correct = cor
    catch e
      # res.indeterminate = true

    return res

  ready: (cb) ->
    @add_event_callback('ready', cb)

  load: (cb) ->
    @add_event_callback('load:complete', cb)

  screencap: (name) ->
    @emit('screen_capture', { name: name }, (response) =>
      @responses.screencap ||= []
      @responses.screencap.push response

      # TODO: Screen position doesn't quite translate.
      # for img in $('img[name]')
      #   targ = $(img)
      #   continue unless targ.is(':visible')

      #   @responses[targ.attr('name')] = {
      #     y: targ.offset().top + window.screenY,
      #     x: targ.offset().left + window.screenX,
      #     width: targ.width(),
      #     height: targ.height()
      #   }

      return
    )

  before_submit: (cb) ->
    @on_next ||= []
    @on_next.push cb

  experiment: ->
    JSON.parse _experiment.experiment

  handle_event_response: (event, response) ->
    cbs = @events[event] if @events.hasOwnProperty(event)
    @events[event] = []
    return if !cbs

    for cb in cbs
      setTimeout( ->
        cb(response)
      , 1)

    return

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

  init_handlebars: ->
    Handlebars.registerHelper "each_random", (context, options) ->
      throw new Exception("Must pass iterator to #each_random")  unless options

      ret = ""
      context = context.call(this)  if context instanceof Function

      random = (min, max) ->
        return Math.floor(Math.random() * (max - min)) + min

      data = {}
      
      if context and typeof context is "object"
        keys = undefined

        if context instanceof Array
          keys = [0..context.length-1]
        else
          keys = Object.keys(context)

        length = keys.length

        i = 0
        while keys.length > 0
          kidx = random(0, keys.length)
          key = keys.splice(kidx, 1)
          data.index = key
          data.key = key
          data.order = i
          ret = ret + options.fn(context[key], { data: data })
          i++

      ret

window.cmef = new CMEF()

# Callback triggered when the Python ThinClient is ready.
window.on_python_ready = ->
  setTimeout(->
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

    load_js "../cmef/jquery.js", ->
      load_js "../cmef/handlebars.js", instantiate_cmef
  ,1)

  # (->
  #   if navigator.userAgent.search(/Python/i) is -1
  #     console.log "disease"
  #   else
  #     console.log "disease"
  #   return
  # )()