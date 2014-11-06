// Generated by CoffeeScript 1.3.3
(function() {
  var SelfText;

  SelfText = (function() {

    function SelfText() {
      try {
        this.check_cmef();
      } catch (Exception) {
        this.fail();
      }
      this.validated();
      this.gtg = true;
    }

    SelfText.prototype.validated = function() {
      $(".show-on-valid").show();
      return $("#begin").click(function(event) {
        if (!($('#pid').val() > 0)) {
          return;
        }
        return cmef.emit('start', function(response) {});
      });
    };

    SelfText.prototype.fail = function() {
      return $(".show-on-failure").show();
    };

    SelfText.prototype.check_cmef = function() {
      if (!cmef.initialized) {
        throw new Exception('CMEF failed to initialized.');
      }
    };

    return SelfText;

  })();

  cmef.ready(function() {
    return window.selftest = new SelfText();
  });

}).call(this);
