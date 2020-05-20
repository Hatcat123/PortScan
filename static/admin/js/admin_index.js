layui.use(['layer', "carousel", "jquery"], function () {
    var layer = layui.layer;

    var $ = layui.$;
    // header信息
    $('#weather').leoweather({
        format: '，{时段}好！<span id="colock">现在时间是：<strong>{年}年{月}月{日}日 星期{周} {时}:{分}:{秒}</strong>'
    });
    $('#closeInfo').on('click', function () {
        $('#infoSwitch').hide();
    });


    $('.panel .tools .iconpx-chevron-down').click(function () {
        var el = $(this).parents(".panel").children(".panel-body");
        if ($(this).hasClass("iconpx-chevron-down")) {
            $(this).removeClass("iconpx-chevron-down").addClass("iconpx-chevron-up");
            el.slideUp(200);
        } else {
            $(this).removeClass("iconpx-chevron-up").addClass("iconpx-chevron-down");
            el.slideDown(200);
        }
    });

    // 快捷方式
    $('#shortcut section').on('click', function () {
        var title = $(this).children('.value').find('p').text();
        var href = $(this).children('.value').find('a').data('href');
        var icon = $(this).children('.symbol').find('i:first').data('icon');
        var data = {
            href: href,
            icon: icon,
            title: title
        };
        parent.navtab.tabAdd(data);
    });

    var carousel = layui.carousel;
    carousel.render({
        elem: '#test1'
        , arrow: 'none'
        , height: '305px'
        , width: '100%'
        , autoplay: true
        , interval: 5000
        , indicator: 'outside'
    });


    // $(window).on('resize', function () {
        // $.getJSON('./westeros.project.json', function (themeJSON) {
        //     echarts.registerTheme('westeros', JSON.parse(themeJSON));
        //     var chart = echarts.init(document.getElementById('bar'), 'westeros');
    $(function () {
        var chart1 = echarts.init(document.getElementById('bar1'), 'essos', {renderer: 'canvas'});
        window.onresize = function(){
            chart1.resize();
        };
        chart1.setOption({

            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
        });
        $(
            function () {
                fetchData1(chart1);
                setInterval(fetchData1, 1000 * 60 * 60 * 2);
            }
        );

        function fetchData1() {
            $.ajax({
                type: "GET",
                url: "/admin/barChart1/",
                dataType: 'json',
                success: function (result) {
                    chart1.setOption(result);
                }
            });
        }
    });

    $(function () {
        var chart2 = echarts.init(document.getElementById('bar2'), 'essos', {renderer: 'canvas'});
        window.onresize = function () {
            chart2.resize();
        };
        chart2.setOption({

            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
        });
        $(
            function () {
                fetchData2(chart2);
                setInterval(fetchData2, 1000 * 60 * 60);
            }
        );

        function fetchData2() {
            $.ajax({
                type: "GET",
                url: "/admin/barChart2/",
                dataType: 'json',
                success: function (result) {
                    chart2.setOption(result);
                }
            });
        }
    });

     $(function () {
        var chart3 = echarts.init(document.getElementById('bar3'), 'essos', {renderer: 'canvas'});
        window.onresize = function () {
            chart3.resize();
        };
        chart3.setOption({

            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            // xAxis:{
            //     nameRotate:90
            // }
        });
        $(
            function () {
                fetchData3(chart3);
                setInterval(fetchData3, 1000 * 60 * 60);
            }
        );

        function fetchData3() {
            $.ajax({
                type: "GET",
                url: "/admin/barChart3/",
                dataType: 'json',
                success: function (result) {
                    chart3.setOption(result);
                }
            });
        }
    });

          $(function () {
        var chart4 = echarts.init(document.getElementById('bar4'), 'essos', {renderer: 'canvas'});
        window.onresize = function () {
            chart4.resize();
        };
        chart4.setOption({

            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            // xAxis:{
            //     nameRotate:90
            // }
        });
        $(
            function () {
                fetchData4(chart4);
                setInterval(fetchData4, 1000 * 60 * 60);
            }
        );

        function fetchData4() {
            $.ajax({
                type: "GET",
                url: "/admin/barChart4/",
                dataType: 'json',
                success: function (result) {
                    chart4.setOption(result);
                }
            });
        }
    });
    });






