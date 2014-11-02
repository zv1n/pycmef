(function() {
  if (navigator.userAgent.search(/Python/i) == -1) {
  } else {
  }
})(); 

window.onload = function () {
  var load_jquery = function (callback) {
    // Adding the script tag to the head as suggested before
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = "cmef/jquery.js";

    // Then bind the event to the callback function.
    // There are several events for cross browser compatibility.
    script.onreadystatechange = callback;
    script.onload = callback;

    // Fire the loading
    head.appendChild(script);
  };

  var init_cmef = function() {
    window.cmef = (function() {
      this.initialized = true;

      this.experiment = function() {
        console.log(this._experiment);
        return JSON.parse(this._experiment.experiment);
      };

      return this;
    })();

    $('body').show();
    cmef.experiment();
  }

  load_jquery(init_cmef);
};
