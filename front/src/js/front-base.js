function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
// function getCookie(name) {
//      var cookieValue = null;
//      if (document.cookie && document.cookie !== '') {
//          var cookies = document.cookie.split(';');
//          for (var i = 0; i < cookies.length; i++) {
//              var cookie = jQuery.trim(cookies[i]);
//              // Does this cookie string begin with the name we want?
//              if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                  break;
//              }
//          }
//      }
//      return cookieValue;
//  }


// 处理用户认证
function Auth() {
    var that = this;
    that.maskWrapper = $('.mask-wrapper');
    that.scrollWrapper = $('.scroll-wrapper');
    that.smsCaptchaBtn = $('.sms-captcha-btn');
}

Auth.prototype.run = function () {
    var that = this;
    that.listenShowHideEvent();
    that.listenSwitchEvent();
    that.listenSigninEvent();
    that.listenImgCaptchaCode();
    that.listenSmsCaptchaEvent();
    that.listenSignupEvent();
};

Auth.prototype.showEvent = function () {
    var that = this;
    that.maskWrapper.show('fade');
};

Auth.prototype.hideEvent = function () {
    var that = this;
    that.maskWrapper.hide();
};

Auth.prototype.listenImgCaptchaCode = function () {
  var imgCaptcha = $('.img-captcha');
  imgCaptcha.click(function () {
      imgCaptcha.attr('src', '/account/img_captcha/' + '?random=' + Math.random())
  });
};

Auth.prototype.smsSuccessSend = function () {
    var that = this;
    var count = 60;

    window.messageBox.showSuccess('短信验证码发送成功!');
    that.smsCaptchaBtn.addClass('disabled');
    that.smsCaptchaBtn.unbind('click');

    var timer = setInterval(function () {
        that.smsCaptchaBtn.text(count + 's');
        count -= 1;

        if (count <= 0) {
            clearInterval(timer);
            that.smsCaptchaBtn.removeClass('disabled');
            that.smsCaptchaBtn.text('发送验证码');
            that.listenSmsCaptchaEvent();
        }
    }, 1000)

};

Auth.prototype.listenSmsCaptchaEvent = function () {
  var that = this;
  var telephoneInput = $('.signup-group input[name="telephone"]');

  that.smsCaptchaBtn.click(function () {
      var telephoneVal = telephoneInput.val();

      if (!telephoneVal) {
          window.messageBox.show('请填写手机号！')
      }

      var data = {
          'telephone': telephoneVal
      };

      $.get({
          url: '/account/sms_captcha/',
          data: data,
          success: function (res) {
              if (res.code === 200) {
                  that.smsSuccessSend();
              } else {
                  alert(res.message);
              }
          },
          error: function () {
              window.messageBox.showError('服务器内部错误!')
          }
      })
  })
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
               window.messageBox.showError('服务器内部错误!')
           }
       })
    })

};

Auth.prototype.listenSignupEvent = function () {
    var that = this;
    var signupGroup = $('.signup-group');
    var submitBtn = signupGroup.find('.submit-btn');

    submitBtn.click(function (event) {
        event.preventDefault();
        var telephoneVal = signupGroup.find('input[name="telephone"]').val();
        var usernameVal = signupGroup.find('input[name="username"]').val();
        var password1Val = signupGroup.find('input[name="password1"]').val();
        var password2Val = signupGroup.find('input[name="password2"]').val();
        var img_captchaVal = signupGroup.find('input[name="img_captcha"]').val();
        var sms_captchaVal = signupGroup.find('input[name="sms_captcha"]').val();

        var data = {
            'telephone': telephoneVal,
            'username': usernameVal,
            'password1': password1Val,
            'password2': password2Val,
            'img_captcha': img_captchaVal,
            'sms_captcha': sms_captchaVal
        };

        $.ajax({
            url: '/account/register/',
            data: data,
            type: 'POST',
            headers: {
               'X-CSRFToken': getCookie('csrftoken')
            },
            success: function (res) {
                if (res.code === 200) {
                    window.messageBox.showSuccess('注册成功!');
                    window.location.reload();
                }else {
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
            }
        })
    })
};

// 处理hover出来的导航条
function FrontBase() {

}

FrontBase.prototype.listenAuthBoxHover = function () {
    var authBox = $('.auth-box');
    var userMoreBox = $('.user-more-box');

    authBox.hover(function () {
        userMoreBox.show();
    }, function () {
        userMoreBox.hide();
    });
};

FrontBase.prototype.run = function () {
  var that = this;
  that.listenAuthBoxHover();
  that.listenSwitchBottom();
};

// FrontBase.prototype.listenSwitchBottom = function () {
//     var infoNav = $('#nav-info');
//     var index = infoNav.find('li:first');
//     index.addClass('active');
//
//     infoNav.children().click(function () {
//         var btn = $(this);
//         var url = {
//             'info_url': '/',
//             'course_url': '/course/',
//             'payinfo_url': '/payinfo/',
//             'search_url': '/search/'
//         };
//         var currentUrl = btn.attr('href');
//         if (currentUrl === url.info_url) {
//             index.removeClass('active');
//             btn.addClass('active');
//             // btn.siblings().removeClass('active');
//         } else if(currentUrl===url.course_url) {
//             index.removeClass('active');
//             btn.addClass('active');
//             // btn.siblings().removeClass('active');
//         } else if (currentUrl===url.payinfo_url) {
//             index.removeClass('active');
//             btn.addClass('active');
//             // btn.siblings().removeClass('active');
//         } else {
//             index.removeClass('active');
//             btn.addClass('active');
//             // btn.siblings().removeClass('active');
//         }
//     })
// };

FrontBase.prototype.listenSwitchBottom = function () {
  var urlStr = location.href;
  var urlStatus = false;

  $('#nav-info a').each(function(){
      if ((urlStr + '/').indexOf($(this).attr('href')) > -1 && $(this).attr('href') !== '') {
          $(this).addClass('active');
          urlStatus = true;
      } else {
            $(this).removeClass('active')
      }
  });
  if (!urlStatus) {
      $('#nav-info a').eq(0).addClass('active');
  }
};

$(function () {
    var auth = new Auth();
    auth.run();
});

$(function () {
    var frontBase = new FrontBase();
    frontBase.run();
});

$(function () {
   if (window.template) {
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
});
