function Message() {
    var that = this;
    that.isAppend = false;
    that.wrapperHeight = 48;
    that.wrapperWidth = 300;
    that.initStyle();
    that.initElement();
    that.listenCloseEvent();
}


Message.prototype.initStyle = function () {
    var that = this;
    that.errorStyle = {
        'wrapper': {
            'background': '#f2dede',
            'color': '#993d3d'
        },
        'close': {
            'color': '#993d3d'
        }
    };

    that.successStyle = {
        'wrapper': {
            'background': '#dff0d8',
            'color': '#468874'
        },
        'close': {
            'color': '#468874'
        }
    };

    that.infoStyle = {
        'wrapper': {
            'background': '#d9edf7',
            'color': '#5bc0de'
        },
        'close': {
            'color': '#5bc0de'
        }
    };
};

Message.prototype.initElement = function () {
    var that = this;
    that.wrapper = $('<div></div>');
    that.wrapper.css({
        'overflow': 'hidden',
        'padding': '10px',
        'font-size': '14px',
        'width': '300px',
        'height': '48px',
        'position': 'fixed',
        'top': '-48px',
        'left': '50%',
        'margin-left': '-150px',
        'box-sizing': 'border-box',
        'border': '1px solid #ddd',
        'border-radius': '4px',
        'z-index': 10000,
        'line-height': '24px',
        'font-weight': 700
    });

    that.closeBtn = $('<span>x</span>');
    that.closeBtn.css({
        'display': 'inline-block',
        'float': 'right',
        'font-size': '18px',
        'cursor': 'pointer',
        'font-family': 'core_sans_n45_regular,"Avenir Next","Helvetica Neue",Helvetica,Arial,"PingFang SC","Source Han Sans SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi MicroHei",sans-serif;'
    });

    that.messageSpan = $('<span class="message-group"></span>');
    that.wrapper.append(that.messageSpan);
    that.wrapper.append(that.closeBtn);
};

Message.prototype.listenCloseEvent = function () {
    var that = this;
    that.closeBtn.click(function () {
        that.wrapper.animate({'top': -that.wrapperHeight});
    });
};

Message.prototype.show = function (message, type) {
    var that = this;
    if (!that.isAppend) {
        $(document.body).append(that.wrapper);
        that.isAppend = true;
    }

    that.messageSpan.text(message);

    if (type === 'error') {
        that.wrapper.css(that.errorStyle['wrapper']);
        that.closeBtn.css(that.errorStyle['close']);
    }else if ( type === 'info'){
        that.wrapper.css(that.infoStyle['wrapper']);
        that.closeBtn.css(that.infoStyle['close']);
    } else {
        that.wrapper.css(that.successStyle['wrapper']);
        that.closeBtn.css(that.successStyle['close']);
    }
    that.wrapper.animate({'top':0}, function () {
        setTimeout(function () {
            that.wrapper.animate({'top': -that.wrapperHeight});
        }, 5000)
    })
};

Message.prototype.showError = function (message) {
    this.show(message, 'error')
};

Message.prototype.showSuccess = function (message) {
    this.show(message, 'success')
};

Message.prototype.showInfo = function (message) {
  this.show(message, 'info')
};

window.messageBox = new Message();





















