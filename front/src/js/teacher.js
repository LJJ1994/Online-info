function AddTeacher() {
    this.progressGroup = $('#progress-group');
}

AddTeacher.prototype.run = function () {
    var that =this;
    // that.listenUploadfileEvent();
    that.listenQiniuFileUploadEvent();
    that.initUeditor();
    that.listenAddNewsEvent();
    that.listenDeleteTeacherEvent();
};

AddTeacher.prototype.initUeditor = function () {
    window.ue = UE.getEditor('profile-editor', {
        'initialFrameHeight': 500,
        'serverUrl': '/ueditor/upload/'
    });
};

AddTeacher.prototype.listenAddNewsEvent = function () {
  var that = this;
  var submitBtn = $('#teacher-submit-btn');
  submitBtn.click(function (event) {
      event.preventDefault();

      var btn = $(this);
      var pk = btn.attr('data-teacher-id');
      console.log('pk的值:', pk);
      var url = '';

      if (pk) {
          url = '/cms/edit_course_teacher/';
      } else {
          url = '/cms/add_course_teacher/';
      }

      var username = $("input[name='username']").val();
      var jobtitle = $("input[name='jobtitle']").val();
      var avatar_url = $("input[name='thumbnail']").val();
      var profile = window.ue.getContent();
      console.log(username, jobtitle, avatar_url, profile);

      $.post({
          url: url,
          data: {
              'username': username,
              'jobtitle': jobtitle,
              'avatar_url': avatar_url,
              'profile': profile,
              'pk': pk
          },
          success: function (res) {
              if (res.code === 200) {
                  xfzalert.alertSuccess('添加讲师成功!', function () {
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

AddTeacher.prototype.listenDeleteTeacherEvent = function () {
  var that = this;
  var btn = $('.delete-btn');
  btn.click(function (event) {
    event.preventDefault();
    var currentBtn = $(this);
    var teacher_id = currentBtn.attr('data-teacher-id');

    xfzalert.alertConfirm({
      'text': '你确实要删除该讲师?',
      'confirmCallback': function () {
        $.post({
          url: '/cms/delete_course_teacher/',
          data: {
            'teacher_id': teacher_id
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

AddTeacher.prototype.listenUploadfileEvent = function () {
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

AddTeacher.prototype.listenQiniuFileUploadEvent = function () {
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

AddTeacher.prototype.handleFileUploadProcess = function (response) {
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0) + '%';
    var progressGroup = AddTeacher.progressGroup;
    progressGroup.show();

    var progressBar = $('.progress-bar');
    progressBar.css({'width': percentText});
    progressBar.text(percentText);

};

AddTeacher.prototype.handleFileUploadError = function (response) {
    window.messageBox.showError(response.message);
    var progressGroup = $('#progress-group');
    progressGroup.hide();
    console.log(response.message);
};

AddTeacher.prototype.handleFileUploadComplete = function (response) {
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
    var addTeacher = new AddTeacher();
    addTeacher.run();
    AddTeacher.progressGroup = $('#progress-group');
});