function assertButtonIsChecked(assert) {
  assert.ok($('#btn-1').hasClass('ui-icon-check'), 'Checked!');
};

function assertButtonIsNotCheckedYet(assert) {
  assert.ok($('#btn-1').hasClass('ui-icon-plus'), 'Not checked yet.');
  assert.ok($('#cnt-1').hasClass('ui-body-b'), 'Black counter label');
};

function assertCounterIsHidden(assert) {
  assert.ok($('#cnt-1').is(':hidden'), 'Counter is hidden.');
};

function assertCounterLabel(assert, text) {
  assert.ok($('#cnt-1').is(':visible'), 'Counter is visible.');
  assert.equal($('#cnt-1').text(), text, 'Counter label text');
};

function beforeEach() {
  this.today = new Date(2016, 0, 12);
  $('<a id="btn-1"><span id="cnt-1"></span></a>')
    .appendTo('#qunit-fixture');

  $.ajax = $.proxy(function(path, options) {
    this.ajaxPath = path;

    return {
      always: function() {},
      done: function() {},
      fail: function() {}
    }
  }, this);

  this.assertCheckRequest = function(assert) {
    assert.equal(this.ajaxPath, '/check/', 'Requests check on click');
  }

  this.assertUncheckRequest = function(assert) {
    assert.equal(this.ajaxPath, '/uncheck/', 'Requests uncheck on click');
  }
};

QUnit.module('setLastDate() - Daily Task', {
  beforeEach: beforeEach
});

QUnit.test("Same day", function(assert) {
  setLastDate(1, Interval.DAY, this.today, {year: 2016, month: 1, day: 12});

  assertButtonIsChecked(assert);
  assertCounterIsHidden(assert);

  toggle(1, Interval.DAY, this.today);

  this.assertUncheckRequest(assert);
});

QUnit.test("Yesterday", function(assert) {
  setLastDate(1, Interval.DAY, this.today, {year: 2016, month: 1, day: 11});

  assertButtonIsNotCheckedYet(assert);
  assertCounterLabel(assert, 'Yesterday');

  toggle(1, Interval.DAY, this.today);

  this.assertCheckRequest(assert);
});

QUnit.test("2 days ago", function(assert) {
  setLastDate(1, Interval.DAY, this.today, {year: 2016, month: 1, day: 10});

  assertButtonIsNotCheckedYet(assert);
  assertCounterLabel(assert, '2 days');

  toggle(1, Interval.DAY, this.today);

  this.assertCheckRequest(assert);
});


QUnit.module('setLastDate() - Weekly Task', {
  beforeEach: beforeEach
});

QUnit.test("Same day", function(assert) {
  setLastDate(1, Interval.WEEK, this.today, {year: 2016, month: 1, day: 12});

  assertButtonIsChecked(assert);
  assertCounterIsHidden(assert);

  toggle(1, Interval.WEEK, this.today);

  this.assertUncheckRequest(assert);
});

QUnit.test("Yesterday", function(assert) {
  setLastDate(1, Interval.WEEK, this.today, {year: 2016, month: 1, day: 11});

  assertButtonIsChecked(assert);
  assertCounterLabel(assert, 'Yesterday');
  assert.ok($('#cnt-1').hasClass('ui-body-a'), 'White counter label');

  toggle(1, Interval.WEEK, this.today);

  this.assertCheckRequest(assert);
});

QUnit.test("2 days ago", function(assert) {
  setLastDate(1, Interval.WEEK, this.today, {year: 2016, month: 1, day: 10});

  assertButtonIsChecked(assert);
  assertCounterLabel(assert, '2 days');
  assert.ok($('#cnt-1').hasClass('ui-body-a'), 'White counter label');

  toggle(1, Interval.WEEK, this.today);

  this.assertCheckRequest(assert);
});

QUnit.test("6 days ago", function(assert) {
  setLastDate(1, Interval.WEEK, this.today, {year: 2016, month: 1, day: 6});

  assertButtonIsChecked(assert);
  assertCounterLabel(assert, '6 days');
  assert.ok($('#cnt-1').hasClass('ui-body-a'), 'White counter label');

  toggle(1, Interval.WEEK, this.today);

  this.assertCheckRequest(assert);
});

QUnit.test("7 days ago", function(assert) {
  setLastDate(1, Interval.WEEK, this.today, {year: 2016, month: 1, day: 5});

  assertButtonIsNotCheckedYet(assert);
  assertCounterLabel(assert, 'Last week');

  toggle(1, Interval.WEEK, this.today);

  this.assertCheckRequest(assert);
});

QUnit.test("14 days ago", function(assert) {
  setLastDate(1, Interval.WEEK, this.today, {year: 2015, month: 12, day: 29});

  assertButtonIsNotCheckedYet(assert);
  assertCounterLabel(assert, '2 weeks');

  toggle(1, Interval.WEEK, this.today);

  this.assertCheckRequest(assert);
});
