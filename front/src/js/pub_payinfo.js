function PubPayinfo() {

}

PubPayinfo.prototype.run = function () {
    var that = this;
    that.listenUploadfileEvent();
    that.listenAddPayinfoEvent();
    that.listenDeletePayinfoEvent();
    that.listenDatePickEvent();
};

PubPayinfo.prototype.listenUploadfileEvent = function () {
    // 上传付费资讯文件
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

PubPayinfo.prototype.listenAddPayinfoEvent = function () {
    // 添加付费资讯文章
  var that = this;
  var submitBtn = $('#submit-btn');
  submitBtn.click(function (event) {
      event.preventDefault();
      var btn = $(this);
      var pk = btn.attr('data-payinfo-id');
      var url = '';

      if (pk) {
          url = '/cms/edit_payinfo/';
      } else {
          url = '/cms/write_payinfo/';
      }

      var title = $("input[name='title']").val();
      var price = $("input[name='price']").val();
      var file_path = $("input[name='thumbnail']").val();
      var profile = $("input[name='profile']").val();

      $.post({
          url: url,
          data: {
              'title': title,
              'price': price,
              'file_path': file_path,
              'profile': profile,
              'pk': pk
          },
          success: function (res) {
              if (res.code === 200) {
                  xfzalert.alertSuccess('添加或编辑付费资讯文章成功!', function () {
                      // window.location.reload();
                      console.log('好的')
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

PubPayinfo.prototype.listenDeletePayinfoEvent = function () {
  var that = this;
  var btn = $('.delete-btn');
  btn.click(function () {
    var currentBtn = $(this);
    var payinfo_id = currentBtn.attr('data-payinfo-id');

    xfzalert.alertConfirm({
      'text': '你确实要删除这篇资讯吗?',
      'confirmCallback': function () {
        $.post({
          url: '/cms/delete_payinfo/',
          data: {
            'payinfo_id': payinfo_id
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


PubPayinfo.prototype.listenDatePickEvent = function () {
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


$(function () {
   var pubPayinfo = new PubPayinfo();
   pubPayinfo.run();
});