// Generated by CoffeeScript 1.10.0
(function() {
  var CMEF, Match, MatchAny, Range, Timer, Validator;

  Timer = (function() {
    function Timer(name1, duration1) {
      this.name = name1;
      this.duration = duration1;
      this.current = 0;
      this.running = false;
      this.dom = $("#" + this.name + ".timer");
      this.update_display(false);
    }

    Timer.prototype.run_timer = function() {
      this.running = true;
      setTimeout((function(_this) {
        return function() {
          return cmef.handle_event_response("timer:" + _this.name, {});
        };
      })(this), this.duration);
      return this.update_display(true);
    };

    Timer.prototype.is_running = function() {
      return this.running;
    };

    Timer.prototype.update_display = function(schedule) {
      if (!(this.dom.length > 0)) {
        return;
      }
      this.delta = this.duration - this.current;
      if (schedule) {
        this.schedule_update(1000);
      }
      return this.dom.html(Math.floor(this.delta / 1000));
    };

    Timer.prototype.schedule_update = function(timeout) {
      if (this.delta < timeout) {
        timeout = this.delta;
      }
      return setTimeout((function(_this) {
        return function() {
          _this.current += timeout;
          return _this.update_display(true);
        };
      })(this), timeout);
    };

    return Timer;

  })();

  window.DataGrid = (function() {
    function DataGrid(selector1, data1) {
      this.selector = selector1;
      this.data = data1 != null ? data1 : void 0;
      this.container = $(this.selector);
      if (this.data == null) {
        this.data = cmef.current;
      }
    }

    DataGrid.prototype.render = function(ts, options, cb) {
      var data, fn, idx, j, klass, len, ref;
      this.template(ts);
      this.options = $.extend({
        columns: 5
      }, options);
      klass = 'pure-u-1-5';
      if (this.options.columns === 6) {
        klass = 'pure-u-4-24';
      }
      ref = this.data;
      fn = (function(_this) {
        return function(data, idx) {
          var content, grid, sel;
          if (cb) {
            data = cb(data, idx);
          }
          content = cmef.handlebars(_this.template, {
            data: data
          });
          sel = $('<div>').addClass('selection').append(content);
          grid = $('<div>').addClass(klass).append(sel);
          sel.data('content', data);
          return _this.container.append(grid);
        };
      })(this);
      for (idx = j = 0, len = ref.length; j < len; idx = ++j) {
        data = ref[idx];
        fn(data, idx);
      }
      this.init_selectors();
      return this;
    };

    DataGrid.prototype.selectable = function(selection_cb) {
      this.selection_cb = selection_cb;
      return this;
    };

    DataGrid.prototype.init_selectors = function() {
      $('.selection', this.container).off('.grid-manager').on('click.grid-manager', (function(_this) {
        return function(event) {
          var data, selection;
          selection = $(event.currentTarget);
          data = selection.data('content');
          if (_this.selection_cb) {
            return _this.selection_cb(selection, data);
          }
        };
      })(this));
      return this;
    };

    DataGrid.prototype.template = function(ts) {
      if (ts) {
        this.template_selector = ts;
        this.template = $(this.template_selector);
      }
      return this;
    };

    return DataGrid;

  })();

  window.ViewManager = (function() {
    function ViewManager(hash) {
      var j, klass, len;
      this.views = hash;
      if (typeof hash === 'string') {
        this.views = {};
        for (j = 0, len = arguments.length; j < len; j++) {
          klass = arguments[j];
          this.views[klass] = "." + klass;
        }
      }
      this.generate_methods();
      this;
    }

    ViewManager.prototype.generate_methods = function() {
      this.generate_just_show_methods();
      this.generate_show_methods();
      this.generate_template_methods();
      return this;
    };

    ViewManager.prototype.generate_just_show_methods = function() {
      var fn, name, ref, selector;
      ref = this.views;
      fn = (function(_this) {
        return function(name) {
          selector = _this.views[name];
          return _this["just_show_" + name] = function(param) {
            var sel;
            sel = $(selector);
            if (param) {
              sel.show();
            } else {
              sel.hide();
            }
            $('.validatable', sel).trigger('data:vis-change');
            return this;
          };
        };
      })(this);
      for (name in ref) {
        selector = ref[name];
        fn(name);
      }
      return this;
    };

    ViewManager.prototype.trigger_visibility = function() {
      var name, ref, results, selector;
      ref = this.views;
      results = [];
      for (name in ref) {
        selector = ref[name];
        results.push($('.validatable', selector).trigger('data:vis-change'));
      }
      return results;
    };

    ViewManager.prototype.generate_show_methods = function() {
      var fn, name, ref, selector;
      ref = this.views;
      fn = (function(_this) {
        return function(name) {
          var sel;
          sel = _this.views[name];
          return _this["only_show_" + name] = _this["show_" + name] = function() {
            var hname, hsel, ref1;
            ref1 = this.views;
            for (hname in ref1) {
              hsel = ref1[hname];
              if (hname === name) {
                continue;
              }
              $(hsel).hide();
            }
            $(sel).show();
            this.trigger_visibility();
            return this;
          };
        };
      })(this);
      for (name in ref) {
        selector = ref[name];
        fn(name);
      }
      return this;
    };

    ViewManager.prototype.generate_template_methods = function() {
      var fn, name, ref, selector;
      ref = this.views;
      fn = (function(_this) {
        return function(name) {
          return _this["refresh_" + name] = function(param) {
            var container;
            container = $(this.views[name]);
            cmef.auto_populate_common(container, {
              data: param
            });
            cmef.auto_template(container, {
              data: param
            });
            this.trigger_visibility();
            return this;
          };
        };
      })(this);
      for (name in ref) {
        selector = ref[name];
        fn(name);
      }
      return this;
    };

    return ViewManager;

  })();

  Range = (function() {
    function Range(validator1, name1, value1) {
      var list;
      this.validator = validator1;
      this.name = name1;
      this.value = value1;
      list = this.value.split('-');
      if (list.length === 2) {
        this.low = parseInt(list[0]);
        this.high = parseInt(list[1]);
      } else {
        this.low = 0;
        this.high = parseInt(list[0]);
      }
    }

    Range.prototype.is_valid = function(val) {
      var ival;
      ival = parseInt(val);
      return ival >= this.low && ival <= this.high;
    };

    return Range;

  })();

  Match = (function() {
    function Match(validator1, name1, value1) {
      this.validator = validator1;
      this.name = name1;
      this.value = value1;
    }

    Match.prototype.is_valid = function(val) {
      var valid;
      valid = val.substring(0, 3) === this.value.substring(0, 3);
      this.validator.valid(this.name, valid);
      return true;
    };

    return Match;

  })();

  MatchAny = (function() {
    function MatchAny(validator1, name1, value1) {
      this.validator = validator1;
      this.name = name1;
      this.value = value1;
    }

    MatchAny.prototype.is_valid = function(val) {
      var data, j, len, ref, valid, value;
      ref = cmef.dataset;
      for (j = 0, len = ref.length; j < len; j++) {
        data = ref[j];
        value = Handlebars.compile("{{" + this.value + "}}")({
          data: data
        });
        valid = val.substring(0, 3) === value.substring(0, 3);
        if (valid) {
          cmef.responses.data = data;
          this.validator.valid(this.name, valid);
          return true;
        }
      }
      this.validator.valid(this.name, false);
      return true;
    };

    return MatchAny;

  })();

  Validator = (function() {
    function Validator(constraints) {
      var fn, name;
      this.constraints = constraints;
      this.validity = {};
      fn = (function(_this) {
        return function(name) {
          var change, comparison, constraint, dom, value;
          dom = $("[name='" + name + "']");
          constraint = _this.constraints[name];
          value = void 0;
          if ('value' in constraint) {
            value = cmef.handlebars_value(constraint.value);
          }
          comparison = _this.comparator(name, constraint.type, value);
          dom.data('validator', comparison);
          change = function(event) {
            _this.validity[name] = !$(event.currentTarget).is(':visible') || comparison.is_valid(event.currentTarget.value);
            if (_this.all_valid()) {
              return $('[data-enable-on-valid]').attr('disabled', false).removeClass('pure-button-disabled');
            } else {
              return $('[data-enable-on-valid]').attr('disabled', true).addClass('pure-button-disabled');
            }
          };
          dom.on('change.validate', change);
          dom.on('keyup.validate', change);
          dom.on('data:modified.validate', change);
          dom.on('data:vis-change', change);
          dom.addClass('validatable');
          return dom.trigger('data:modified');
        };
      })(this);
      for (name in this.constraints) {
        fn(name);
      }
    }

    Validator.prototype.all_valid = function() {
      var f, res;
      res = true;
      for (f in this.validity) {
        res = res && this.validity[f];
      }
      return res;
    };

    Validator.prototype.comparator = function(name, type, value) {
      switch (type) {
        case 'range':
          return new Range(this, name, value);
        case 'match':
          return new Match(this, name, value);
        case 'match-any':
          return new MatchAny(this, name, value);
        default:
          return void 0;
      }
    };

    Validator.prototype.valid = function(name, val) {
      return cmef.responses[name + "_correct"] = val;
    };

    return Validator;

  })();

  CMEF = (function() {
    function CMEF() {
      this.events = {};
      this.responses = {};
      this.event_count = 0;
      this.times = {};
      this.iselectors = [];
      this.on_next = [];
      this.loadables = 0;
      this.want_screencap = false;
      this.mark('load');
    }

    CMEF.prototype.initialize_experiment = function() {
      _experiment.on_event_response.connect((function(_this) {
        return function(event, response) {
          _this.event_count++;
          return _this.handle_event_response(event, response);
        };
      })(this));
      this.load_data();
      this.init_handlebars();
      this.initialized = true;
      this.default_methods();
      this.auto_populate_common();
      this.auto_template();
      this.auto_enable();
      this.auto_input();
      this.auto_eyetracker();
      this.init_timers();
      this.init_validators();
      this.handle_event_response('ready', {});
      this.emit("show", (function(_this) {
        return function(response) {
          _this.mark('show');
          $(".show-on-load").show();
          if ($('body').data('eyetracker')) {
            return setTimeout(function() {
              return _this.screencap();
            }, 500);
          }
        };
      })(this));
    };

    CMEF.prototype.load_data = function() {
      this.current = JSON.parse(_experiment.current || '{}');
      this.dataset = JSON.parse(_experiment.dataset || '{}');
      this.datasets = JSON.parse(_experiment.datasets || '{}');
      this.subsection = JSON.parse(_experiment.subsection);
      this.experiment = JSON.parse(_experiment.experiment);
      this.results = JSON.parse(_experiment.results);
      this.condition = _experiment.current_condition;
    };

    CMEF.prototype.mark = function(name) {
      return this.times[name] = (new Date()).getTime();
    };

    CMEF.prototype.default_methods = function() {
      $('[data-default="true"]').click((function(_this) {
        return function(event) {
          _this.mark('submit');
          return _this.submit(_this.collect_response());
        };
      })(this));
    };

    CMEF.prototype.submit = function(content) {
      var cb, j, len, ref;
      ref = this.on_next;
      for (j = 0, len = ref.length; j < len; j++) {
        cb = ref[j];
        cb();
      }
      return this.emit('next', content);
    };

    CMEF.prototype.init_validators = function() {
      if (this.subsection.constraints) {
        return this.validator = new Validator(this.subsection.constraints);
      }
    };

    CMEF.prototype.init_timers = function() {
      var duration, name, ref, results;
      if (this.timers == null) {
        this.timers = [];
      }
      ref = this.subsection.timers;
      results = [];
      for (name in ref) {
        duration = ref[name];
        results.push(this.timers.push(new Timer(name, duration)));
      }
      return results;
    };

    CMEF.prototype.auto_input = function() {
      var j, len, ref, target;
      ref = $('[data-input]');
      for (j = 0, len = ref.length; j < len; j++) {
        target = ref[j];
        this.input_selectors($(target).data('input').split(','));
      }
    };

    CMEF.prototype.auto_eyetracker = function() {
      if ($('body').data('eyetracker')) {
        this.emit('start_eyetracker');
        this.before_submit((function(_this) {
          return function() {
            return _this.emit('stop_eyetracker');
          };
        })(this));
      }
    };

    CMEF.prototype.auto_populate = function(type, modifier, container, data) {
      var j, len, ref, render, target, value;
      ref = $("[data-" + type + "]", container);
      for (j = 0, len = ref.length; j < len; j++) {
        target = ref[j];
        target = $(target);
        value = target.data('value');
        render = target.data('render');
        data || (data = this.render_data());
        if (!render) {
          render = Handlebars.compile(value);
          target.data('render', render);
        }
        this.track_loadables(modifier(target, render(data)));
      }
    };

    CMEF.prototype.auto_populate_common = function(container, data) {
      this.auto_populate('attribute', function(target, value) {
        var attr;
        attr = target.data('attribute');
        return target.attr(attr, value);
      }, container, data);
      return this.auto_populate('content', function(target, value) {
        return target.html(value);
      }, container, data);
    };

    CMEF.prototype.render_data = function() {
      return {
        data: this.current,
        experiment: this.experiment,
        dataset: this.dataset
      };
    };

    CMEF.prototype.handlebars = function($target, data) {
      var html, rendered;
      data || (data = this.render_data());
      html = Handlebars.compile($target.html())(data);
      rendered = $(html);
      this.track_loadables(rendered);
      return rendered;
    };

    CMEF.prototype.handlebars_value = function(value) {
      return Handlebars.compile(value)(this.render_data());
    };

    CMEF.prototype.auto_template = function(container, data) {
      var $target, j, len, ref, rendered, target;
      ref = $("[type='text/x-handlebars-template']", container);
      for (j = 0, len = ref.length; j < len; j++) {
        target = ref[j];
        $target = $(target);
        if ($target.data('auto') === false) {
          continue;
        }
        rendered = this.handlebars($target, data);
        rendered.insertBefore($target);
      }
    };

    CMEF.prototype.auto_enable = function() {
      var $target, change, etarg, j, k, len, len1, ref, ref1, selector, target;
      ref = $("[data-enable-on]");
      for (j = 0, len = ref.length; j < len; j++) {
        target = ref[j];
        $target = $(target);
        $target.addClass('pure-button-disabled').attr('disabled', true);
        selector = $target.data('enable-on');
        etarg = $(selector).data('enable-target', target);
        change = function() {
          var validator;
          validator = etarg.data('validator');
          if (validator) {
            if (!validator.is_valid(etarg.val())) {
              return;
            }
          }
          return $target.removeClass('pure-button-disabled').attr('disabled', false);
        };
        etarg.change(change);
        etarg.keyup(change);
      }
      ref1 = $("[data-enable-on-valid]");
      for (k = 0, len1 = ref1.length; k < len1; k++) {
        target = ref1[k];
        $target = $(target);
        $target.addClass('pure-button-disabled').attr('disabled', true);
      }
    };

    CMEF.prototype.track_loadable = function(img) {
      this.loadables++;
      return $(img).ready((function(_this) {
        return function() {
          _this.loadables--;
          if (_this.loadables === 0) {
            return _this.handle_event_response('load:complete', {});
          }
        };
      })(this));
    };

    CMEF.prototype.track_loadables = function(html) {
      var img, j, len, ref;
      if (html.is('img, svg, canvas')) {
        this.track_loadable(html);
      } else {
        ref = $('img, svg, canvas', html);
        for (j = 0, len = ref.length; j < len; j++) {
          img = ref[j];
          this.track_loadable(img);
        }
      }
    };

    CMEF.prototype.input_selectors = function(sels) {
      var f, j, len;
      if (!(sels instanceof Array)) {
        sels = [sels];
      }
      for (j = 0, len = sels.length; j < len; j++) {
        f = sels[j];
        this.iselectors.push(f);
      }
    };

    CMEF.prototype.collect_response = function() {
      var $target, cor, e, error, j, k, l, len, len1, len2, ref, ref1, ref2, res, sel, target, val;
      res = this.responses;
      res.times = this.times;
      if (!('data' in res)) {
        res.data = this.current;
      }
      ref = this.iselectors;
      for (j = 0, len = ref.length; j < len; j++) {
        sel = ref[j];
        ref1 = $(sel);
        for (k = 0, len1 = ref1.length; k < len1; k++) {
          target = ref1[k];
          $target = $(target);
          res[$target.attr('name')] = $target.val();
        }
      }
      ref2 = $('[data-collect=true]');
      for (l = 0, len2 = ref2.length; l < len2; l++) {
        sel = ref2[l];
        $target = $(sel);
        val = $target.val();
        if (!val) {
          val = $target.attr('value');
        }
        res[$target.attr('name')] = val;
      }
      try {
        cor = res.data.question.correct.toString() === res.answer.toString();
        res.correct = cor;
      } catch (error) {
        e = error;
      }
      return res;
    };

    CMEF.prototype.ready = function(cb) {
      return this.add_event_callback('ready', cb);
    };

    CMEF.prototype.load = function(cb) {
      return this.add_event_callback('load:complete', cb);
    };

    CMEF.prototype.screencap = function(name) {
      return this.emit('screen_capture', {
        name: name
      }, (function(_this) {
        return function(response) {
          var base;
          (base = _this.responses).screencap || (base.screencap = []);
          _this.responses.screencap.push(response);
        };
      })(this));
    };

    CMEF.prototype.before_submit = function(cb) {
      this.on_next || (this.on_next = []);
      return this.on_next.push(cb);
    };

    CMEF.prototype.experiment = function() {
      return JSON.parse(_experiment.experiment);
    };

    CMEF.prototype.handle_event_response = function(event, response) {
      var cb, cbs, j, len;
      if (this.events.hasOwnProperty(event)) {
        cbs = this.events[event];
      }
      this.events[event] = [];
      if (!cbs) {
        return;
      }
      for (j = 0, len = cbs.length; j < len; j++) {
        cb = cbs[j];
        setTimeout(function() {
          return cb(response);
        }, 1);
      }
    };

    CMEF.prototype.add_event_callback = function(event, cb) {
      if (!this.events.hasOwnProperty(event)) {
        this.events[event] = [];
      }
      if (cb instanceof Function) {
        this.events[event].push(cb);
      }
    };

    CMEF.prototype.timer = function(event, cb) {
      var j, len, ref, timer;
      this.add_event_callback("timer:" + event, cb);
      ref = this.timers;
      for (j = 0, len = ref.length; j < len; j++) {
        timer = ref[j];
        if (event === timer.name && !timer.is_running()) {
          timer.run_timer();
        }
      }
      return true;
    };

    CMEF.prototype.emit = function(event, cb_or_args, cb) {
      var args;
      if (cb_or_args instanceof Function) {
        cb = cb_or_args;
        cb_or_args = '';
      } else if (cb_or_args instanceof Object) {
        cb_or_args = JSON.stringify(cb_or_args);
      }
      args = cb_or_args;
      this.add_event_callback(event, cb);
      _experiment.emit(event, args);
    };

    CMEF.prototype.init_handlebars = function() {
      return Handlebars.registerHelper("each_random", function(context, options) {
        var data, i, j, key, keys, kidx, length, random, ref, results, ret;
        if (!options) {
          throw new Exception("Must pass iterator to #each_random");
        }
        ret = "";
        if (context instanceof Function) {
          context = context.call(this);
        }
        random = function(min, max) {
          return Math.floor(Math.random() * (max - min)) + min;
        };
        data = {};
        if (context && typeof context === "object") {
          keys = void 0;
          if (context instanceof Array) {
            keys = (function() {
              results = [];
              for (var j = 0, ref = context.length - 1; 0 <= ref ? j <= ref : j >= ref; 0 <= ref ? j++ : j--){ results.push(j); }
              return results;
            }).apply(this);
          } else {
            keys = Object.keys(context);
          }
          length = keys.length;
          i = 0;
          while (keys.length > 0) {
            kidx = random(0, keys.length);
            key = keys.splice(kidx, 1);
            data.index = key;
            data.key = key;
            data.order = i;
            ret = ret + options.fn(context[key], {
              data: data
            });
            i++;
          }
        }
        return ret;
      });
    };

    return CMEF;

  })();

  window.cmef = new CMEF();

  window.on_python_ready = function() {
    return setTimeout(function() {
      var instantiate_cmef, load_js;
      load_js = function(path, callback) {
        var head, script;
        head = document.getElementsByTagName("head")[0];
        script = document.createElement("script");
        script.type = "text/javascript";
        script.src = path;
        script.onreadystatechange = callback;
        script.onload = callback;
        head.appendChild(script);
      };
      instantiate_cmef = function() {
        return cmef.initialize_experiment();
      };
      return load_js("../cmef/jquery.js", function() {
        return load_js("../cmef/handlebars.js", instantiate_cmef);
      });
    }, 1);
  };

}).call(this);
