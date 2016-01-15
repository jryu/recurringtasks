var Interval = {
  DAY: 10,
  WEEK: 20};

function getDailyLabel(days) {
  if (days == 1) {
    return 'Yesterday';
  } else {
    return days + ' days';
  }
};

function getWeeklyLabel(weeks) {
  if (weeks == 1) {
    return 'Last week';
  } else {
    return weeks + ' weeks';
  }
};

function getCountLabel(days, interval) {
  switch (interval) {
    case Interval.DAY:
      return getDailyLabel(days);
    case Interval.WEEK:
      if (days < 7) {
        return getDailyLabel(days);
      } else {
        return getWeeklyLabel(Math.floor(days / 7));
      }
  }
};

function shouldCheck(days, interval) {
  switch (interval) {
    case Interval.DAY:
      return days < 1;
    case Interval.WEEK:
      return days < 7;
  }
};

function setChecked(shouldCheck, buttonElement, countElement) {
  if (shouldCheck) {
    buttonElement.buttonMarkup({icon: 'check'});
    countElement.addClass('ui-body-a');
    countElement.removeClass('ui-body-b');
  } else {
    buttonElement.buttonMarkup({icon: 'plus'});
    countElement.removeClass('ui-body-a');
    countElement.addClass('ui-body-b');
  }
};

function formatDate(date) {
  return [date.getMonth() + 1,
          date.getDate(),
          date.getFullYear()].join('/');
};

function createDate(y, m, d) {
  return new Date(y, m - 1, d);
};

function setLastDate(pk, interval, today, lastDate) {
  var buttonElement = $('#btn-' + pk);
  var countElement = $('#cnt-' + pk);

  if (lastDate) {
    lastDate = createDate(lastDate.year, lastDate.month, lastDate.day);
    var days = (today - lastDate) / (1000 * 60 * 60 * 24);

    // buttonElement
    setChecked(shouldCheck(days, interval), buttonElement, countElement);

    // countElement
    if (lastDate < today) {
      countElement.text(getCountLabel(days, interval));
      countElement.show();
    } else {
      countElement.hide();
    }
  } else {
    setChecked(false, buttonElement, countElement);

    countElement.text('New');
    countElement.show();
  }
};

function toggle(pk, interval, today) {
  $.mobile.loading('show');

  var isUncheck =
      $('#btn-' + pk).hasClass('ui-icon-check') &&
      $('#cnt-' + pk).is(':hidden');

  var request = $.ajax(
    isUncheck ? '/uncheck/' : '/check/',
    {
      method: 'POST',
      data: {
        date: formatDate(today),
        task: pk,
      }
    });

  request.always(function() {
    $.mobile.loading('hide');
  });

  request.done(function(response) {
    if (isUncheck && response.last_date == null) {
      // The task no longer has any check.
      setLastDate(pk, interval, today, null);
    } else {
      setLastDate(pk, interval, today, response);
    }
  });

  request.fail(function(response) {
    $('#errorMessage p').text(
        $.map(response.responseJSON, function(val, key) { return val; })
            .join(' '));
    $('#errorMessage').popup('open');
  });
  return false;
};
