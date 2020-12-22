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
            console.log(dataURI)
            localStorage.setItem("origin_image", dataURI)

            //썸네일 이미지 보여주기
            document.querySelector('img.origin-thumbnail').src = dataURI;
            
            //썸네일 이미지를 다운로드할 수 있도록 링크 설정
            //document.querySelector('#download').href = dataURI;
        };
    }; 
}

function color_pick(params) {
    console.log("색상뽑기이이~~")
    $.ajax({
        url: "pallate/color_pick",
        method: "post",
        data: {
            'dataURI': localStorage.getItem("origin_image"),
        },
        dataType: 'json',
        success: function (data) {
            console.log('return data : ', data);
            
        },
        error: function (data) {
            console.log('error :', data);
        }
    });
    
}

$(document).ready(function(){
    // onload
    local_origin_image = localStorage.getItem("origin_image");
    if(local_origin_image != null) {
        $('img.origin-thumbnail')[0].src = local_origin_image;
    }

    // 탭메뉴 컨트롤
    $('ul.pallate-nav li').click(function(){
        self = $(this);
        
        $('ul.pallate-nav li').removeClass("active");
        self.addClass("active");
        
        $('.pallate-content .pallate-tab').hide();
        $('.pallate-content .pallate-tab').filter('[data-page="'+self.attr('data-page')+'"]').show();
    });

});