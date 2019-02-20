// 全局通用js文件
$(document).ready(function () {
    // 字数监测 start
    var checkStrLengths = function (str, maxLength) {
        var maxLength = maxLength;
        var result = 0;
        if (str && str.length > maxLength) {
            result = maxLength;
        } else {
            result = str.length;
        }
        return result;
    };

    //监听输入
    $(".wishContent").on('input propertychange', function () {

        //获取输入内容
        var userDesc = $(this).val();

        //判断字数
        var len;
        if (userDesc) {
            len = checkStrLengths(userDesc, 15);
        } else {
            len = 0
        }

        //显示字数
        $(".wordsNum").html(len + '/15');
    });
    // 字数监测 end
});

