function  Index() {
    this.page = 2;

    template.defaults.imports.timeSince = function (value) {
        // art_template模板过滤器，格式化时间
        var date = new Date(value);
        var datets = date.getTime();
        var nowts = (new Date()).getTime();
        var timestamp = (nowts - datets) / 1000; //得到两者相差的时间戳，单位为秒

        if (timestamp < 60) {

            return "刚刚"
        } else if (timestamp >= 60 && timestamp < 60*60) {
            var minutes = parseInt(timestamp/60);

            return minutes + '分钟前'
        } else if (timestamp >= 60*60 && timestamp < 60*60*24) {
            var hours = parseInt(timestamp/60/60);

            return hours + '小时前'
        } else if (timestamp >= 60*60*24 && timestamp < 60*60*24*30) {
            var days = parseInt(timestamp/60/60/24);
            return days + '天前'
        } else {
            var year = date.getFullYear();
            var month = date.getMonth();
            var day = date.getDay();
            var hour = date.getHours();
            var minute = date.getMinutes();

            return year + '/' + month + '/' + day + ' ' + hour + ':' + minute
        }
    };
}

Index.prototype.listenLoadMoreEvent = function () {
  var that = this;
  var loadMoreBtn = $('#load-more');

  loadMoreBtn.click(function () {
      var page = that.page;

      $.get({
          url: '/news/news_list/',
          data: {
              'p': page
          },
          success: function (res) {
              if (res.code===200) {
                  if (res['data'].length>0) {
                      var newses = res['data'];
                      var tpl = template("tpl", {"newses": newses});
                      var ulELem = $('.list-inner-gropu');
                      ulELem.append(tpl);

                      that.page += 1;
                  } else {
                      loadMoreBtn.hide();
                  }
              } else {
                  window.messageBox.showError(res.message);
              }
          },
          error: function (res) {
              window.messageBox.showError(res.message);
          }
      })
  })
};

Index.prototype.run = function () {
    var that = this;
    that.listenLoadMoreEvent();
};

$(function () {
   var index = new Index();
   index.run();
});
