class Timer
  constructor: (@name, @duration) ->
    @current = 0
    @running = false
    @dom = $("##{@name}.timer")

    @update_display(false)

  run_timer: ->
    @running = true
    setTimeout(=>
      cmef.handle_event_response("timer:#{@name}", {})
    , @duration)

    @update_display(true)

  is_running: ->
    @running

  update_display: (schedule) ->
    return unless @dom.length > 0

    @delta = @duration - @current
    @schedule_update(1000) if schedule

    @dom.html(Math.floor(@delta/1000))

  schedule_update: (timeout) ->
    if @delta < timeout
      timeout = @delta

    setTimeout(=>
      @current += timeout
      @update_display(true)
    , timeout)


class window.DataGrid
  constructor: (@selector) ->
    @container = $(@selector)

  render: (ts)->
    @template(ts)

    for data in cmef.current
      do (data) =>
        content = cmef.handlebars(@template, { data: data })
        sel = $('<div>').addClass('selection').append(content)
        grid = $('<div>').addClass('pure-u-1-5').append(sel)
        sel.data('content', data)
        @container.append(grid)
    @init_selectors()

  selectable: (@selection_cb) ->

  init_selectors: ->
    $('.selection', @container).off('.grid-manager')
    .on('click.grid-manager', (event) =>
      selection = $(event.currentTarget)
      data = selection.data('content')
      @selection_cb(selection, data) if @selection_cb
    )

  template: (ts) ->
    if (ts)
      @template_selector = ts
      @template = $(@template_selector)


# Manage multiple views on the same page.  Each can be controlled using
# Generate methods for:
#  show_[classname]()           -> show classname and hide all others
#  just_show_[classname](bool)  -> show or hide this class name
#  refresh_[classname](data)    -> refresh the container with the provided
#                                  data object.
class window.ViewManager
  constructor: () ->
    @views = arguments
    @generate_methods()

  generate_methods: ->
    @generate_just_show_methods()
    @generate_show_methods()
    @generate_template_methods()

  generate_just_show_methods: ->
    for view in @views
      body = """
              if (param) {
                $('.#{view}').show();
              } else {
                $('.#{view}').hide();
              }
             """

      @generate_method("just_show_#{view}", body)

  generate_show_methods: ->
    for view in @views

      show = []
      for showview in @views
        continue if showview == view
        show.push "$('.#{showview}').hide();"
      show.push "$('.#{view}').show();"

      @generate_method("show_#{view}", show.join(''))

  generate_template_methods: ->
    for view in @views
      body = """
        var container = $(".#{view}");
        cmef.auto_populate_common(container, { data: param });
        cmef.auto_template(container, { data: param });
      """
      @generate_method("refresh_#{view}", body)

  generate_method: (name, contents) ->
    method = [
      "this.#{name} = function (param) {"
      contents,
      "}"
    ].join('')
    # console.log("Generating method: ", method)
    eval(method)


class Range
  constructor: (@validator, @name, @value) ->
    list = @value.split('-')

    if list.length == 2
      @low = parseInt(list[0])
      @high = parseInt(list[1])
    else
      @low = 0
      @high = parseInt(list[0])

  is_valid: (val) ->
    ival = parseInt(val)
    return (ival >= @low && ival <= @high)




class Match
  constructor: (@validator, @name, @value) ->

  is_valid: (val) ->
    valid = (val.substring(0,3) == @value.substring(0,3))
    @validator.valid(@name, valid)
    true


class MatchAny
  constructor: (@validator, @name, @value) ->

  is_valid: (val) ->
    for data in cmef.dataset
      value = Handlebars.compile("{{#{@value}}}")({ data: data })
      valid = (val.substring(0,3) == value.substring(0,3))

      if valid
        cmef.responses.data = data
        @validator.valid(@name, valid)
        return true

    @validator.valid(@name, false)
    return true



class Validator
  constructor: (@constraints) ->
    @validity = {}

    for name of @constraints
      do (name) =>
        dom = $("[name='#{name}']")
        constraint = @constraints[name]
        value = undefined

        if 'value' of constraint
          value = cmef.handlebars_value(constraint.value)

        comparison = @comparator(name, constraint.type, value)
        dom.data('validator', comparison)

        change = (event) =>
          @validity[name] = comparison.is_valid(event.currentTarget.value)

          if @all_valid()
            $('[data-enable-on-valid]').attr('disabled', false).removeClass('pure-button-disabled')
          else
            $('[data-enable-on-valid]').attr('disabled', true).addClass('pure-button-disabled')

        dom.on 'change.validate', change
        dom.on 'keyup.validate', change
        dom.on 'data:modified.validate', change

        dom.trigger('data:modified')

  all_valid: ->
    res = true
    for f of @validity
      res = res && @validity[f]
    return res

  comparator: (name, type, value) ->
    switch type
      when 'range' then return new Range(this, name, value)
      when 'match' then return new Match(this, name, value)
      when 'match-any' then return new MatchAny(this, name, value)
      else return undefined

  valid: (name, val) ->
    cmef.responses["#{name}_correct"] = val


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

    @auto_populate_common()
    @auto_template()
    @auto_enable()
    @auto_input()
    @auto_eyetracker()

    @init_timers()
    @init_validators()

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
    @dataset = JSON.parse(_experiment.dataset || '{}')
    @datasets = JSON.parse(_experiment.datasets || '{}')
    @subsection = JSON.parse(_experiment.subsection)
    @experiment = JSON.parse(_experiment.experiment)

    return

  mark: (name) ->
    @times[name] = (new Date()).getTime()

  default_methods: ->
    $('[data-default="true"]').click (event) =>
      @mark('submit')
      @submit(@collect_response())

    return

  submit: (content) ->
    for cb in @on_next
      cb()

    @emit('next', content)

  init_validators: ->
    if @subsection.constraints
      @validator = new Validator(@subsection.constraints)

  init_timers: ->
    @timers ?= []

    for name, duration of @subsection.timers
      @timers.push new Timer(name, duration)

  auto_input: ->
    for target in $('[data-input]')
      @input_selectors($(target).data('input').split(','))

    return

  auto_eyetracker: ->
    if $('body').data('eyetracker')
      @emit('start_eyetracker')
      @before_submit => @emit('stop_eyetracker')

    return

  auto_populate: (type, modifier, container, data) ->
    for target in $("[data-#{type}]", container)
      target = $(target)
      value = target.data('value')
      render = target.data('render')
      data ||= @render_data()

      if (!render)
        render = Handlebars.compile(value)
        target.data('render', render)

      @track_loadables modifier(target, render(data))

    return

  auto_populate_common: (container, data) ->
    @auto_populate('attribute',
      (target, value) ->
        attr = target.data('attribute')
        target.attr(attr, value)
      ,
      container, data
    )

    @auto_populate('content',
      (target, value) ->
        target.html(value)
      ,
      container, data
    )

  render_data: ->
    {
      data: @current,
      experiment: @experiment,
      dataset: @dataset
    }

  handlebars: ($target, data) ->
    data ||= @render_data()
    html = Handlebars.compile($target.html())(data)

    rendered = $(html)
    @track_loadables rendered
    rendered

  handlebars_value: (value) ->
    Handlebars.compile(value)(@render_data())

  auto_template: (container, data) ->
    for target in $("[type='text/x-handlebars-template']", container)
      $target = $(target)
      continue if $target.data('auto') == false
      rendered = @handlebars($target, data)
      rendered.insertBefore($target)
    return

  auto_enable: ->
    for target in $("[data-enable-on]")
      $target = $(target)
      $target.addClass('pure-button-disabled').attr('disabled', true)
      selector = $target.data('enable-on')

      etarg = $(selector).data('enable-target', target)

      change = ->
        validator = etarg.data('validator')

        if validator
          return unless validator.is_valid(etarg.val())

        $target.removeClass('pure-button-disabled').attr('disabled', false)

      etarg.change change
      etarg.keyup change

    for target in $("[data-enable-on-valid]")
      $target = $(target)
      $target.addClass('pure-button-disabled').attr('disabled', true)

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

    unless 'data' of res
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

  timer: (event, cb) ->
    @add_event_callback("timer:#{event}", cb)

    for timer in @timers
      if event == timer.name && !timer.is_running()
        timer.run_timer()

    true

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