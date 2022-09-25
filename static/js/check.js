const id = document.querySelector('user_id')
const test1 = () => {
  const isValid = input.validity.valid
  if (!isValid) {
    input.setCustomValidity('올바른 아이디 형식이 아닙니다')
    input.reportValidity()
  }
}

id.addEventListener('change', test1)

const pw = document.querySelector('user_pw')
const test2 = () => {
  const isValid = input.validity.valid
  if (!isValid) {
    input.setCustomValidity('올바른 비밀번호 형식이 아닙니다')
    input.reportValidity()
  }
}

id.addEventListener('change', test2)