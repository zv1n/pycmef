// Generated by CoffeeScript 1.3.3
(function() {
  var CMEF;

  CMEF = (function() {

    function CMEF() {
      this.events = {};
      this.event_count = 0;
      this.times = {};
      this.mark('load');
    }

    CMEF.prototype.initialize_experiment = function() {
      var _this = this;
      _experiment.on_event_response.connect(function(event, response) {
        _this.event_count++;
        return _this.handle_event_response(event, response);
      });
      this.load_data();
      this.initialized = true;
      this.handle_event_response('ready', {});
      return this.default_methods();
    };

    CMEF.prototype.load_data = function() {
      this.data = JSON.parse(_experiment.dataset);
      this.subsection = JSON.parse(_experiment.subsection);
      return this.experiment = JSON.parse(_experiment.experiment);
    };

    CMEF.prototype.mark = function(name) {
      return this.times[name] = new Date();
    };

    CMEF.prototype.default_methods = function() {
      var _this = this;
      return $('#next[data-default=true]').click(function(event) {
        console.log('Next');
        _this.mark('next');
        return _this.emit('next', _this.collect_response());
      });
    };

    CMEF.prototype.input_selectors = function(input_selectors) {
      this.input_selectors = input_selectors;
    };

    CMEF.prototype.collect_response = function() {
      var $target, res, sel, _i, _len, _ref;
      res = {};
      res.times = this.times;
      res.data = this.data;
      _ref = this.input_selectors;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        sel = _ref[_i];
        $target = $(sel);
        res[$target.attr('name')] = $target.val();
      }
      return res;
    };

    CMEF.prototype.ready = function(cb) {
      return this.add_event_callback('ready', cb);
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

    return CMEF;

  })();

  window.cmef = new CMEF();

  window.on_python_ready = function() {
    var instantiate_cmef, load_jquery;
    load_jquery = function(callback) {
      var head, script;
      if (!window.jQuery) {
        head = document.getElementsByTagName("head")[0];
        script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "../cmef/jquery.js";
        script.onreadystatechange = callback;
        script.onload = callback;
        head.appendChild(script);
      } else {
        return callback();
      }
    };
    instantiate_cmef = function() {
      cmef.initialize_experiment();
      return cmef.emit("show", function(response) {
        cmef.mark('show');
        return $(".show-on-load").show();
      });
    };
    return load_jquery(instantiate_cmef);
  };

}).call(this);
