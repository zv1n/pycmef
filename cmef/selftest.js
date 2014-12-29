// Generated by CoffeeScript 1.6.2
(function() {
  var SelfText,
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  SelfText = (function() {
    function SelfText() {
      var Exception;

      try {
        this.check_cmef();
      } catch (_error) {
        Exception = _error;
        this.fail();
      }
      this.validated();
      this.gtg = true;
    }

    SelfText.prototype.validated = function() {
      $(".show-on-valid").show();
      $("#begin").click(function(event) {
        var condition, participant;

        participant = $('#participant_id').val();
        condition = $('#condition').val();
        if (!(participant > 0)) {
          console.log('Invalid Participant');
          return;
        }
        if (cmef.experiment.conditions instanceof Array) {
          if (__indexOf.call(cmef.experiment.conditions, condition) < 0) {
            console.log('Invalid Condition');
            return;
          }
        }
        return cmef.emit('start', {
          participant: participant,
          condition: condition
        });
      });
      return cmef.emit('start', {
        participant: "1337",
        condition: "A"
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
