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

function setLastDate(pk, interval, today, lastDate) {
  var buttonElement = $('#btn-' + pk);
  var countElement = $('#cnt-' + pk);

  if (lastDate) {
    lastDate = new Date(lastDate.year, lastDate.month - 1, lastDate.day);
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
