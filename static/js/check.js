function check_e(){
  const t = document.getElementById('email').value;
  console.log(t);
  $.ajax({
    type: "POST",
    url: `/user/checke/${t}`,
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
  const t = document.getElementById('id').value;
  console.log(t);
  $.ajax({
    type: "POST",
    url: `/user/checkDup/${t}`,
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