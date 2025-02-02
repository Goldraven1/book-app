// Обработка входа: теперь используем email вместо username
document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;
  let response = await eel.login(email, password)();
  if (response.status === 'success') {
    window.location.href = "dashboard.html";
  } else {
    // Вместо alert можно реализовать иной способ уведомления
    console.error("Ошибка входа: " + response.message);
  }
});

// Переключение форм
document.getElementById('showRegister').addEventListener('click', function(e) {
  e.preventDefault();
  document.getElementById('loginForm').style.display = 'none';
  document.getElementById('registerForm').style.display = 'block';
});
document.getElementById('showLogin').addEventListener('click', function(e) {
  e.preventDefault();
  document.getElementById('registerForm').style.display = 'none';
  document.getElementById('loginForm').style.display = 'block';
});

// Обработка регистрации: передаём email вместе с username и password
document.getElementById('registerForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const username = document.getElementById('regUsername').value;
  const email = document.getElementById('regEmail').value;
  const password = document.getElementById('regPassword').value;
  const confirmPassword = document.getElementById('regConfirmPassword').value;
  if (password !== confirmPassword) {
    console.error("Пароли не совпадают!");
    return;
  }
  let response = await eel.register(username, email, password)();
  if (response.status === 'success') {
    window.location.href = "dashboard.html";
  } else {
    console.error("Ошибка регистрации: " + response.message);
  }
});
