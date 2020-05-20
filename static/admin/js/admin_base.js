//JavaScript代码区域
layui.use(['element', 'layer']);



document.addEventListener("click", operateTimeOut);
var session = '${session}';
var second = 0;
startit();

//开始计时 
function startit() {
    second++;
    setTimeout("startit()", 1000); //每隔1秒（1000毫秒）递归调用一次 
}

function operateTimeOut() { //    startit();
    //session超时自动退出
    if (session == null || second > 60 * 60 * 10) {
        document.removeEventListener("click", operateTimeOut);
        zlajax.get({
            'url': '/logout_ajax/',
            'data': {
                'flag': '1'
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    layer.alert("登录超时,请重新登录", {
                        icon: 3,
                        title: '提示',
                        closeBtn: 0,
                        skin: 'layui-layer-molv'
                    }, function () {
                        location.href = "/login/";
                    });
                } else {
                    zlalert.alertInfo(data['message']);
                }
            }
        });
        return;
    }
    second = 0;
}