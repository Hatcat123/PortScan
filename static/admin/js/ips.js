layui.use(['table', 'jquery', 'util', 'layer', 'form', 'code'], function () {
    var table = layui.table;
    var $ = layui.$;
    util = layui.util;
    var form = layui.form;

    table.render({
        elem: '#test'
        , height: 'full-200'
        , url: '/admin/ips/'
        , method: 'post'
        , toolbar: '#toolbarDemo'
        , cellMinWidth: 80
        , limits: [ 60,1000]
        , limit: 15 //每页默认显示的数量
        // , headers: {'X-CSRF-TOKEN': token}
        , title: '资产管理'
        , id: 'testReload'
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {type: 'numbers', field: 'id', title: 'ID', width: 80, sort: true}

            , {field: 'ips', title: 'IP地址/网段 ', width: 350}

            , {
                field: 'status', title: '状态', width: 100, sort: true, templet: function (res) {
                    if (res.status == '0') {
                        return '<span class="layui-badge layui-bg-gray " ><span class="fa fa-spinner " ></span> 放弃</span>'
                    } else if (res.status == '1') {
                        return '<span class="layui-badge layui-bg-blue "> <span class="fa fa-spinner fa-spin"></span> 监控</span>'
                    } else {
                        return '<span class="layui-badge layui-bg-black">未定义</span>'
                    }
                }
            }
              , {
                field: 'status', title: '选择', width: 100, templet: function (res) {
                    if (res.status == '1') {
                        return '<input type="checkbox" name="status" value=' + res.id + ' lay-skin="switch" lay-text="监控|弃用" lay-filter="sexDemo"  checked>'
                    } else if (res.status == '0') {
                        return '<input type="checkbox" name="status" value=' + res.id + ' lay-skin="switch" lay-text="监控|弃用" lay-filter="sexDemo" >'
                    } else {
                        return '<input type="checkbox" name="status" value=' + res.id + ' lay-skin="switch" lay-text="监控|弃用" lay-filter="sexDemo" >'
                    }
                }
            }
                   , {
                field: 'scan_time',
                title: '最近扫描时间',
                width: 200, sort: true,
                temple: function (res) {
                    if (res.scan_time == null) {
                        return '<div>暂无</div>'
                    } else {
                        return "<div>{{layui.util.toDateString(res.scan_time,'yyyy-MM-dd HH:mm:ss')}}</div>"
                    }
                }
            }
            , {
                field: 'create_time',
                title: '添加时间',
                width: 200, sort: true,
                temple: function (res) {
                    if (res.create_time == null) {
                        return '<div>暂无</div>'
                    } else {
                        return "<div>{{layui.util.toDateString(res.create_time,'yyyy-MM-dd HH:mm:ss')}}</div>"
                    }
                }
            }
             , {field: 'id', title: '查看详情 ', width: 100,
                    templet :"<div ><a href='/admin/show/?id={{d.id}}' target=\"_blank\">详情</a></div>"
                }
            , {fixed: 'right', title: '操作', toolbar: '#barDemo', width: 150}
        ]]
        , page: true
    });


    //头工具栏事件
    table.on('toolbar(test)', function (obj) {
        var checkStatus = table.checkStatus(obj.config.id);
        switch (obj.event) {

            case 'addIPS':
                layer.open({
                    type: 1,
                    anim: 1,
                    area: ['800px', '30%'],
                    skin: 'demo-class',
                    // btn: ['立即提交', '取消'],
                    maxmin: true,
                    shadeClose: false,
                    title: '添加资产',
                    content: $('#add'),
                    success: function (index) {
                        var but = $(".layui-layer-btn0");
                        but.attr('lay-filter', 'demo1');
                        but.attr('lay-submit', "");
                    }
                });
                break;
        }
    });


    //监听行工具事件
    table.on('tool(test)', function (obj) {
        console.log(obj);
        var data = obj.data;
        var id = data.id;


        if (obj.event === 'del') {
            layer.confirm('真的删除该资产吗？', function (index) {


                zlajax.post({
                    'url': '/admin/del_ips/',
                    'data': {
                        'id': data.id,

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
        }

        return false;
    });

    //添加邮件
    form.on('submit(add)', function (data1, index) {
        var dic = new Object();
        var ips = data1.field.ips;

        dic.ips = ips;

        zlajax.post({
            'url': '/admin/add_ips/',
            'data': dic,
            'success': function (data) {
                if (data['code'] == 200) {
                    layer.msg(data['message']);
                    form.val('example', {
                        'ips': null,

                    });
                    setTimeout(function () {
                        layer.closeAll();
                    }, 500);
                    layer.msg('添加成功');
                    table.reload('testReload', {});
                } else {
                    layer.msg(data['message']);

                }
            }, 'fail': function () {
                layer.msg('网络错误！')
            }
        });

        return false
    });

     //监听选择操作
    form.on('switch(sexDemo)', function (obj) {
        var dic = new Object();
        id = this.value;
        dic.id = id;
        if (obj.elem.checked == true) {
            dic.status = '1';
        }
        else {
            dic.status = '0';
        }
        zlajax.post({
            'url': '/admin/change_ips/',
            'data': dic,
            'success': function (data) {
                if (data['code'] == 200) {
                    table.reload('testReload', {});
                    layer.msg(data['message']);

                } else {
                    layer.msg(data['message']);
                }
            }, 'fail': function () {
                layer.msg('网络错误！')
            }
        });
    });
});
