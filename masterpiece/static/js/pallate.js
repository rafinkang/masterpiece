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
            localStorage.setItem("origin_image", dataURI)

            //썸네일 이미지 보여주기
            document.querySelector('img.origin-thumbnail').src = dataURI;
            
            //썸네일 이미지를 다운로드할 수 있도록 링크 설정
            //document.querySelector('#download').href = dataURI;
        };
    }; 
}

function color_pick() {
    $.ajax({
        url: "pallate/color_pick",
        method: "post",
        data: {
            'dataURI': localStorage.getItem("origin_image"),
        },
        dataType: 'json',
        success: function (data) {
            console.log('return data : ', data);
            localStorage.setItem("color_pick", JSON.stringify(data));
            
        },
        error: function (data) {
            console.log('error :', data);
        }
    });
}

function load_localstorage() {
    
    if(local_origin_image = localStorage.getItem("origin_image")) {
        $('img.origin-thumbnail')[0].src = local_origin_image;
    }
    
    if(color_pick_data = localStorage.getItem('color_pick')){
        data = JSON.parse(color_pick_data)
        $('.pallate .pallate-list .color1').css('background-color', data['hex1'])
        $('.pallate .pallate-list .color2').css('background-color', data['hex2'])
        $('.pallate .pallate-list .color3').css('background-color', data['hex3'])
        $('.pallate .pallate-list .color4').css('background-color', data['hex4'])
        
        $('.pallate .pallate-list .hsv1').text('('+data['h1']+','+data['s1']+','+data['v1']+')')
        $('.pallate .pallate-list .hsv2').text('('+data['h2']+','+data['s2']+','+data['v2']+')')
        $('.pallate .pallate-list .hsv3').text('('+data['h3']+','+data['s3']+','+data['v3']+')')
        $('.pallate .pallate-list .hsv4').text('('+data['h4']+','+data['s4']+','+data['v4']+')')

        $('.pallate .pallate-list .hex1').text(data['hex1'])
        $('.pallate .pallate-list .hex2').text(data['hex2'])
        $('.pallate .pallate-list .hex3').text(data['hex3'])
        $('.pallate .pallate-list .hex4').text(data['hex4'])
    }

}

$(document).ready(function(){
    load_localstorage()
    // onload

    // 탭메뉴 컨트롤
    $('ul.pallate-nav li').click(function(){
        self = $(this);
        
        $('ul.pallate-nav li').removeClass("active");
        self.addClass("active");
        
        $('.pallate-content .pallate-tab').hide();
        $('.pallate-content .pallate-tab').filter('[data-page="'+self.attr('data-page')+'"]').show();
    });

});