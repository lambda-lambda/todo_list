const userApi = {}

userApi.signin = (username, password, callback) => {
    const path = '/api/user/signin'
    const user = {
        username: username,
        password: password,
    }

    postJSONRequest(path, user, callback)
}

/*
 '/api/user/all': 'all',
 '/api/user/delete': 'delete',
 '/api/user/password/update': 'update_password',
 '/api/user/signin': 'signin',
 '/api/user/signup': 'signup',
 '/api/user/username/update': 'update_username',
*/

userApi.signup = (username, password, callback) => {
    const path = '/api/user/signup'
    const user = {
        username: username,
        password: password,
    }

    postJSONRequest(path, user, callback)
}

const userView = {}

userView.signin = () => {
    const resultDiv = e('#id-div-signin-result')
    resultDiv.innerText = '登录成功 3 秒后跳转到 todo 主页'
    redirect('/todo/index')
}

userView.signup =() => {
    const resultDiv = e('#id-div-signup-result')
    resultDiv.innerText = '注册成功 3 秒后跳转到 登录 主页'
    redirect('/signin')
}

const userEvent = {}

userEvent.signin = () => {
    bind('#id-button-signin', 'click', event => {
        const username = value('#id-input-username')
        const password = value('#id-input-password')

        userApi.signin(username, password, userView.signin)
    })
}

userEvent.signup = () => {
    bind('#id-button-signup', 'click', event => {
        const username = value('#id-input-username')
        const password = value('#id-input-password')

        userApi.signup(username, password, userView.signup)
    })
}
