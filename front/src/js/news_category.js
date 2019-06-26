function  NewsCategory() {

}

NewsCategory.prototype.run = function () {
    var that = this;
    that.listenAddCategoryEvent();
    that.listenEditNewsCategoryEvent();
    that.listenDeleteNewsCategoryEvent();
};

NewsCategory.prototype.listenAddCategoryEvent = function () {
  var addBtn = $('#add-btn');
  addBtn.click(function () {
      xfzalert.alertOneInput({
          'title': '添加新闻分类',
          'placeholder': '请输入要添加的新闻分类',
            'confirmCallback': function (inputVal) {
                $.post({
                    url: '/cms/add_news_category/',
                    data: {
                        'name': inputVal
                    },
                    success: function (res) {
                        if (res.code === 200) {
                            window.location.reload();
                        } else {
                            xfzalert.close();
                            window.messageBox.showError(res.message);
                        }
                    },
                    error: function (res) {
                        console.log(res.message);
                    }
                })
            }
      })
  })
};


NewsCategory.prototype.listenEditNewsCategoryEvent = function () {
    var editBtn = $('.edit-btn');
    editBtn.click(function () {// 这里的this指向调用click事件的按钮edit-btn, 通过它获取它的父元素的父元素
        var current = $(this);
        var tr = current.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');

        xfzalert.alertOneInput({
            'title': '编辑该分类',
            'value': name,
            'confirmCallback': function (inputVal) {
                $.post({
                    url: '/cms/edit_news_category/',
                    data: {
                        'pk': pk,
                        'name': inputVal
                    },
                    success: function (res) {
                        if (res.code === 200) {
                            console.log(res);
                            window.location.reload();
                        } else {
                            xfzalert.close();
                            window.messageBox.showError(res.message);
                        }
                    },
                    error: function (res) {
                        console.log(res.message);
                    }
                })
            }
        })
    })
};


NewsCategory.prototype.listenDeleteNewsCategoryEvent = function() {
    var that = this;
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var current = $(this);
        var tr = current.parent().parent();
        var pk = tr.attr('data-pk');

        xfzalert.alertConfirm({
            'title': '你确定要删除该分类吗?',
            'confirmCallback': function () {
                $.post({
                    url: '/cms/delete_news_category/',
                    data: {
                        'pk': pk
                    },
                    success: function (res) {
                        if (res.code === 200) {
                            window.location.reload();
                        } else {
                            xfzalert.close();
                            window.messageBox.showError(res.message);
                        }
                    },
                    error: function (res) {
                        console.log(res.messages)
                    }
                })
            }
        })
    });
};

$(function () {
    var newCategory = new NewsCategory();
    newCategory.run();
});