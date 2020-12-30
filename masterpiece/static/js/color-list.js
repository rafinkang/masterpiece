function list_filter() {
    color_type = [];
    season_type = [];
    cw_type = [];
    cp_type = [];
    value_type = [];

    $('input[name=color]:checked').each(function () {
        color_type.push($(this).val());
    });
    $('input[name=season]:checked').each(function () {
        season_type.push($(this).val());
    });
    $('input[name=cw]:checked').each(function () {
        cw_type.push($(this).val()); 
    });
    $('input[name=cp]:checked').each(function () {
        cp_type.push($(this).val());
    });
    $('input[name=value]:checked').each(function () {
        value_type.push($(this).val());
    });
    

    $.ajax({
        url: "/gallery/color_list",
        method: "post",
        data: {
            'color_type': color_type.join(),
            'season_type': season_type.join(),
            'cw_type': cw_type.join(),
            'cp_type': cp_type.join(),
            'value_type': value_type.join(),
        },
        dataType: 'html',
        success: function (data) {
            // console.log('return data : ', data);
            $('.content-list').html(data);
        },
        error: function (data) {
            console.log('error :', data);
        }
    });
}

function copy(target) {
    setTimeout(function() {
        $('#copied_tip').remove();
    }, 1000);
    // $(target).parent('.place').append("<div class='tip' id='copied_tip'>Copied!</div>");
    var text = target.textContent;
    $(target).append("<div class='tip' id='copied_tip'>Copied!</div>");
    var input = document.createElement('input');
    input.setAttribute('value', text);
    document.body.appendChild(input);
    input.select();
    var result = document.execCommand('copy');
    document.body.removeChild(input)
    return result;
}

function set_like(cl_idx, e) {
    $.ajax({
        url: "/gallery/color_like",
        method: "post",
        data: {
            'cl_idx': cl_idx
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