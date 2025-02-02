from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import bcrypt
import math

# Определение базового класса моделей
Base = declarative_base()

# Модель пользователя с добавлением email
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=False, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # Добавляем отношение к книгам
    books = relationship('Book', backref='owner', lazy='dynamic')

# Обновляем модель книги с геоданными
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String)
    cover_url = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

class UserDatabase:
    def __init__(self, db_url="postgresql://postgres:postgre@31.41.155.119:5432/derevyankin"):
        self.engine = create_engine(db_url, echo=False)  # Отключаем echo для логов SQL
        self.Session = sessionmaker(bind=self.engine)
        
        # Просто создаем таблицы, если их нет, без удаления
        Base.metadata.create_all(self.engine)
        print("База данных успешно инициализирована")
    
    def create_user_table(self):
        Base.metadata.create_all(self.engine)
        print("Таблица пользователей успешно создана или уже существует.")
    
    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def add_user(self, username: str, email: str, password: str):
        hashed_pwd = self.hash_password(password)
        session = self.Session()
        user = User(username=username, email=email, hashed_password=hashed_pwd.decode('utf-8'))
        session.add(user)
        session.commit()
        user_id = user.id
        session.close()
        return user_id

    def authenticate_user(self, email: str, password: str):
        session = self.Session()
        user = session.query(User).filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            user_id = user.id
            session.close()
            return user_id
        session.close()
        return None

    def get_user(self, email: str):
        session = self.Session()
        try:
            user = session.query(User).filter_by(email=email).first()
            if user:
                # Добавляем подсчет книг пользователя
                book_count = session.query(Book).filter_by(owner_id=user.id).count()
                result = {
                    'username': user.username, 
                    'email': user.email,
                    'book_count': book_count  # Добавляем количество книг
                }
                return result
            return None
        finally:
            session.close()

    def add_book(self, title: str, author: str, description: str, cover_url: str, owner_email: str, latitude: float = None, longitude: float = None):
        session = self.Session()
        try:
            owner = session.query(User).filter_by(email=owner_email).first()
            if not owner:
                raise Exception("Пользователь не найден")
            
            book = Book(
                title=title, 
                author=author, 
                description=description, 
                cover_url=cover_url, 
                owner_id=owner.id,
                latitude=latitude,
                longitude=longitude
            )
            session.add(book)
            session.commit()
            return book.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def list_books_nearby(self, latitude: float, longitude: float, radius: float):
        raise Exception("Функция поиска по координатам недоступна")

    def list_books(self, owner_email: str):
        session = self.Session()
        try:
            owner = session.query(User).filter_by(email=owner_email).first()
            if not owner:
                return []
            books = session.query(Book).filter_by(owner_id=owner.id).all()
            result = [{
                'id': b.id,
                'title': b.title,
                'author': b.author,
                'description': b.description,
                'cover_url': b.cover_url,
                'owner_id': b.owner_id  # Добавляем owner_id в результат
            } for b in books]
            return result
        finally:
            session.close()

    def delete_book(self, book_id: int, owner_email: str):
        session = self.Session()
        # Получаем книгу и её владельца
        book = session.query(Book).filter_by(id=book_id).first()
        if not book:
            session.close()
            raise Exception("Книга не найдена")
        owner = session.query(User).filter_by(id=book.owner_id).first()
        if owner.email != owner_email:
            session.close()
            raise Exception("Нет прав для удаления данной книги")
        session.delete(book)
        session.commit()
        session.close()

    def update_user(self, email: str, new_username: str):
        session = self.Session()
        user = session.query(User).filter_by(email=email).first()
        if not user:
            session.close()
            raise Exception("Пользователь не найден")
        user.username = new_username
        session.commit()
        session.close()

    def search_books(self, query: str):
        session = self.Session()
        try:
            # Изменяем запрос, чтобы получить информацию о владельце
            books = session.query(Book, User.email).join(User, Book.owner_id == User.id)\
                         .filter(Book.title.ilike(f"%{query}%")).all()
            result = [{
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'description': book.description,
                'owner_email': owner_email  # Добавляем email владельца
            } for book, owner_email in books]
            return result
        finally:
            session.close()

