function image_filter() {
    opt_type = [];

    $('input[name=opt]:checked').each(function () {
        opt_type.push($(this).val());
    });

    $.ajax({
        url: "image_filter",
        method: "post",
        data: {
            'opt_type' : opt_type.join()
        },
        dataType: 'html',
        success: function (data) {
            $('.content-list').html(data);
        },
        error: function (data) {
            console.log('error :', data);
        }
    });
}

$(document).ready(function(){
    // onload
    image_filter();
});

function set_like(gl_idx, e) {
    $.ajax({
        url: "set_like",
        method: "post",
        data: {
            'gl_idx': gl_idx
        },
        dataType: 'text',
        success: function(res) {
            cnt = parseInt($(e).children(":first").text());

            if (res == '0') { // 좋아요 등록
                $(e).children(":first").text(cnt + 1);
                $(e).css('color', '#ff0000');
            } else if(res == '1') { // 좋아요 해제
                $(e).children(":first").text(cnt - 1);
                $(e).css('color', '#393e46');
            }
            // res = -1인 경우 세션에 유저 정보 없는 경우
        },
        error: function(msg) {
            console.log('error :', msg);
        }
    });
}
