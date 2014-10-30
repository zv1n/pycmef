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
    cmef.initialized = true;

    cmef.prototype.experiment = function() {
      alert(this._experiment);
      return JSON.parse(this._experiment);
    }

    alert('alibaba~!');
    $('body').show();
  }

  load_jquery(init_cmef);
};
