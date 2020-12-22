$(document).ready(function(){
    setImage = function(f) {
        var file = f.files[0];
        const image_container = $("#ch_image_container");

        // 확장자 체크
        if(!/\.(jpg|jpeg|png)$/i.test(file.name)){
            alert('이미지파일만 선택해 주세요.\n\n현재 파일 : ' + file.name);
    
            // 선택한 파일 초기화
            f.outerHTML = f.outerHTML;
            image_container.text("");
        } else {
            // FileReader 객체 사용
            var reader = new FileReader();

            // 파일 읽기가 완료되었을때 실행
            reader.onload = function(rst){
                image_container.append('<img src="' + rst.target.result + '">');
            }
            // 파일을 읽는다
            reader.readAsDataURL(file);

            // temp_img_upload(file);
        }
    }

    temp_img_upload = function(img_f) {
        // var original_name = img_f.name.split(".")[0];
        // var img_extension = img_f.name.split(".")[1];

        var data = new FormData($('ch_upload_image'));
        console.log(data);
        $.ajax({
            url: 'ch_style/temp_img_upload',
            type: 'post',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(res) {
                console.log(res)
            },
            error: function(msg) {
                console.log(msg)
            }
        });
        return false;



        
        $("#original_name").val(img_f.name);

        // console.log($("#original_name").val());

        $.ajax({
            url: "ch_style/temp_img_upload",
            type: 'post',
            // data: {
            //     'img_f': img_f,
            //     'original_name' : original_name,
            //     'img_extension' : img_extension
            // },
            data: {'img_f':img_f},
            dataType: 'text',
            success: function(res) {
                console.log('success', res);
            },
            error: function(error) {
                console.log('error');
            }
        });
    }

    origin_to_masterpiece = function(dataURI) {
        $.ajax({
            url: "ch_style/change_masterpiece",
            type: 'post',
            data: {
                'dataURI': dataURI
            },
            dataType: 'text',
            success: function(res) {
                console.log('success', res);
            },
            error: function(error) {
                console.log('error');
            }
        });
    }
});