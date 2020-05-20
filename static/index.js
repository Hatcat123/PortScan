layui.use(['table', 'jquery', 'util', 'layer', 'form', 'code'], function () {
    var table = layui.table;
    var $ = layui.$;
    util = layui.util;


    table.render({
        elem: '#test'
        , height: 'full-200'
        , url: '/'
        , method: 'post'
        , toolbar: '#toolbarDemo'
        , cellMinWidth: 80
        , limits: [15, 30, 60, 1000]
        , limit: 15 //每页默认显示的数量
        // , headers: {'X-CSRF-TOKEN': token}
        , title: '全球动态情报跟踪推送服务专题定制系列'
        , id: 'testReload'
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {type: 'numbers', field: 'id', title: 'ID', width: 80, sort: true}
            // ,{type:"number",title:'id',templet:'{{d.LAY_TABLE_INDEX+1}}', width: 80, sort: true}

            , {
                field: 'type', title: '来源', width: 100, sort: true, templet: function (res) {
                    if (res.type == 'defense') {
                        return '<span class="layui-badge layui-bg-red " ><span class="fa fa-spinner " ></span> DOD</span>'
                    } else if (res.type == 'dodcio') {
                        return '<span class="layui-badge layui-bg-green "> <span class="fa fa-spinner fa-spin"></span> CIO</span>'
                    } else {
                        return '<span class="layui-badge layui-bg-black">未定义</span>'
                    }
                }
            }
            , {
                field: 'title', title: '文章标题 ', width: 500
                , templet: "<div ><a href='{{d.url}}' target=\"_blank\">{{d.title}}</a></div>"
            }

            , {
                field: 'news_time',
                title: '发布时间',
                width: 200, sort: true,
                temple: function (res) {
                    if (res.news_time == null) {
                        return '<div>暂无</div>'
                    } else {
                        return "<div>{{layui.util.toDateString(res.news_time,'yyyy-MM-dd HH:mm:ss')}}</div>"
                    }
                }
            }
            , {
                field: 'status', title: '状态', width: 100, sort: true, templet: function (res) {
                    if (res.status == '0') {
                        return '<span class="layui-badge layui-bg-gray " ><span class="fa fa-spinner " ></span> O</span>'
                    } else if (res.status == '1') {
                        return '<span class="layui-badge layui-bg-blue "> <span class="fa fa-spinner fa-spin"></span> &#10004</span>'
                    } else {
                        return '<span class="layui-badge layui-bg-black">未定义</span>'
                    }
                }
            }
            , {
                field: 'create_time',
                title: '采集时间',
                width: 200, sort: true,
                temple: function (res) {
                    if (res.create_time == null) {
                        return '<div>暂无</div>'
                    } else {
                        return "<div>{{layui.util.toDateString(res.create_time,'yyyy-MM-dd HH:mm:ss')}}</div>"
                    }
                }
            }
            // , {fixed: 'right', title: '操作', toolbar: '#barDemo', width: 150}
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


        if (obj.event === 'del') {
            layer.confirm('真的删除该新闻吗？', function (index) {
                var account_tasks = data['account_tasks'];

                zlajax.post({
                    'url': '/delete/',
                    'data': {
                        'id': data.id,
                        'account_id': data.account_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            obj.del();
                            layer.msg(data['message']);

                        } else {
                            layer.msg(data['message']);
                        }
                    },
                    'fail': function () {
                        layer.msg('网络错误！')
                    }
                });
            });


        } else if (obj.event === 'show') {
            layer.confirm('展示pdf？', function (index) {
                var id = data['id'];
                window.open('/newws/' + id + '/')
                layer.msg('跳转新页面');
            });
        }
        return false;
    });

    $('#submit').on('click', function () {
        var type = $("#select").val();
        var his = $("#his").val();
        var obj = new Object();

        if (type != "") {
            obj.type = type;
        }
        if (his != "") {
            obj.his = his;
        }
        if (Object.keys(obj).length == 0) {
            layer.msg("请选择相关选项！");
            return;
        }
        table.reload('testReload', {
            method: 'post',
            url: '/',
            where: obj,
            page: {
                curr: 1
            },
            done: function (res) {

                if ($("#select").val() == "") {
                    delete this.where.type
                }
                if ($("#his").val() == "") {
                    delete this.where.his
                }
                // this.where={}; //解决参数叠加问题 https://fly.layui.com/jie/21267/
                if (res['count'] == 0) {
                    layer.msg(res['message']);
                    setTimeout(function () {
                        window.location = '/';
                    }, 1000);
                } else {
                    layer.msg(res['message']);
                }
            }
        })
    });
});
