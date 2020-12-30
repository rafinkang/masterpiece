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

// 색상뽑기 후 저장
function color_insert() {
    origin_image = sessionStorage.getItem("origin_image");
    color_pick = sessionStorage.getItem("color_pick");
    if(!origin_image) {
        alert('파일을 선택해주세요.');
        return;
    }
    $.ajax({
        url: "pallate/color_insert",
        method: "post",
        data: {
            'dataURI': origin_image,
            'color_pick': color_pick
        },
        dataType: 'text',
        success: function (data) {
            // console.log('return data : ', data);
            if(data == 1) {
                alert("색상이 저장 되었습니다.")
            }else{
                alert(data)
            }
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

        $('.pallate .pallate-list .hex1 span').text(data['hex1']);
        $('.pallate .pallate-list .hex2 span').text(data['hex2']);
        $('.pallate .pallate-list .hex3 span').text(data['hex3']);
        $('.pallate .pallate-list .hex4 span').text(data['hex4']);
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
        $('#pallate table.emotion td.color_pred').text(data['color']);
        $('#pallate table.emotion td.season_pred').text(data['season']);
        $('#pallate table.emotion td.cw_pred').text(data['cw']);
        $('#pallate table.emotion td.cp_pred').text(data['cp']);
        $('#pallate table.emotion td.value_pred').text(data['value']);
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
            // console.log('return data : ', data);
            $('.content-list').html(data);
        },
        error: function (data) {
            console.log('error :', data);
        }
    });
}

function picktostorage(data) {
    data.percent1 = 25;
    data.percent2 = 25;
    data.percent3 = 25;
    data.percent4 = 25;

    sessionStorage.setItem("color_pick", JSON.stringify(data));
    load_storage();
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
    emotion_filter()
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

        $('.cd-wrap .droplet_1').css('fill', data['hex1']);
        $('.cd-wrap .droplet_2').css('fill', data['hex2']);
        $('.cd-wrap .droplet_3').css('fill', data['hex3']);
        $('.cd-wrap .droplet_4').css('fill', data['hex4']);
    });

    // 색상 입히기 버튼 클릭시, 민수 추가함
    readURL2 = function(input) {
        console.log("이미지 입력되었음")

        // hex1,2,3,4 를 변수로 지정하자
        color_pick_data = sessionStorage.getItem('color_pick')
        data = JSON.parse(color_pick_data)
        hex1 = data['hex1']
        hex2 = data['hex2']
        hex3 = data['hex3']
        hex4 = data['hex4']

        if(!/\.(jpg|jpeg|png)$/i.test(input.files[0].name)){

            alert('이미지파일만 선택해 주세요.\n\n현재 파일 : ' + input.files[0].name);

        } else if (input.files && input.files[0]) {
            var reader = new FileReader();
      
            reader.onload = function(e) {
                $('.cd-image-upload-wrap').hide();
                $('.cd-file-upload-image').attr('src', e.target.result);
                $(".cd-file-upload-content").show();
            };
      
            reader.readAsDataURL(input.files[0]);
      
        } else {
            removeUpload2();
        }
    }

    
    // imageCopy = function() {
    //     var imgData = [{"imgURL" : sessionStorage.getItem("origin_image")}];
        
    //     $('.cd-image-upload-wrap').hide();
    //     $('.cd-file-upload-image').attr('src', imgData[0].imgURL);
    //     $(".cd-file-upload-content").show();
    // }
      
    removeUpload2 = function() {
        $('.cd-file-upload-input').val("")
        $(".cd-file-upload-content").hide();
        $('.cd-image-upload-wrap').show();
    }

    setImage2 = function(type) {
        console.log("색상 입히기 버튼 눌렸음")
        var file = $("#cd_input_image")[0].files[0];
        var dataURI;
        const cd_input_image_container = $("#cd_input_image_container");

        console.log("file", file);

        if (file) { // 이미지 파일을 선택한 경우

            original_name = file.name;
    
            // FileReader 객체 사용
            var reader = new FileReader();
    
            // 파일을 읽는다
            reader.readAsDataURL(file);
                
            // 읽기
            var reader = new FileReader();
            reader.readAsDataURL(file);
        
            //로드 한 후
            reader.onload = function() {
                //썸네일 이미지 생성
                var tempImage = new Image(); //drawImage 메서드에 넣기 위해 이미지 객체화
                tempImage.src = reader.result; //data-uri를 이미지 객체에 주입
    
    
                tempImage.onload = function() {
                    //리사이즈를 위해 캔버스 객체 생성
                    var canvas = document.createElement('canvas');
                    var canvasContext = canvas.getContext("2d");
    
                    canvas.width = tempImage.width;
                    canvas.height = tempImage.height;
                    
                    //이미지를 캔버스에 그리기
                    canvasContext.drawImage(this, 0, 0);
                    //캔버스에 그린 이미지를 다시 data-uri 형태로 변환
                    dataURI = canvas.toDataURL("image/jpg");
    
                    /*
                        TO-DO pallate.py와 합칠 때 "origin_iamge" json형태로 바꿔서 저장하기
                    */
                    sessionStorage.setItem("origin_image", dataURI);
                    sessionStorage.setItem("origin_image_name", original_name);
    
                    $('img.origin-thumbnail').each(function(){
                        $(this)[0].src = dataURI;
                    });
            
                    style_type = type
            
                    tempImgUpload2(dataURI);
                };
            };

        } else { // 이미지 파일을 팔렛트에서 가져온 경우
            original_name = sessionStorage.getItem("origin_image_name");
            dataURI = $('.cd-file-upload-image').attr('src');
            
            if (!original_name) { // original image의 이름이 없을 경우 "Untitiled.확장자"로 저장
                // data:image/png;
                ets = dataURI.split(";")[0].split("/")[1];
                original_name = "Untitled." + ets;
            }
    
            $('img.origin-thumbnail').each(function(){
                $(this)[0].src = dataURI;
            });
    
            style_type = type
    
            tempImgUpload2(dataURI);
        }
    }

    tempImgUpload2 = function(dataURI) {
        console.log("팔렛트js의 tempImgUpload2 부분 실행되었음")
        $.ajax({
            url: "pallate/cd_style/temp_img_upload2",
            type: 'post',
            data: {
                'dataURI' : dataURI
            },
            dataType: 'text',
            success: function(res) {
                originToMasterpiece2(res);
            },
            error: function(error) {
                console.log('error', error);
            }
        });
    }

    originToMasterpiece2 = function(img_name) {
        $.ajax({
            url: "pallate/cd_style/change_masterpiece2",
            type: 'post',
            data: {
                'img_name': img_name,
                'styleType' : style_type,
                'hex1' : hex1,
                'hex2' : hex2,
                'hex3' : hex3,
                'hex4' : hex4,
            },
            dataType: 'text',
            success: function(res) {
                console.log("res : ",res)

                const cd_output_image_container = $("#cd_output_image_container");
                let res_list = res.split('/');
                const master_name = res_list[res_list.length - 1];

                tg_str = '<div class="row cd-file-upload-box">' +
                            '<img src="' + res + '" class="cd-file-output-image cd-image rounded">' +
                        '</div>' +
                        '<div class="cd-image-title-wrap row">' +
                            '<a class="hidden-download" id="download_link" href="#" download="#"></a>' +
                            '<button type="button" class="btn btn-custom-2 col-md-6 cd-image-btn" onclick="downloadImage(\'' + master_name + '\')">다운로드</button>' +
                        '</div>';
                
                cd_output_image_container.empty();
                cd_output_image_container.append(tg_str);
            },
            error: function(error) {
                console.log('error', error);
            }
        });
    }

    $('#color_pick').click(color_pick);
    $('#color_insert').click(color_insert);
});