function CourseList() {}

CourseList.prototype.run = function () {
    var that = this;
    that.listenDatePickEvent();
    that.listenDeleteNewsEvent();
};

CourseList.prototype.listenDatePickEvent = function () {
  var startPicker = $('#start-picker');
  var endPicker = $('#end-picker');
  var todayDate = new Date();
  var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth() + 1) + '/' + todayDate.getDate();

  options = {
    'showButtonPanel': true,
    'format': 'yyyy/mm/dd',
      'startDate': '2019/6/1',
      'endDate': todayStr,
      'language': 'zh-CN',
      'todayBtn': 'linked',
      'todayHighlight': true,
      'clearBtn': true,
      'autoclose': true
  };

  startPicker.datepicker(options);
  endPicker.datepicker(options);
};

CourseList.prototype.listenDeleteNewsEvent = function () {
  var that = this;
  var btn = $('.delete-btn');
  btn.click(function () {
    var currentBtn = $(this);
    var course_id = currentBtn.attr('data-course-id');

    xfzalert.alertConfirm({
      'text': '你确实要删除该课程吗?',
      'confirmCallback': function () {
        $.post({
          url: '/cms/delete_course/',
          data: {
            'course_id': course_id
          },
          success: function (res) {
            if (res.code === 200) {
              window.location.reload();
              window.messageBox.showSuccess(message=res.message);
            }
          }
        })
      }
    })
  })
};

$(function () {
   var courseList = new CourseList();
   courseList.run();
});