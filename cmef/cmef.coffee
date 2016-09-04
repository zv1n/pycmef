class window.Timer
  constructor: (@name, @duration) ->
    @running = false

    @timer_dom = $("##{@name}.timer")
    @bar_timer_dom = $("##{@name}.bar-timer")

    if @bar_timer_dom.length > 0
      @bar_delta = @bar_timer_dom.width() / @duration
    else
      @bar_delta = @duration

    @update_displays(false)

  epoch: ->
    (new Date).getTime()

  start: (cb) ->
    cmef.add_event_callback("timer:#{@name}", cb) if (cb)
    @epoch_duration = @duration + @epoch()
    @running = true

    setTimeout(=>
      console.log("handle event!!")
      cmef.handle_event_response("timer:#{@name}", {})
    , @duration)
    @update_displays(true)

  update_displays: (schedule) ->
    @update_timer(schedule)
    @update_bar_timer(schedule)

  run_timer: ->
    @start()

  is_running: ->
    @running

  update_timer: (schedule) ->
    if @timer_dom.length > 0
      @schedule_update(1000, @update_timer) if schedule
      @timer_dom.html(Math.floor(@delta/1000))

  update_bar_timer: (schedule) ->
    if @bar_timer_dom.length > 0
      @schedule_update(@bar_delta, @update_bar_timer) if schedule
      if !@running
        @bar_timer_dom.css("width", "100%")
      else
        percent = 100.0 * @delta / @duration
        @bar_timer_dom.css("width", "#{percent}%")

        if percent > 15.0 and percent <= 30.0
          @bar_timer_dom.addClass('slow-pulse')
        else
          @bar_timer_dom.removeClass('slow-pulse')

        if percent <= 15.0
          @bar_timer_dom.addClass('fast-pulse')
        else
          @bar_timer_dom.removeClass('fast-pulse')

  schedule_update: (timeout, cb) ->
    if @delta < timeout
      timeout = @delta

    if timeout > 0
      setTimeout(=>
        @delta = @epoch_duration - @epoch()
        cb.apply(this, [true])
      , timeout)
    else
      @running = false


class window.DataGrid
  constructor: (@selector, @data = undefined) ->
    @container = $(@selector)
    @data ?= cmef.current

  render: (ts, options, cb)->
    @template(ts)
    @options = $.extend({
      columns: 5
    }, options)

    klass = 'pure-u-1-5'
    klass = 'pure-u-4-24' if @options.columns == 6

    for data, idx in @data
      do (data, idx) =>
        data = cb(data, idx) if cb
        content = cmef.handlebars(@template, { data: data })
        sel = $('<div>').addClass('selection').append(content)
        grid = $('<div>').addClass(klass).append(sel)
        sel.data('content', data)
        @container.append(grid)

    @init_selectors()
    this

  selectable: (@selection_cb) ->
    this

  init_selectors: ->
    $('.selection', @container).off('.grid-manager')
    .on('click.grid-manager', (event) =>
      selection = $(event.currentTarget)
      data = selection.data('content')
      @selection_cb(selection, data) if @selection_cb
    )
    this

  template: (ts) ->
    if (ts)
      @template_selector = ts
      @template = $(@template_selector)
    this


# Manage multiple views on the same page.  Each can be controlled using
# Generate methods for:
#  show_[classname]()           -> show classname and hide all others
#  just_show_[classname](bool)  -> show or hide this class name
#  refresh_[classname](data)    -> refresh the container with the provided
#                                  data object.
class window.ViewManager
  constructor: (hash) ->
    @views = hash

    if typeof hash is 'string'
      @views = {}
      for klass in arguments
        @views[klass] = ".#{klass}"

    @switch_hide_type()
    @generate_methods()
    this

  switch_hide_type: ->
    for name, selector of @views
      sel = $(selector)
      if sel.hasClass('hidden')
        sel.hide()
        sel.removeClass('hidden')

  generate_methods: ->
    @generate_just_show_methods()
    @generate_show_methods()
    @generate_template_methods()
    this

  generate_just_show_methods: ->
    for name, selector of @views
      do (name) =>
        selector = @views[name]
        this["just_show_#{name}"] = (param) ->
          sel = $(selector)
          if (param)
            sel.show()
          else
            sel.hide()

          $('.validatable', sel).trigger('data:vis-change')
          this
    this

  trigger_visibility: ->
    for name, selector of @views
      $('.validatable', selector).trigger('data:vis-change')

  generate_show_methods: ->
    for name, selector of @views
      do (name) =>
        sel = @views[name]
        this["only_show_#{name}"] = this["show_#{name}"] = ->
          for hname, hsel of @views
            continue if hname == name
            $(hsel).hide()
          $(sel).show()
          @trigger_visibility()
          this
    this

  generate_template_methods: ->
    for name, selector of @views
      do (name) =>
        this["refresh_#{name}"] = (param) ->
          container = $(@views[name])
          cmef.auto_populate_common(container, { data: param })
          cmef.auto_template(container, { data: param })
          @trigger_visibility()
          this
    this

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


class MatchValue
  constructor: (@validator, @name, @value) ->

  is_valid: (val) ->
    value = Handlebars.compile("{{#{@value}}}")({ data: cmef.current })
    valid = (val.toString() == value.toString())
    @validator.valid(@name, valid)
    true

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
          @validity[name] = !$(event.currentTarget).is(':visible') || comparison.is_valid(event.currentTarget.value)

          if @all_valid()
            $('[data-enable-on-valid]').attr('disabled', false).removeClass('pure-button-disabled')
          else
            $('[data-enable-on-valid]').attr('disabled', true).addClass('pure-button-disabled')

        dom.on 'change.validate', change
        dom.on 'keyup.validate', change
        dom.on 'data:modified.validate', change
        dom.on 'data:vis-change', change

        dom.addClass('validatable')
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
      when 'match-value' then return new MatchValue(this, name, value)
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
    @handle_event_response('data-ready', {})

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
    @results = JSON.parse(_experiment.results)
    @condition = _experiment.current_condition

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

  data_ready: (cb) ->
    @add_event_callback('data-ready', cb)

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
