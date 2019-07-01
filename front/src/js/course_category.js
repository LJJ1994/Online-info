function  CourseCategory() {

}

CourseCategory.prototype.run = function () {
    var that = this;
    that.listenAddCategoryEvent();
    that.listenEditNewsCategoryEvent();
    that.listenDeleteNewsCategoryEvent();
};

CourseCategory.prototype.listenAddCategoryEvent = function () {
  var addBtn = $('#add-btn');
  addBtn.click(function () {
      xfzalert.alertOneInput({
          'title': '添加课程分类',
          'placeholder': '请输入要添加的课程分类',
            'confirmCallback': function (inputVal) {
                $.post({
                    url: '/cms/add_course_category/',
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


CourseCategory.prototype.listenEditNewsCategoryEvent = function () {
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
                    url: '/cms/edit_course_category/',
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


CourseCategory.prototype.listenDeleteNewsCategoryEvent = function() {
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
                    url: '/cms/delete_course_category/',
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
    var courseCategory = new CourseCategory();
    courseCategory.run();
});