// Generated by CoffeeScript 1.6.2
(function() {
  var CMEF;

  CMEF = (function() {
    function CMEF() {
      this.events = {};
      this.event_count = 0;
      this.times = {};
      this.iselectors = [];
      this.on_next = [];
      this.mark('load');
    }

    CMEF.prototype.initialize_experiment = function() {
      var _this = this;

      _experiment.on_event_response.connect(function(event, response) {
        _this.event_count++;
        return _this.handle_event_response(event, response);
      });
      this.load_data();
      this.handlebars();
      this.initialized = true;
      this.handle_event_response('ready', {});
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
      this.auto_eyetracker();
      this.auto_input();
    };

    CMEF.prototype.load_data = function() {
      this.current = JSON.parse(_experiment.current || '{}');
      this.data = JSON.parse(_experiment.dataset || '{}');
      this.subsection = JSON.parse(_experiment.subsection);
      this.experiment = JSON.parse(_experiment.experiment);
    };

    CMEF.prototype.mark = function(name) {
      return this.times[name] = (new Date()).getTime();
    };

    CMEF.prototype.default_methods = function() {
      var _this = this;

      $('#next[data-default="true"]').click(function(event) {
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
        this.emit('screen_capture');
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
        modifier(target, render({
          data: this.current
        }));
      }
    };

    CMEF.prototype.auto_template = function() {
      var $target, html, rendered, target, _i, _len, _ref;

      _ref = $("[type='text/x-handlebars-template']");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        target = _ref[_i];
        $target = $(target);
        html = Handlebars.compile($target.html())({
          data: this.current
        });
        rendered = $(html);
        rendered.insertBefore($target);
      }
    };

    CMEF.prototype.auto_enable = function() {
      var $target, selector, target, _i, _len, _ref;

      _ref = $("[data-enable-on]");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        target = _ref[_i];
        $target = $(target);
        $target.addClass('pure-button-disabled');
        selector = $target.data('enable-on');
        $(selector).data('enable-target', target).change(function() {
          return $target.removeClass('pure-button-disabled');
        });
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
      var $target, cor, e, res, sel, _i, _len, _ref;

      res = {};
      res.times = this.times;
      res.data = this.current;
      _ref = this.iselectors;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        sel = _ref[_i];
        $target = $(sel);
        res[$target.attr('name')] = $target.val();
      }
      try {
        cor = res.data.question.correct.toString() === res.answer.toString();
        res.correct = cor;
      } catch (_error) {
        e = _error;
      }
      return res;
    };

    CMEF.prototype.ready = function(cb) {
      return this.add_event_callback('ready', cb);
    };

    CMEF.prototype.before_submit = function(cb) {
      this.on_next || (this.on_next = []);
      return this.on_next.push(cb);
    };

    CMEF.prototype.experiment = function() {
      return JSON.parse(_experiment.experiment);
    };

    CMEF.prototype.handle_event_response = function(event, response) {
      var cb, cbs, _i, _len, _results;

      if (this.events.hasOwnProperty(event)) {
        cbs = this.events[event];
      }
      this.events[event] = [];
      if (!cbs) {
        return;
      }
      _results = [];
      for (_i = 0, _len = cbs.length; _i < _len; _i++) {
        cb = cbs[_i];
        _results.push(cb(response));
      }
      return _results;
    };

    CMEF.prototype.add_event_callback = function(event, cb) {
      if (!this.events.hasOwnProperty(event)) {
        this.events[event] = [];
      }
      if (cb instanceof Function) {
        this.events[event].push(cb);
      }
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

    CMEF.prototype.handlebars = function() {
      return Handlebars.registerHelper("each_random", function(context, options) {
        var key, keys, kidx, length, random, ret, _i, _ref, _results;

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
          while (keys.length > 0) {
            kidx = random(0, keys.length);
            key = keys.splice(kidx, 1);
            ret = ret + options.fn(context[key]);
          }
        }
        return ret;
      });
    };

    return CMEF;

  })();

  window.cmef = new CMEF();

  window.on_python_ready = function() {
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
      cmef.initialize_experiment();
      return cmef.emit("show", function(response) {
        cmef.mark('show');
        return $(".show-on-load").show();
      });
    };
    return load_js("../cmef/jquery.js", function() {
      return load_js("../cmef/handlebars.js", instantiate_cmef);
    });
  };

}).call(this);
