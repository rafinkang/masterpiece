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