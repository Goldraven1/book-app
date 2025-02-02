import eel
from base import UserDatabase

class RouteHandler:
    def __init__(self):
        self.db = UserDatabase()
        self.db.create_user_table()

    def register_user(self, username: str, email: str, password: str):
        try:
            user_id = self.db.add_user(username, email, password)
            return {'status': 'success', 'user_id': user_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def login_user(self, email: str, password: str):
        user_id = self.db.authenticate_user(email, password)
        if user_id is not None:
            return {'status': 'success', 'user_id': user_id}
        else:
            return {'status': 'error', 'message': 'Неверный логин или пароль'}

    def add_book(self, title: str, author: str, description: str, cover_url: str, owner_email: str, latitude: float = None, longitude: float = None):
        try:
            book_id = self.db.add_book(title, author, description, cover_url, owner_email, latitude, longitude)
            return {'status': 'success', 'book_id': book_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def list_books(self, owner_email: str):
        try:
            books = self.db.list_books(owner_email)
            return {'status': 'success', 'books': books}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def list_books_nearby(self, latitude: float, longitude: float, radius: float):
        try:
            books = self.db.list_books_nearby(latitude, longitude, radius)
            return {'status': 'success', 'books': books}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_profile(self, email: str):
        try:
            user = self.db.get_user(email)
            if user:
                return {'status': 'success', 'user': user}
            else:
                return {'status': 'error', 'message': 'Пользователь не найден'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_book(self, book_id: int, owner_email: str):
        try:
            self.db.delete_book(book_id, owner_email)
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_profile(self, email, new_username):
        try:
            self.db.update_user(email, new_username)
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def search_books(self, query):
        try:
            books = self.db.search_books(query)
            return {'status': 'success', 'books': books}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

route_handler = RouteHandler()

@eel.expose
def register(username, email, password):
    return route_handler.register_user(username, email, password)

@eel.expose
def login(email, password):
    return route_handler.login_user(email, password)

@eel.expose
def add_book(title, author, description, cover_url, owner_email, latitude=None, longitude=None):
    try:
        return route_handler.add_book(title, author, description, cover_url, owner_email, latitude, longitude)
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@eel.expose
def list_books(owner_email):
    return route_handler.list_books(owner_email)

@eel.expose
def search_books_nearby(latitude, longitude, radius):
    return {'status': 'error', 'message': 'Геопоиск отключён'}

@eel.expose
def get_profile(email):
    return route_handler.get_profile(email)

@eel.expose
def delete_book(book_id, owner_email):
    return route_handler.delete_book(book_id, owner_email)

@eel.expose
def update_profile(email, new_username):
    try:
        return route_handler.update_profile(email, new_username)
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@eel.expose  # Добавляем декоратор для экспорта функции
def search_books(query):
    return route_handler.search_books(query)

# Удалить или закомментировать старое определение функции search_books
# def search_books(query):
#     return route_handler.search_books(query)
