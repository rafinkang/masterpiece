function image_filter() {
    artist_type = [];
    style_type = [];

    $('input[name=artist]:checked').each(function () {
        artist_type.push($(this).val());
    });
    $('input[name=style]:checked').each(function () {
        style_type.push($(this).val());
    });

    $.ajax({
        url: "image_filter",
        method: "post",
        data: {
            'artist_type': artist_type.join(),
            'style_type': style_type.join()
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
