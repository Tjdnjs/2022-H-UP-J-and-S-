// function is_username(asValue) {
//     var regExp = /^[a-zA-z0-9]{4,10}{2,10}$/;
//     return regExp.test(asValue);
// }

// function is_nickname(asValue) {
//     var regExp = /^[가-힣ㄱ-ㅎa-zA-Z0-9._-]{2,}$/;
//     return regExp.test(asValue);
// }
// function is_password(asValue) {
//     var regExp = /^[a-zA-z0-9]{8,16}$/;
//     return regExp.test(asValue);
// }

function check_dup(){
    let username = $("#input-username").val()
    // if (username == "") {
    //     $("#help-id").text("아이디를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
    //     $("#input-username").focus()
    //     return;
    // }
    // if (!is_username(username)) {
    //     $("#help-id").text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이").removeClass("is-safe").addClass("is-danger")
    //     $("#input-username").focus()
    //     return;
    // }
    $("#help-id").addClass("is-loading")
    $.ajax({
        type: "POST",
        url: "/user/checkDup",
        data: {
            id: username
        },
        success: function (response) {
            if (response["exists"]) {
                $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
                $("#input-username").focus()
            } else {
                $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
            }
            $("#help-id").removeClass("is-loading")
        }
    });
}
