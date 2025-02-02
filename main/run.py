import os
import eel
import route

# Изменяем cwd на корневую папку проекта
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

eel.init('web')

if __name__ == '__main__':
    eel.start('main.html', size=(1920, 1080))