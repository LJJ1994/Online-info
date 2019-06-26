function NewsList() {

}

NewsList.prototype.listenCommentSubitEvent = function () {
  var that = this;
  var submitBtn = $('.submit-btn');
  var textarea = $('textarea[name="comment"]');

  submitBtn.click(function () {
      var news_id = submitBtn.attr('data-news-id');
      var content = textarea.val();

      $.post({
         url: '/news/news_comment/',
         data: {
            'news_id': news_id,
            'content': content
         },
         success: function (res) {
            if (res.code === 200) {
               var comment = res['data'];
               var tpl = template('comment-item', {
                  'comment': comment
               });
               var commentList = $('.comment-list');
               commentList.prepend(tpl);
               window.messageBox.showSuccess('评论发表成功!');
               textarea.val("");
            } else {
               window.messageBox.showError(message=res.message);
            }
         },
         error: function (res) {
            window.messageBox.showError(message='服务器内部错误!');
         }
      })
  })
};

NewsList.prototype.run = function () {
   var that = this;
   that.listenCommentSubitEvent();
};

$(function () {
   var newsList = new NewsList();
   newsList.run();
});