layui.use(['table', 'jquery', 'util', 'layer', 'form', 'code'], function () {
    var table = layui.table;
    var $ = layui.$;
    util = layui.util;


    table.render({
        elem: '#test'
        , height: 'full-200'
        , url: '/admin/iport/'
        , method: 'post'
        , toolbar: '#toolbarDemo'
        , cellMinWidth: 80
        , limits: [15, 30, 60, 1000]
        , limit: 15 //每页默认显示的数量

        , title: '端口指纹信息'
        , id: 'testReload'
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {type: 'numbers', field: 'id', title: 'ID', width: 80, sort: true}
            // ,{type:"number",title:'id',templet:'{{d.LAY_TABLE_INDEX+1}}', width: 80, sort: true}

            , {
                field: 'ips', title: '来源', width: 200, sort: true
            }
            , {
                field: 'ip', title: 'IP ', width: 150

            }
 , {field: 'port', title: '端口', width: 100, sort: true }
 , {field: 'finger_name', title: '服务', width: 200, sort: true }
  , {
                field: 'status', title: '状态', width: 100, sort: true, templet: function (res) {
                    if (res.status == 'closed') {
                        return '<span class="layui-badge layui-bg-gray " ><span class="fa  " ></span> 关闭</span>'
                    } else if (res.status == 'open') {
                        return '<span class="layui-badge layui-bg-blue "> <span class="fa "></span> 开放</span>'
                    } else {
                        return '<span class="layui-badge layui-bg-black">未定义</span>'
                    }
                }
            }
 , {field: 'finger_product', title: '产品', width: 200, sort: true }
 , {field: 'finger_version', title: '版本', width: 100, sort: true }
 , {field: 'finger_extrainfo', title: '信息', width: 200, sort: true }
 , {field: 'finger_cpe', title: 'cpe', width: 300, sort: true }
            , {
                field: 'scan_time',
                title: '扫描时间',
                width: 200, sort: true,
                temple: function (res) {
                    if (res.scan_time == null) {
                        return '<div>暂无</div>'
                    } else {
                        return "<div>{{layui.util.toDateString(res.news_time,'yyyy-MM-dd HH:mm:ss')}}</div>"
                    }
                }
            }



            // , {fixed: 'right', title: '操作', toolbar: '#barDemo', width: 100}
        ]]
        , page: true
    });


    //头工具栏事件
    table.on('toolbar(test)', function (obj) {
        var checkStatus = table.checkStatus(obj.config.id);
        switch (obj.event) {
            case 'sendEmain':
                var accounts = checkStatus.data;
                if (accounts.length == 0) {
                    layer.msg('至少也得选择一个吧', {icon: 2});
                    return;
                }
                var data_account_name = [];
                $.each(accounts, function (key, val) {
                    data_account_name.push('<span style="color: red">' + val.title + '</span>');
                });
                layer.confirm('发送新闻有:<br>' + data_account_name.join('<br>'), function (index) {
                     layer.load();

        layer.msg('正在发送新闻');
                    zlajax.post({
                        'url': '/send_email/',
                        "traditional": true,
                        'data': {
                            'news_title': JSON.stringify(accounts)
                        },
                        'success': function (data) {
                            if (data['code'] == 0) {
                                layer.closeAll('loading');
                                layer.msg(data['message']);
                                table.reload('testReload', {});
                            } else {
                                layer.closeAll('loading');
                                layer.msg(data['message']);
                                table.reload('testReload', {});
                            }
                        },
                        'fail': function (error) {
                            layer.msg('网络错误！')
                        }
                    })
                });
                break;
        }
    });


    //监听行工具事件
    table.on('tool(test)', function (obj) {
        console.log(obj);
        var data = obj.data;
        var task_id = data.id;


        if  (obj.event === 'show') {
            layer.confirm('展示pdf？', function (index) {
                var id = data['id'];
                window.open('/newws/' + id + '/')
                layer.msg('跳转新页面');
            });
        }
        return false;
    });

    $('#submit').on('click', function () {
        // var ip = $("#ip").val();
        var port = $("#port").val();
        var name = $("#name").val();
        var obj = new Object();

        // if (ip != "") {
        //     obj.ip = ip;
        // }
        if (port != "") {
            obj.port = port;
        }
          if (name != "") {
            obj.name = name;
        }
        if (Object.keys(obj).length == 0) {
            layer.msg("请选择相关选项！");
            return;
        }
        table.reload('testReload', {
            method: 'post',
            url: '/admin/iport/',
            where: obj,
            page: {
                curr: 1
            },
            done: function (res) {

                // if ($("#ip").val() == "") {
                //     delete this.where.ip
                // }
                 if ($("#port").val() == "") {
                    delete this.where.port
                }
                if ($("#name").val() == "") {
                    delete this.where.name
                }
                // this.where={}; //解决参数叠加问题 https://fly.layui.com/jie/21267/
                if (res['count'] == 0) {
                    layer.msg(res['message']);
                    setTimeout(function () {
                        window.location = '/admin/iport/';
                    }, 1000);
                } else {
                    layer.msg(res['message']);
                }
            }
        })
    });
});
