$(document).ready(function(){
    readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
      
            reader.onload = function(e) {
                $('.ch-image-upload-wrap').hide();
                $('.ch-file-upload-image').attr('src', e.target.result);
                $(".ch-file-upload-content").show();
                // $('.image-title').html(input.files[0].name);
            };
      
          reader.readAsDataURL(input.files[0]);
      
        } else {
            removeUpload();
        }
      }
      
    removeUpload = function() {
        $('.ch-file-upload-input').val("")
        $(".ch-file-upload-content").hide();
        $('.ch-image-upload-wrap').show();
    }

    setImage = function(f) {
        var file = $("#ch_input_image")[0].files[0];
        const ch_input_image_container = $("#ch_input_image_container");

        // 확장자 체크
        if(!/\.(jpg|jpeg|png)$/i.test(file.name)){
            alert('이미지파일만 선택해 주세요.\n\n현재 파일 : ' + file.name);
    
            // 선택한 파일 초기화
            f.outerHTML = f.outerHTML;
            ch_input_image_container.text("");
        } else {
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
                    var dataURI = canvas.toDataURL("image/jpg");

                    sessionStorage.setItem("origin_image", dataURI);
                    $('img.origin-thumbnail').each(function(){
                        $(this)[0].src = dataURI;
                    });

                    temp_img_upload(dataURI);
                };
            };
        }
    }

    temp_img_upload = function(dataURI) {
        let userID = sessionStorage.getItem('login_id');
        userID = userID.replace("@", "__");
        userID = userID.replace(".", "__");
        
        $.ajax({
            url: "pallate/ch_style/temp_img_upload",
            type: 'post',
            data: {
                'dataURI' : dataURI,
                'userID' : userID
            },
            dataType: 'text',
            success: function(res) {
                origin_to_masterpiece(res);
            },
            error: function(error) {
                console.log('error', error);
            }
        });
    }

    origin_to_masterpiece = function(img_name) {
        let userID = sessionStorage.getItem('login_id');
        userID = userID.replace("@", "__");
        userID = userID.replace(".", "__");

        $.ajax({
            url: "pallate/ch_style/change_masterpiece",
            type: 'post',
            data: {
                'img_name': img_name,
                'userID' : userID
            },
            dataType: 'text',
            success: function(res) {
                const ch_output_image_container = $("#ch_output_image_container");
                let res_list = res.split('/');
                const master_name = res_list[res_list.length - 1];

                tg_str = '<div class="row ch-file-upload-box">' +
                            '<img src="' + res + '" class="ch-file-upload-image ch-image rounded">' +
                        '</div>' +
                        '<div class="ch-image-title-wrap row">' +
                            '<button type="button" class="btn btn-outline-success col-md-6 ch-image-btn" onclick="download_image(\'' + master_name + '\')">다운로드</button>' +
                        '</div>';
                
                ch_output_image_container.empty();
                ch_output_image_container.append(tg_str);
            },
            error: function(error) {
                console.log('error', error);
            }
        });
    }

    download_image = function(master_name) {
        console.log(master_name);
        // $.ajax({
        //     url: "pallate/ch_style/download_img",
        //     type: 'post',
        //     data: {
        //         'dataURI' : dataURI,
        //         'userID' : userID
        //     },
        //     dataType: 'text',
        //     success: function(res) {
        //         origin_to_masterpiece(res);
        //     },
        //     error: function(error) {
        //         console.log('error', error);
        //     }
        // });
    }
      
});