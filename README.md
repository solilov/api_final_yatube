# "REST API YaTube"

### Описание
  Учебный API для проекта социальной сети из курса Python разработчик от Яндекс Практикум
  
### Запуск
  - Клонируйте проект в свою рабочую директорию на компьютере
```html
    git clone/<путь репозитория>
```
  - Перейдите в директорию с проектом
```html
    ls <путь до директории>
```
  - Создать и активировать виртуальное окружение

```html
    python3 -m venv venv
```
```html
    source/venv/bin/activate
```
  - Устанавливаем зависимости
```html
    pip install -r requirements.txt 
```
  - Выполняем миграции
```html
    python manage.py migrate 
```
  - Запускаем сервер
```html
    python manage.py runserver
```

### Используемые технологии:
  - Python 3.7
  - Django
  - Django REST Framework
