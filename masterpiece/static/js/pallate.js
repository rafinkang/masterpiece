function origin_thumbnail(obj) {
    var fileList = obj.files ;
    // 읽기
    var reader = new FileReader();
    reader.readAsDataURL(fileList[0]);

    //로드 한 후
    reader.onload = function  () {
        //로컬 이미지를 보여주기
        //document.querySelector('#preview').src = reader.result;
        
        //썸네일 이미지 생성
        var tempImage = new Image(); //drawImage 메서드에 넣기 위해 이미지 객체화
        tempImage.src = reader.result; //data-uri를 이미지 객체에 주입


        tempImage.onload = function() {
            //리사이즈를 위해 캔버스 객체 생성
            var canvas = document.createElement('canvas');
            var canvasContext = canvas.getContext("2d");
            
            //캔버스 크기 설정
            // canvas.width = 150; //가로 150px
            // canvas.height = 150; //세로 150px
            canvas.width = tempImage.width; //가로 150px
            canvas.height = tempImage.height; //세로 150px
            
            //이미지를 캔버스에 그리기
            // canvasContext.drawImage(this, 0, 0, 150, 150);
            canvasContext.drawImage(this, 0, 0);
            //캔버스에 그린 이미지를 다시 data-uri 형태로 변환
            var dataURI = canvas.toDataURL("image/jpg");
            // console.log(dataURI)
            sessionStorage.setItem("origin_image", dataURI)

            //썸네일 이미지 보여주기
            $('img.origin-thumbnail').each(function(){
                $(this)[0].src = dataURI;
            });
            // document.querySelector('img.origin-thumbnail').src = dataURI;
            
            //썸네일 이미지를 다운로드할 수 있도록 링크 설정
            //document.querySelector('#download').href = dataURI;
        };
    }; 
}

function color_pick() {
    origin_image = sessionStorage.getItem("origin_image");
    if(!origin_image) {
        alert('파일을 선택해주세요.');
        return;
    }
    $.ajax({
        url: "pallate/color_pick",
        method: "post",
        data: {
            'dataURI': origin_image,
        },
        dataType: 'json',
        success: function (data) {
            // console.log('return data : ', data);
            sessionStorage.setItem("color_pick", JSON.stringify(data));
            load_storage();
            
        },
        error: function (data) {
            console.log('error :', data);
        }
    });
}

function load_storage() {
    
    if(local_origin_image = sessionStorage.getItem("origin_image")) {
        // $('img.origin-thumbnail')[0].src = local_origin_image;
        $('img.origin-thumbnail').each(function(){
            $(this)[0].src = local_origin_image;
        });
    }
    
    if(color_pick_data = sessionStorage.getItem('color_pick')){
        data = JSON.parse(color_pick_data)
        $('.pallate .pallate-list .color1').css('background-color', data['hex1']);
        $('.pallate .pallate-list .color2').css('background-color', data['hex2']);
        $('.pallate .pallate-list .color3').css('background-color', data['hex3']);
        $('.pallate .pallate-list .color4').css('background-color', data['hex4']);

        $('.pallate .pallate-list .color1').width(data['percent1']+'%');
        $('.pallate .pallate-list .color2').width(data['percent2']+'%');
        $('.pallate .pallate-list .color3').width(data['percent3']+'%');
        $('.pallate .pallate-list .color4').width(data['percent4']+'%');
        
        $('.pallate .pallate-list .hsv1').text('('+data['h1']+','+data['s1']+','+data['v1']+')');
        $('.pallate .pallate-list .hsv2').text('('+data['h2']+','+data['s2']+','+data['v2']+')');
        $('.pallate .pallate-list .hsv3').text('('+data['h3']+','+data['s3']+','+data['v3']+')');
        $('.pallate .pallate-list .hsv4').text('('+data['h4']+','+data['s4']+','+data['v4']+')');

        $('.pallate .pallate-list .hex1').text(data['hex1']);
        $('.pallate .pallate-list .hex2').text(data['hex2']);
        $('.pallate .pallate-list .hex3').text(data['hex3']);
        $('.pallate .pallate-list .hex4').text(data['hex4']);
        // 색상뽑기 내부 컬러박스
        $('#pallate .color-pick .color-pick-box.color1').css('background-color', data['hex1']);
        $('#pallate .color-pick .color-pick-box.color2').css('background-color', data['hex2']);
        $('#pallate .color-pick .color-pick-box.color3').css('background-color', data['hex3']);
        $('#pallate .color-pick .color-pick-box.color4').css('background-color', data['hex4']);

        $('#pallate .color-pick .color-pick-box span.hex1').text(data['hex1']);
        $('#pallate .color-pick .color-pick-box span.hex2').text(data['hex2']);
        $('#pallate .color-pick .color-pick-box span.hex3').text(data['hex3']);
        $('#pallate .color-pick .color-pick-box span.hex4').text(data['hex4']);

        $('#pallate .color-pick .color-pick-box.color1').height(data['percent1']+'%');
        $('#pallate .color-pick .color-pick-box.color2').height(data['percent2']+'%');
        $('#pallate .color-pick .color-pick-box.color3').height(data['percent3']+'%');
        $('#pallate .color-pick .color-pick-box.color4').height(data['percent4']+'%');
        // 감성분석 결과
        $('#pallate table.emotion td.color_pred').text(data['color_pred']);
        $('#pallate table.emotion td.season_pred').text(data['season_pred']);
        $('#pallate table.emotion td.cw_pred').text(data['cw_pred']);
        $('#pallate table.emotion td.cp_pred').text(data['cp_pred']);
        $('#pallate table.emotion td.value_pred').text(data['value_pred']);
    }
}

function emotion_filter() {
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
        url: "pallate/emotion_filter",
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
            console.log('return data : ', data);
            $('.content-list').html(data);
        },
        error: function (data) {
            console.log('error :', data);
        }
    });
}

function color_dress_image(obj) {
    var fileList = obj.files ;
    // 읽기
    var reader = new FileReader();
    reader.readAsDataURL(fileList[0]);

    //로드 한 후
    reader.onload = function  () {
        //로컬 이미지를 보여주기
        //document.querySelector('#preview').src = reader.result;
        
        //썸네일 이미지 생성
        var tempImage = new Image(); //drawImage 메서드에 넣기 위해 이미지 객체화
        tempImage.src = reader.result; //data-uri를 이미지 객체에 주입


        tempImage.onload = function() {
            //리사이즈를 위해 캔버스 객체 생성
            var canvas = document.createElement('canvas');
            var canvasContext = canvas.getContext("2d");
            
            //캔버스 크기 설정
            // canvas.width = 150; //가로 150px
            // canvas.height = 150; //세로 150px
            canvas.width = tempImage.width; //가로 150px
            canvas.height = tempImage.height; //세로 150px
            
            //이미지를 캔버스에 그리기
            // canvasContext.drawImage(this, 0, 0, 150, 150);
            canvasContext.drawImage(this, 0, 0);
            //캔버스에 그린 이미지를 다시 data-uri 형태로 변환
            var dataURI = canvas.toDataURL("image/jpg");
            // console.log(dataURI)
            sessionStorage.setItem("color-dress-image", dataURI)

            //썸네일 이미지 보여주기
            document.querySelector('img.color-dress-image').src = dataURI;
            
            //썸네일 이미지를 다운로드할 수 있도록 링크 설정
            //document.querySelector('#download').href = dataURI;
        };
    }; 
}

$(document).ready(function(){
    // onload
    load_storage()

    // 탭메뉴 컨트롤
    $('ul.pallate-nav li').click(function(){
        self = $(this);
        
        $('ul.pallate-nav li').removeClass("active");
        self.addClass("active");
        
        $('.pallate-content .pallate-tab').hide();
        $('.pallate-content .pallate-tab').filter('[data-page="'+self.attr('data-page')+'"]').show();

            
        // 색상입히기용, 민수 추가함
        color_pick_data = sessionStorage.getItem('color_pick')
        data = JSON.parse(color_pick_data)

        $('.color-dress .droplet_1').css('fill', data['hex1']);
        $('.color-dress .droplet_2').css('fill', data['hex2']);
        $('.color-dress .droplet_3').css('fill', data['hex3']);
        $('.color-dress .droplet_4').css('fill', data['hex4']);
    });

});