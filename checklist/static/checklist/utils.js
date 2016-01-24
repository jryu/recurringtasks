var Interval = {
  DAY: 10,
  WEEK: 20
};

function formatDate(date) {
  return [date.getFullYear(),
          date.getMonth() + 1,
          date.getDate()].join('-');
};
