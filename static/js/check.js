

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