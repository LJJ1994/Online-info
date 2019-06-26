// $(function () {
//     $('#btn').click(function () {
//         $('.mask-wrapper').show(500, 'swing');
//     });
//
//     $('.close-btn').click(function () {
//         $('.mask-wrapper').hide(500);
//     });
//
//     $('.switch').click(function () {
//         var currentLeft = $('.scroll-wrapper').css('left');
//         currentLeft = parseInt(currentLeft);
//
//         if (currentLeft < 0) {
//             $('.scroll-wrapper').animate({'left': '0'});
//         }else {
//             $('.scroll-wrapper').animate({'left': '-400px'});
//         }
//     });
// });

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function Auth() {
    var that = this;
    that.maskWrapper = $('.mask-wrapper');
    that.scrollWrapper = $('.scroll-wrapper');
}

Auth.prototype.run = function () {
    var that = this;
    that.listenShowHideEvent();
    that.listenSwitchEvent();
    that.listenSigninEvent();
};

Auth.prototype.showEvent = function () {
    var that = this;
    that.maskWrapper.show('fade');
};

Auth.prototype.hideEvent = function () {
    var that = this;
    that.maskWrapper.hide();
};

Auth.prototype.listenShowHideEvent = function () {
    var that = this;
    var signinBtn = $('.signin-btn');
    var signupBtn = $('.signup-btn');
    var closeBtn = $('.close-btn');

    signinBtn.click(function () {
        that.showEvent();
        that.scrollWrapper.css({'left':0});
    });
    
    signupBtn.click(function () {
        that.showEvent();
        that.scrollWrapper.css({'left':'-400px'});
    });
    
    closeBtn.click(function () {
        that.hideEvent();
    })
};

Auth.prototype.listenSwitchEvent = function () {
    var that = this;
    var switchBtn = $('.switch');

    switchBtn.click(function () {
        var currentLength = that.scrollWrapper.css('left');
        currentLength = parseInt(currentLength);

        if (currentLength < 0) {
            that.scrollWrapper.animate({'left':0});
        } else {
            that.scrollWrapper.animate({'left': '-400px'});
        }
    })
};

Auth.prototype.listenSigninEvent = function () {
    var that = this;
    var signinGroup = $('.signin-group');
    var telephoneInput = signinGroup.find("input[name='telephone']");
    var passwordInput = signinGroup.find("input[name='password']");
    var rememberInput = signinGroup.find("input[name='remember']");

    var signinBtn = signinGroup.find('.submit-btn');

    signinBtn.click(function () {
       var telephoneVal = telephoneInput.val();
       var passwordVal = passwordInput.val();
       var rememberVal = rememberInput.prop('checked');

       var data =  {
           'telephone': telephoneVal,
           'password': passwordVal,
           'remember': rememberVal ? 1 : 0
        };
       //  var data_json = JSON.stringify(data);
       // console.log(data_json)

       $.ajax({
           url: '/account/login/',
           type: 'POST',
           data: data,
           headers: {
               'X-CSRFToken': getCookie('csrftoken')
           },
           success: function (res) {
               if (res.code === 200) {
                   that.hideEvent();
                   window.location.reload();
               } else {
                   var messageObj = res['message'];
                   if (typeof messagObje === 'string' || messageObj.constructor === String) {
                       window.messageBox.show(messageObj);
                   } else {
                       for (var key in messageObj) {
                           var messages = messageObj[key];
                           var message = messages[0];
                           window.messageBox.show(message);
                       }
                   }
               }
           },
           error: function () {
               alert('请求参数或类型错误，请重新检查ajax代码！')
           }
       })

        // xfzajax.post({
        //     'url': '/account/login/',
        //     'data:': data,
        //     'success': function (res) {
        //         if (res.code === 200) {
        //             console.log(res)
        //         } else {
        //             console.log(res)
        //         }
        //     },
        //     'fail': function (res) {
        //         console.log(res)
        //     }
        // })
        })

};

$(function () {
    var auth = new Auth();
    auth.run();
});




















