function startTimer(duration, left_duration, display) {
  var status = 'start';
  if (duration < 0) {
    duration = left_duration;
    status = 'end'
  }
  var timer = duration, hours, minutes, seconds;
  timerFunction = function () {
      if (timer < 0) {
        display.textContent = Translations[status];
        clearInterval(timerFunction);
        return;
      }
      days = parseInt(timer / 86400, 10);
      hours = parseInt((timer - (days * 86400)) / 3600, 10);
      minutes = parseInt(((timer - (days * 86400))-hours*3600) / 60, 10);
      seconds = parseInt(((timer - (days * 86400))-hours*3600) % 60, 10);

      days = days < 0 ? "" : days;
      hours = hours < 10 ? "0" + hours : hours;
      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      display.textContent = parseInt(hours) > 0 || parseInt(days) > 0 ? days + ' ' + hours + ":" + minutes + ":" + seconds : minutes + ":" + seconds;
      timer--;
  }
  setInterval(timerFunction, 1000);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

jQuery(window).load(function() {
  var time_left = parseInt($('#time-left-sec').text());
  var vote_left = parseInt($('#vote-left-sec').text());
  var display = document.querySelector('#time-left');
  if(!isNaN(time_left)) {
    startTimer(time_left, vote_left, display);
  }
});
$(document).ready(function() {
  $('.vote-button').on('click', function(e) {
    $('.vote-button').attr('disabled','disabled');
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      },
      error: function(xhr, textStatus, error) {
        if (error == "Conflict") {
          $('.project-alert').addClass('alert-danger');
          $('.project-vote-message').text($.parseJSON(xhr.responseText).message);
        } else if (error == "Not Found") {
          $('.project-alert').addClass('alert-danger');
          $('.project-vote-message').text($.parseJSON(xhr.responseText).message);
        } else if (error == "Bad Request") {
          $('.project-alert').addClass('alert-warning');
          $('.project-vote-message').text($.parseJSON(xhr.responseText).message);
        } else if (error == "Unauthorized") {
          $('.project-alert').addClass('alert-danger');
          $('.project-vote-message').text(Translations.login_error);
        } else {
          $('.project-alert').addClass('alert-danger');
          $('.project-vote-message').text(Translations.unknown_error);
        }
        $('.project-alert').toggle('hidden')
      }
    });
    $.ajax({
      "type": "POST",
      "dataType": "json",
      "url": "/api/projects/" + $('.project-id').val() + "/vote/",
      "data": {},
      "beforeSend": function(xhr, settings) {
        $.ajaxSettings.beforeSend(xhr, settings);
      },
      "success": function(result) {
        $('.project-alert').addClass('alert-success');
        $('.project-vote-message').text(result.message);
        $('.project-alert').toggle('hidden')
      }
    });
    return false;
  });
});
