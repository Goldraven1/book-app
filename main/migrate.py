from main.base import UserDatabase

def main():
    db = UserDatabase()
    try:
        db.create_user_table()
    except Exception as e:
        print("Ошибка при создании таблицы:", e)

if __name__ == "__main__":
    main()
