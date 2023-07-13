const accept = document.querySelector(".accept-tos")
const tos = document.querySelector(".ToS")
const wrap = document.querySelector(".signup-wrap")

accept.addEventListener("click",e=> {
    tos.remove()
    makeSignUpForm()
})


function makeSignUpForm(){
    const label_username = document.createElement("label")
    label_username.for = "username"
    label_username.innerHTML = "username"

    const username = document.createElement("input")
    username.name = "username"

    const label_email = document.createElement("label")
    label_email.for = "email"
    label_email.innerHTML = "email"

    const email = document.createElement("input")
    email.name = "email"

    const label_role = document.createElement("label")
    label_role.for = "role"
    label_role.innerHTML = "select your role"

    const role = document.createElement("select")
    role.name = "role"

    const player = document.createElement("option")
    player.value = "player"
    player.selected = true
    player.innerHTML = "player"

    const dm = document.createElement("option")
    dm.value = "dm"
    dm.innerHTML = "dm"

    role.appendChild(player)
    role.appendChild(dm)

    const password_req = document.createElement("h4")
    password_req.innerHTML = "password must be at least 8 characters long and max 16 characters"

    const label_password = document.createElement("label")
    label_password.for = "password"
    label_password.innerHTML = "password"

    const password = document.createElement("input")
    password.name = "password"
    password.type = "password"

    const label_password2 = document.createElement("label")
    label_password2.for = "password2"
    label_password2.innerHTML = "re-enter password"

    const password2 = document.createElement("input")
    password2.name = "password2"
    password2.type = "password"

    const finish = document.createElement("button")
    finish.innerHTML = "sign-up"
    finish.name = "button"
    finish.value = "sign-up"

    wrap.appendChild(label_username)
    wrap.appendChild(username)
    wrap.appendChild(label_email)
    wrap.appendChild(email)
    wrap.appendChild(label_role)
    wrap.appendChild(role)
    wrap.appendChild(label_password)
    wrap.appendChild(password)
    wrap.appendChild(password_req)
    wrap.appendChild(label_password2)
    wrap.appendChild(password2)
    wrap.appendChild(finish)
}