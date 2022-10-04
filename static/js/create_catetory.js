var arrInput = new Array(0);
var arrInputValue = new Array(0);
 
function addInput() {
  arrInput.push(arrInput.length);
  arrInputValue.push("");
  display();
}
 
function display() {
  document.getElementById('create').innerHTML="";
  for (intI=0;intI<arrInput.length;intI++) {
    document.getElementById('create').innerHTML+=createInput(arrInput[intI], arrInputValue[intI]);
  }
}
 
function saveValue(intId,strValue) {
  arrInputValue[intId]=strValue;
}  
 
function createInput(id,value) {
  return "<input name = 'cate' type='text' id='cate' onChange='javascript:saveValue("+ id +",this.value)' value='"+ value +"'><br>";
}
 
function deleteInput() {
  if (arrInput.length > 0) { 
     arrInput.pop(); 
     arrInputValue.pop();
  }
  display(); 
}

function submit() {
    const cate = document.getElementById('cate').value;
    $.ajax({
        type: "POST",
        url: `/plan/create/${cate}`,
    //     success: function (response) {
    //       if (response["exists"]) {
    //           $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
    //           $("#input-username").focus()
    //       } else {
    //           $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
    //       }
    //       $("#help-id").removeClass("is-loading")
    //   }
      })
}