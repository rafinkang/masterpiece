$(document).ready(function(){
    const USER_IDX = JSON.parse(sessionStorage.getItem('login_data'))['user_idx'];
    let original_name;
    let style_type;

    readURL = function(input) {
        if(!/\.(jpg|jpeg|png)$/i.test(input.files[0].name)){

            alert('이미지파일만 선택해 주세요.\n\n현재 파일 : ' + input.files[0].name);

        } else if (input.files && input.files[0]) {
            var reader = new FileReader();
      
            reader.onload = function(e) {
                $('.ch-image-upload-wrap').hide();
                $('.ch-file-upload-image').attr('src', e.target.result);
                $(".ch-file-upload-content").show();
            };
      
          reader.readAsDataURL(input.files[0]);
      
        } else {
            removeUpload();
        }
    }

    imageCopy = function() {
        var imgData = [{"imgURL" : sessionStorage.getItem("origin_image")}];
        
        $('.ch-image-upload-wrap').hide();
        $('.ch-file-upload-image').attr('src', imgData[0].imgURL);
        $(".ch-file-upload-content").show();
    }
      
    removeUpload = function() {
        $('.ch-file-upload-input').val("")
        $(".ch-file-upload-content").hide();
        $('.ch-image-upload-wrap').show();
    }

    playVideo = function() {
        const ch_output_image_container = $("#ch_output_image_container");

        tg_str = '<div class="row ch-file-upload-box">' +
                    '<video src="masterpiece/static/video/mp_alter_video.mp4" style="width:100%;" autoplay></video>' +
                '</div>';
        
        ch_output_image_container.empty();
        ch_output_image_container.append(tg_str);

    }

    setImage = function(type) {
        var file = $("#ch_input_image")[0].files[0];
        var dataURI;
        const ch_input_image_container = $("#ch_input_image_container");

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
            
                    tempImgUpload(dataURI);
                };
            };

        } else { // 이미지 파일을 팔렛트에서 가져온 경우
            original_name = sessionStorage.getItem("origin_image_name");
            dataURI = $('.ch-file-upload-image').attr('src');
            
            if (!original_name) { // original image의 이름이 없을 경우 "Untitiled.확장자"로 저장
                // data:image/png;
                ets = dataURI.split(";")[0].split("/")[1];
                original_name = "Untitled." + ets;
            }
    
            $('img.origin-thumbnail').each(function(){
                $(this)[0].src = dataURI;
            });
    
            style_type = type
    
            tempImgUpload(dataURI);
        }
    }

    tempImgUpload = function(dataURI) {
        $.ajax({
            url: "pallate/ch_style/temp_img_upload",
            type: 'post',
            data: {
                'dataURI' : dataURI
            },
            dataType: 'text',
            success: function(res) {
                originToMasterpiece(res);
            },
            error: function(error) {
                console.log('error', error);
            }
        });
    }

    originToMasterpiece = function(img_name) {
        $.ajax({
            url: "pallate/ch_style/change_masterpiece",
            type: 'post',
            data: {
                'img_name': img_name,
                'styleType' : style_type
            },
            dataType: 'text',
            success: function(res) {
                const ch_output_image_container = $("#ch_output_image_container");
                let res_list = res.split('/');
                const master_name = res_list[res_list.length - 1];

                tg_str = '<div class="row ch-file-upload-box">' +
                            '<img src="' + res + '" class="ch-file-output-image ch-image rounded">' +
                        '</div>' +
                        '<div class="ch-image-title-wrap row">' +
                            '<a class="hidden-download" id="download_link" href="#" download="#"></a>' +
                            '<button type="button" class="btn btn-custom-2 col-md-6 ch-image-btn" onclick="downloadImage(\'' + master_name + '\')">다운로드</button>' +
                        '</div>';
                
                ch_output_image_container.empty();
                ch_output_image_container.append(tg_str);
            },
            error: function(error) {
                console.log('error', error);
            }
        });
    }

    downloadImage = function(master_name) {
        download_href = $('#download_link').attr('href');

        if(download_href != "#") {
            $('#download_link')[0].click();
        } else {
            $.ajax({
                url: "pallate/ch_style/download_img",
                type: 'post',
                data: {
                    'styleType' : style_type,
                    'masterpieceImageName' : master_name,
                    'originalImageName' : original_name
                },
                dataType: 'text',
                success: function(res) {
                    $('#download_link').prop('href', res); 
                    $('#download_link').prop('download', 'GIGJ_masterpiece.jpg');
                    $('#download_link')[0].click();
                },
                error: function(error) {
                    console.log('error', error);
                }
            });
        }

        
    }
      
});