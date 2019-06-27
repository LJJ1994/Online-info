function News() {
    this.progressGroup = $('#progress-group');
}

News.prototype.run = function () {
    var that =this;
    // that.listenUploadfileEvent();
    that.listenQiniuFileUploadEvent();
    that.initUeditor();
    that.listenAddNewsEvent();
};

News.prototype.initUeditor = function () {
    window.ue = UE.getEditor('container', {
        'initialFrameHeight': 500,
        'serverUrl': '/ueditor/upload/'
    });
};

News.prototype.listenAddNewsEvent = function () {
  var that = this;
  var submitBtn = $('#submit-btn');
  submitBtn.click(function (event) {
      event.preventDefault();

      var btn = $(this);
      var pk = btn.attr('data-news-id');
      var url = '';

      if (pk) {
          url = '/cms/edit_news/';
      } else {
          url = '/cms/write_news/';
      }

      var title = $("input[name='title']").val();
      var category = $("select[name='category']").val();
      var desc = $("input[name='desc']").val();
      var thumbnail = $("input[name='thumbnail']").val();
      var content = window.ue.getContent();

      $.post({
          url: url,
          data: {
              'title': title,
              'desc': desc,
              'content': content,
              'thumbnail': thumbnail,
              'category': category,
              'pk': pk
          },
          success: function (res) {
              if (res.code === 200) {
                  xfzalert.alertSuccess('添加新闻成功!', function () {
                      window.location.reload();
                  })
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

News.prototype.listenUploadfileEvent = function () {
    var thumbBtn = $('#thumbnail-btn');
    thumbBtn.change(function () {
        // 这里可以上传多个图片，用file[0]选中第一个;
        var file = this.files[0];
        var formData = new FormData();
        formData.append('file', file);

        $.post({
            url: '/cms/upload_file/',
            data: formData,
            contentType: false,
            processData: false,
            success: function (res) {
                if (res.code === 200) {
                    var url = res['data']['url'];
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                } else {
                    window.messageBox.showError(res.message);
                }
            },
            error: function (res) {
                console.log(res)
            }
        })
    });
};

News.prototype.listenQiniuFileUploadEvent = function () {
  var that = this;
  var thumbnailBtn = $('#thumbnail-btn');

  thumbnailBtn.change(function () {
      var file = this.files[0];
      $.get({
          url: '/cms/qn_token/',
          success: function (res) {
              if (res.code === 200) {
                  var token = res['data']['token'];
                  // 通过时间戳 + 文件后缀名的方式生成 key
                  var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                  var putExtra = {
                      fname: key,
                      params: {},
                      // mimeType: ['image/png', 'image/jpeg', 'image/gif', 'video/x-ms-wmv', 'video/flv']
                      mimeType: null
                  };
                  var config = {
                      useCdnDomain: true,
                      retryCount: 5,
                      region: qiniu.region.z2
                  };
                  var observable = qiniu.upload(file, key, token, putExtra, config);
                  observable.subscribe({
                      'next': that.handleFileUploadProcess,
                      'error': that.handleFileUploadError,
                      'complete': that.handleFileUploadComplete
                  })
              }
          }

      })
  })
};

News.prototype.handleFileUploadProcess = function (response) {
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0) + '%';
    var progressGroup = News.progressGroup;
    progressGroup.show();

    var progressBar = $('.progress-bar');
    progressBar.css({'width': percentText});
    progressBar.text(percentText);

};

News.prototype.handleFileUploadError = function (response) {
    window.messageBox.showError(response.message);
    var progressGroup = $('#progress-group');
    progressGroup.hide();
    console.log(response.message);
};

News.prototype.handleFileUploadComplete = function (response) {
    console.log(response);
    var progressGroup = $('#progress-group');
    progressGroup.hide();

    var qiniuDomain = 'http://ptmoolpfo.bkt.clouddn.com/';
    var fileName = response.key;
    var url = qiniuDomain + fileName;
    var thumbnailInput = $('#thumbnail-form');
    thumbnailInput.val(url);
};

$(function () {
    var news = new News();
    news.run();
    News.progressGroup = $('#progress-group');
});