document.querySelectorAll('nav ul li a').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    // Снимаем активный класс со всех ссылок и контента
    document.querySelectorAll('nav ul li a').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    // Активируем выбранную вкладку
    link.classList.add('active');
    const target = link.getAttribute('data-target');
    document.getElementById(target).classList.add('active');
  });
});

// Функция для обновления списка книг (Мои книги)
async function refreshBooks(email) {
  let response = await eel.list_books(email)();
  if (response.status === 'success') {
    const booksList = document.getElementById('booksList');
    booksList.innerHTML = "";
    response.books.forEach(book => {
      let li = document.createElement('li');
      // Формирование информации и кнопок
      li.innerHTML = `<span>"${book.title}" — ${book.author}</span>`;
      // Добавляем кнопку удаления книги
      let delBtn = document.createElement('button');
      delBtn.textContent = "Удалить";
      delBtn.addEventListener('click', () => deleteBook(book.id, email));
      li.appendChild(delBtn);
      booksList.appendChild(li);
    });
  } else {
    console.error("Ошибка загрузки книг: " + response.message);
  }
}

// Функция для отображения результатов геопоиска
async function displayNearbyBooks(lat, lng, radius) {
  let response = await eel.search_books_nearby(lat, lng, radius)();
  const resultsDiv = document.getElementById('searchResults');
  resultsDiv.innerHTML = "";
  // Скрываем контейнер карты по умолчанию
  document.getElementById('mapContainer').style.display = 'none';
  if (response.status === 'success') {
    if(response.books.length) {
      let ul = document.createElement('ul');
      response.books.forEach(book => {
        let li = document.createElement('li');
        li.innerHTML = `<span>"${book.title}" — ${book.author} (расстояние: ${book.distance} км)</span>`;
        ul.appendChild(li);
      });
      resultsDiv.appendChild(ul);
    } else {
      resultsDiv.textContent = "Нет книг в указанном радиусе.";
    }
  } else {
    console.error("Ошибка геопоиска: " + response.message);
  }
}

// Обработка формы добавления книги
document.getElementById('addBookForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const title = document.getElementById('bookTitle').value;
  const author = document.getElementById('bookAuthor').value;
  const description = document.getElementById('bookDescription').value;
  const owner_email = document.getElementById('bookOwnerEmail').value;
  
  let response = await eel.add_book(title, author, description, "", owner_email, null, null)();
  if (response.status === 'success') {
    refreshBooks(owner_email);
    // Добавляем обновление профиля после успешного добавления книги
    loadProfile(owner_email);
    // Очищаем форму после успешного добавления
    this.reset();
    // Восстанавливаем email в поле
    document.getElementById('bookOwnerEmail').value = owner_email;
  } else {
    console.error("Ошибка добавления книги: " + response.message);
  }
});

document.getElementById('titleSearchForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  let query = document.getElementById('searchQuery').value.trim();
  let response = await eel.search_books(query)();
  const resultsDiv = document.getElementById('searchResults');
  resultsDiv.innerHTML = "";
  if(response.status === 'success') {
    if(response.books.length) {
      let ul = document.createElement('ul');
      response.books.forEach(book => {
        let li = document.createElement('li');
        li.innerHTML = `
          <div class="book-info">
            <span class="book-title">"${book.title}" — ${book.author}</span>
            <div class="book-contact">
              <span class="contact-label">Контакт владельца:</span>
              <a href="mailto:${book.owner_email}">${book.owner_email}</a>
            </div>
          </div>
        `;
        ul.appendChild(li);
      });
      resultsDiv.appendChild(ul);
    } else {
      resultsDiv.textContent = "Ничего не найдено.";
    }
  } else {
    console.error("Ошибка поиска: " + response.message);
  }
});

// При загрузке вкладки "Мои книги" обновляем список (если email уже введён)
document.addEventListener('DOMContentLoaded', () => {
  let owner_email = document.getElementById('bookOwnerEmail').value;
  if(owner_email) {
    refreshBooks(owner_email);
    loadProfile(owner_email);
  }
});

// Функция загрузки профиля по Email
async function loadProfile(email) {
  let response = await eel.get_profile(email)();
  const profileDiv = document.getElementById('profileInfo');
  profileDiv.innerHTML = "";
  
  if(response.status === 'success' && response.user) {
    profileDiv.innerHTML = `
      <p><strong>Имя пользователя:</strong> ${response.user.username}</p>
      <p><strong>Email:</strong> ${response.user.email}</p>
    `;
    
    // Обновляем количество книг из данных профиля
    document.getElementById('profileBookCount').textContent = response.user.book_count || '0';
  } else {
    profileDiv.textContent = "Не удалось загрузить информацию профиля.";
    document.getElementById('profileBookCount').textContent = '0';
  }
}

// Обработка формы редактирования профиля
document.getElementById('profileEditForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('bookOwnerEmail').value;
  const newUsername = document.getElementById('newUsername').value.trim();
  if(email && newUsername) {
    let response = await eel.update_profile(email, newUsername)();
    if(response.status === 'success') {
      loadProfile(email);
    } else {
      console.error("Ошибка обновления профиля: " + response.message);
    }
  }
});

// Функция для удаления книги
async function deleteBook(bookId, ownerEmail) {
  if(confirm("Удалить книгу?")) {
    let response = await eel.delete_book(bookId, ownerEmail)();
    if(response.status === 'success') {
      refreshBooks(ownerEmail);
      // Добавляем обновление профиля после успешного удаления книги
      loadProfile(ownerEmail);
    } else {
      console.error("Ошибка удаления книги: " + response.message);
    }
  }
}

// Функция для отображения книги на карте через Google Maps
function showBookOnMap(lat, lng) {
  // Показываем контейнер карты (если требуется, можно интегрировать реальные карты)
  document.getElementById('mapContainer').style.display = 'block';
  // Открываем Google Maps в новой вкладке
  window.open(`https://www.google.com/maps?q=${lat},${lng}`, '_blank');
}
