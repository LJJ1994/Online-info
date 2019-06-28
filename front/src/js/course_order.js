$(function () {
    //这里的思路是: 当文档加载时，点击去支付按钮；
    // 通过ajax向后端拿到paysapi的key数据，填充到隐藏的表单数据
    // 再通过form-btn向paysapi服务器发送请求, 因为key只能在后端，不能放在前端

    var submitBtn = $('#submit-btn');
    submitBtn.click(function (e) {
        e.preventDefault();

        var goodsname = $('input[name="goodsname"]').val();
        var istype = $('input[name="istype"]:checked').val();
        var notify_url = $('input[name="notify_url"]').val();
        var orderid = $('input[name="orderid"]').val();
        var price = $('input[name="price"]').val();
        var return_url = $('input[name="return_url"]').val();

        $.post({
            url: '/course/course_order_key/',
            data: {
                'goodsname': goodsname,
                'istype': istype,
                'notify_url': notify_url,
                'orderid':orderid,
                'price': price,
                'return_url': return_url
            },
            success: function (res) {
                if (res.code === 200) {
                    var key = res['data']['key'];
                    var keyInput = $('input[name="key"]');
                    keyInput.val(key);

                    $('#form-btn').submit();
                }
            }
        })
        });
});