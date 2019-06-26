function  Index() {
    var that = this;
    that.page = 2;
    that.category_id = 0;
    that.loadMoreBtn = $('#load-more');
}

Index.prototype.listenLoadMoreEvent = function () {
  var that = this;
  var loadMoreBtn = $('#load-more');

  loadMoreBtn.click(function () {
      $.get({
          url: '/news/news_list/',
          data: {
              'p': that.page,
              'category_id': that.category_id
          },
          success: function (res) {
              if (res.code===200) {
                  if (res['data'].length>0) {
                      var newses = res['data'];
                      console.log(newses);
                      for (var i=0;i<newses.length;i++) {
                          console.log(newses[i].id)
                      }
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

Index.prototype.listenSwitchCategoryEvent = function () {
  var that = this;
  var listTab = $('.list-tab');
  listTab.children().click(function (event) {
      var li = $(this); //这里的this表示当前选中的li标签
      var category_id = li.attr('data-category');
      var page = 1;
      $.get({
          url: '/news/news_list/',
          data: {
              'category_id': category_id,
              'p': page
          },
          success: function (res) {
              if (res.code === 200) {
                  var newses = res['data'];
                  var tpl = template('tpl', {'newses': newses});
                  var newsListGroup = $('.list-inner-gropu');
                  // 当切换到某个li标签，先将里面的新闻清空，再添加
                  newsListGroup.empty();
                  newsListGroup.append(tpl);
                  that.page = 2;
                  that.category_id = category_id;
                  li.addClass('active').siblings().removeClass('active');
                  that.loadMoreBtn.show();
              }
          }
      })
  })
};

Index.prototype.run = function () {
    var that = this;
    that.listenLoadMoreEvent();
    that.listenSwitchCategoryEvent();
};

$(function () {
   var index = new Index();
   index.run();
});
