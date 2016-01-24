function BarChart(dailyChartSelector, dailyContentSelector,
    weeklyChartSelector, weeklyContentSelector, intervalValueSelector) {

  this.chartDaily_ =
      new google.visualization.ColumnChart($(dailyChartSelector).get(0));

  this.chartWeekly_ =
      new google.visualization.ColumnChart($(weeklyChartSelector).get(0));

  this.dailyContentSelector_ = dailyContentSelector;
  this.weeklyContentSelector_ = weeklyContentSelector;
  this.intervalValueSelector_ = intervalValueSelector;

  this.options_ = {
    legend: { position: 'top', maxLines: 3 },
    bar: { groupWidth: '80%' },
    isStacked: true,
    vAxis: { minValue: 0, maxValue: 4 }
  };
};

BarChart.prototype.getData = function() {
  $.mobile.loading('show');

  var today = new Date();
  today.setHours(0, 0, 0, 0);

  var request = $.ajax(
    '/trends/ajax/',
    {
      method: 'POST',
      data: {
        date: formatDate(today),
        interval: $(this.intervalValueSelector_).val(),
      }
    });

  request.always(function() {
    $.mobile.loading('hide');
  });

  request.done($.proxy(function(response) {
    if (response.interval ==
        $(this.intervalValueSelector_).val()) {
      this.dataDaily_ = response[Interval.DAY];
      this.dataWeekly_ = response[Interval.WEEK];
      this.draw();
    }
  }, this));
};

BarChart.prototype.draw = function() {
  if (this.dataDaily_) {
    $(this.dailyContentSelector_).show();

    this.chartDaily_.draw(
        new google.visualization.arrayToDataTable(this.dataDaily_),
        this.options_);
  } else {
    $(this.dailyContentSelector_).hide();
  }

  if (this.dataWeekly_) {
    $(this.weeklyContentSelector_).show();

    this.chartWeekly_.draw(
        new google.visualization.arrayToDataTable(this.dataWeekly_),
        this.options_);
  } else {
    $(this.weeklyContentSelector_).hide();
  }
};
