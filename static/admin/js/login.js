
$(function () {
    $(".login_btn").click(function (event) {
        event.preventDefault();
        var email_input = $("input[name=email]");
        var password_input = $("input[name='password']");

        var remember_input = $("input[name='remember']");

        var email = email_input.val();
        var password = password_input.val();
        var remember = remember_input.checked ? 1 : 0;

        zlajax.post({
            'url': "/admin/login/",
            'data': {
                'email': email,
                'password': password,
                'remember': remember,

            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast(data['message']);
                    setTimeout(function () {
                        window.location = '/admin/';
                    },2000);
                } else {
                    zlalert.alertInfoToast(data['message']);
                    console.log(data['message']);
                    if(data['message']=='邮箱或者密码错误' || data['message']=='请输入正确格式的密码')
                    {
                        $('#captcha-img').trigger('click');
                    }
                }
            },
            'fail':function (error) {
                    zlalert.alertNetworkError();
                }

        })
    })
});