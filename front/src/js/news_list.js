function CMSNewsList() {}

CMSNewsList.prototype.run = function () {
    var that = this;
    that.listenDatePickEvent();
    that.listenDeleteNewsEvent();
};

CMSNewsList.prototype.listenDatePickEvent = function () {
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

CMSNewsList.prototype.listenDeleteNewsEvent = function () {
  var that = this;
  var btn = $('.delete-btn');
  btn.click(function () {
    var currentBtn = $(this);
    var news_id = currentBtn.attr('data-news-id');

    xfzalert.alertConfirm({
      'text': '你确实要删除这篇新闻吗?',
      'confirmCallback': function () {
        $.post({
          url: '/cms/delete_news/',
          data: {
            'news_id': news_id
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
   var cmsNews = new CMSNewsList();
   cmsNews.run();
});