const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});


function register(event) {
    event.preventDefault();

    const username1 = document.getElementById('name').value;
    const emailuser1 = document.getElementById('email').value;
    const password1 = document.getElementById('password').value;

    if (username1 === "" || emailuser1 === "" || password1 === "") {
        document.getElementById('message').innerText = "Заполните все поля.";
        return;
    }

    if (password1.length < 8) {
        document.getElementById('message').innerText = "Пароль должен содержать как минимум 8 символов.";
        return;
    }

    const existingUser = localStorage.getItem(username1);

    if (existingUser) {
        document.getElementById('message').innerText = "Пользователь уже существует.";
    } else {
        const hashedPassword = CryptoJS.SHA256(password1).toString();
        const userData = {
            email: emailuser1,
            password: hashedPassword
        };
        localStorage.setItem(username1, JSON.stringify(userData));
        document.getElementById('message').innerText = "Профиль создан!";
        console.log("Пользователь сохранён:", userData);
    }
}

function login(event) {
    event.preventDefault();
    
    const emailuser2 = document.getElementById('email1').value;
    const password2 = document.getElementById('password1').value;

    if (emailuser2 === "" || password2 === "") {
        document.getElementById('message1').innerText = "Заполните все поля.";
        return;
    }

    if (password2.length < 8) {
        document.getElementById('message1').innerText = "Пароль должен содержать как минимум 8 символов.";
        return;
    }

    let userFound = false;
    const hashedPassword = CryptoJS.SHA256(password2).toString();
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        const userData = JSON.parse(localStorage.getItem(key));

        if (userData && userData.email === emailuser2 && userData.password === hashedPassword) {
            document.getElementById('message1').innerText = "Вход выполнен!";
            localStorage.setItem('logged', JSON.stringify(true));

            userFound = true;
            break;
        }
    }

    if (!userFound) {
        document.getElementById('message1').innerText = "Неверный email или пароль.";
    }
}
