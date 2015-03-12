// Generated by CoffeeScript 1.3.3
(function() {
  var CMEF, Match, Range, Timer, Validator;

  Timer = (function() {

    function Timer(name, duration) {
      var _this = this;
      this.name = name;
      this.duration = duration;
      this.current = 0;
      this.init_dom();
      setTimeout(function() {
        return cmef.handle_event_response("timer:" + _this.name, {});
      }, this.duration);
    }

    Timer.prototype.init_dom = function() {
      this.dom = $("#" + this.name + ".timer");
      if (!(this.dom.length > 0)) {
        return;
      }
      return this.update_display();
    };

    Timer.prototype.update_display = function() {
      var delta, timeout,
        _this = this;
      timeout = 1000;
      delta = this.duration - this.current;
      if (delta < 1000) {
        timeout = delta;
      }
      setTimeout(function() {
        _this.current += timeout;
        return _this.update_display();
      }, timeout);
      return this.dom.html(Math.floor(delta / 1000));
    };

    return Timer;

  })();

  Range = (function() {

    function Range(validator, name, value) {
      var list;
      this.validator = validator;
      this.name = name;
      this.value = value;
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

    function Match(validator, name, value) {
      this.validator = validator;
      this.name = name;
      this.value = value;
    }

    Match.prototype.is_valid = function(val) {
      var valid;
      valid = val.substring(0, 3) === this.value.substring(0, 3);
      this.validator.valid(this.name, valid);
      return true;
    };

    return Match;

  })();

  Validator = (function() {

    function Validator(constraints) {
      var name, _fn,
        _this = this;
      this.constraints = constraints;
      this.validity = {};
      _fn = function(name) {
        var change, comparison, constraint, dom, value;
        dom = $("[name='" + name + "']");
        constraint = _this.constraints[name];
        value = cmef.handlebars_value(constraint.value);
        comparison = _this.comparator(name, constraint.type, value);
        dom.data('validator', comparison);
        change = function(event) {
          _this.validity[name] = comparison.is_valid(event.currentTarget.value);
          if (_this.all_valid()) {
            return $('[data-enable-on-valid]').attr('disabled', false).removeClass('pure-button-disabled');
          } else {
            return $('[data-enable-on-valid]').attr('disabled', true).addClass('pure-button-disabled');
          }
        };
        dom.on('change.validate', change);
        dom.on('keyup.validate', change);
        dom.on('data:modified.validate', change);
        return dom.trigger('data:modified');
      };
      for (name in this.constraints) {
        _fn(name);
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
        default:
          return void 0;
      }
    };

    Validator.prototype.valid = function(name, val) {
      return cmef.responses["" + name + "_correct"] = val;
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
      var _this = this;
      _experiment.on_event_response.connect(function(event, response) {
        _this.event_count++;
        return _this.handle_event_response(event, response);
      });
      this.load_data();
      this.init_handlebars();
      this.initialized = true;
      this.default_methods();
      this.auto_populate('attribute', function(target, value) {
        var attr;
        attr = target.data('attribute');
        return target.attr(attr, value);
      });
      this.auto_populate('content', function(target, value) {
        return target.html(value);
      });
      this.auto_template();
      this.auto_enable();
      this.auto_input();
      this.auto_eyetracker();
      this.init_timers();
      this.init_validators();
      this.handle_event_response('ready', {});
      this.emit("show", function(response) {
        _this.mark('show');
        $(".show-on-load").show();
        if ($('body').data('eyetracker')) {
          return setTimeout(function() {
            return _this.screencap();
          }, 500);
        }
      });
    };

    CMEF.prototype.load_data = function() {
      this.current = JSON.parse(_experiment.current || '{}');
      this.dataset = JSON.parse(_experiment.dataset || '{}');
      this.datasets = JSON.parse(_experiment.datasets || '{}');
      this.subsection = JSON.parse(_experiment.subsection);
      this.experiment = JSON.parse(_experiment.experiment);
    };

    CMEF.prototype.mark = function(name) {
      return this.times[name] = (new Date()).getTime();
    };

    CMEF.prototype.default_methods = function() {
      var _this = this;
      $('[data-default="true"]').click(function(event) {
        _this.mark('submit');
        return _this.submit(_this.collect_response());
      });
    };

    CMEF.prototype.submit = function(content) {
      var cb, _i, _len, _ref;
      _ref = this.on_next;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        cb = _ref[_i];
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
      var duration, name, _ref, _ref1, _results;
      if ((_ref = this.timers) == null) {
        this.timers = [];
      }
      _ref1 = this.subsection.timers;
      _results = [];
      for (name in _ref1) {
        duration = _ref1[name];
        _results.push(this.timers.push(new Timer(name, duration)));
      }
      return _results;
    };

    CMEF.prototype.auto_input = function() {
      var target, _i, _len, _ref;
      _ref = $('[data-input]');
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        target = _ref[_i];
        this.input_selectors($(target).data('input').split(','));
      }
    };

    CMEF.prototype.auto_eyetracker = function() {
      var _this = this;
      if ($('body').data('eyetracker')) {
        this.emit('start_eyetracker');
        this.before_submit(function() {
          return _this.emit('stop_eyetracker');
        });
      }
    };

    CMEF.prototype.auto_populate = function(type, modifier) {
      var render, target, value, _i, _len, _ref;
      _ref = $("[data-" + type + "]");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        target = _ref[_i];
        target = $(target);
        value = target.data('value');
        render = target.data('render');
        if (!render) {
          render = Handlebars.compile(value);
          target.data('render', render);
        }
        this.track_loadables(modifier(target, render(this.render_data())));
      }
    };

    CMEF.prototype.render_data = function() {
      return {
        data: this.current,
        experiment: this.experiment,
        dataset: this.dataset
      };
    };

    CMEF.prototype.handlebars = function($target) {
      var html, rendered;
      html = Handlebars.compile($target.html())(this.render_data());
      rendered = $(html);
      this.track_loadables(rendered);
      return rendered;
    };

    CMEF.prototype.handlebars_value = function(value) {
      return Handlebars.compile(value)(this.render_data());
    };

    CMEF.prototype.auto_template = function() {
      var $target, rendered, target, _i, _len, _ref;
      _ref = $("[type='text/x-handlebars-template']");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        target = _ref[_i];
        $target = $(target);
        rendered = this.handlebars($target);
        rendered.insertBefore($target);
      }
    };

    CMEF.prototype.auto_enable = function() {
      var $target, change, etarg, selector, target, _i, _j, _len, _len1, _ref, _ref1;
      _ref = $("[data-enable-on]");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        target = _ref[_i];
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
      _ref1 = $("[data-enable-on-valid]");
      for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
        target = _ref1[_j];
        $target = $(target);
        $target.addClass('pure-button-disabled').attr('disabled', true);
      }
    };

    CMEF.prototype.track_loadable = function(img) {
      var _this = this;
      this.loadables++;
      return $(img).ready(function() {
        _this.loadables--;
        if (_this.loadables === 0) {
          return _this.handle_event_response('load:complete', {});
        }
      });
    };

    CMEF.prototype.track_loadables = function(html) {
      var img, _i, _len, _ref;
      if (html.is('img, svg, canvas')) {
        this.track_loadable(html);
      } else {
        _ref = $('img, svg, canvas', html);
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          img = _ref[_i];
          this.track_loadable(img);
        }
      }
    };

    CMEF.prototype.input_selectors = function(sels) {
      var f, _i, _len;
      if (!(sels instanceof Array)) {
        sels = [sels];
      }
      for (_i = 0, _len = sels.length; _i < _len; _i++) {
        f = sels[_i];
        this.iselectors.push(f);
      }
    };

    CMEF.prototype.collect_response = function() {
      var $target, cor, res, sel, target, val, _i, _j, _k, _len, _len1, _len2, _ref, _ref1, _ref2;
      res = this.responses;
      res.times = this.times;
      res.data = this.current;
      _ref = this.iselectors;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        sel = _ref[_i];
        _ref1 = $(sel);
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          target = _ref1[_j];
          $target = $(target);
          res[$target.attr('name')] = $target.val();
        }
      }
      _ref2 = $('[data-collect=true]');
      for (_k = 0, _len2 = _ref2.length; _k < _len2; _k++) {
        sel = _ref2[_k];
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
      } catch (e) {

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
      var _this = this;
      return this.emit('screen_capture', {
        name: name
      }, function(response) {
        var _base;
        (_base = _this.responses).screencap || (_base.screencap = []);
        _this.responses.screencap.push(response);
      });
    };

    CMEF.prototype.before_submit = function(cb) {
      this.on_next || (this.on_next = []);
      return this.on_next.push(cb);
    };

    CMEF.prototype.experiment = function() {
      return JSON.parse(_experiment.experiment);
    };

    CMEF.prototype.handle_event_response = function(event, response) {
      var cb, cbs, _i, _len;
      if (this.events.hasOwnProperty(event)) {
        cbs = this.events[event];
      }
      this.events[event] = [];
      if (!cbs) {
        return;
      }
      for (_i = 0, _len = cbs.length; _i < _len; _i++) {
        cb = cbs[_i];
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
      return this.add_event_callback("timer:" + event, cb);
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
        var data, i, key, keys, kidx, length, random, ret, _i, _ref, _results;
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
              _results = [];
              for (var _i = 0, _ref = context.length - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; 0 <= _ref ? _i++ : _i--){ _results.push(_i); }
              return _results;
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