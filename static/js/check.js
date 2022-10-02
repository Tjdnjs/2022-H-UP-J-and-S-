// function is_userid(asValue) {
//   var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{4,10}$/;
//   return regExp.test(asValue);
// }

// function is_password(asValue) {
//   var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,16}$/;
//   return regExp.test(asValue);
// }

function check_e(){
  const e = document.getElementById('email').value;
  console.log(e);
  $.ajax({
    type: "POST",
    url: `/user/checke/${e}`,
    success: function (response) {
      if (response["exists"]) {
          $("#help-e").text("이미 존재하는 이메일입니다.").removeClass("is-safe").addClass("is-danger")
          $("#input-useremail").focus()
      } else {
          $("#help-e").text("사용할 수 있는 이메일입니다.").removeClass("is-danger").addClass("is-success")
      }
      $("#help-e").removeClass("is-loading")
  }
  })
}

function check_dup(){
  const id = document.getElementById('id').value;
  console.log(id);
  $.ajax({
    type: "POST",
    url: `/user/checkDup/${id}`,
    success: function (response) {
      if (response["exists"]) {
          $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
          $("#input-username").focus()
      } else {
          $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
      }
      $("#help-id").removeClass("is-loading")
  }
  })
}

function check_pw(){
  const pw = document.getElementById('password').value;
  let pw_check = document.getElementById('pw_check').value;
  console.log(pw, pw_check)
  if (pw !== pw_check){
    $("#help-pw").text("비밀번호가 일치하지 않습니다").removeClass("is-danger").addClass("is-success")
  }
  else {
    $("#help-pw").text("비밀번호가 일치합니다").removeClass("is-success").addClass("is-success")
  }
}