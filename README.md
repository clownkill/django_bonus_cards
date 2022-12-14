# Веб-приложение для управления дисконтными картами

![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)

Веб-приложение (REST API) для управления дисконтными картами.

[Документация Openapi](http://127.0.0.1:8000/api/schema/swagger-ui/)


### Требования

Для запуска проекта необходимо:
- Python 3.10

### Переменные окружения

Определите переменные окружения в файле `.env` в формате: `ПЕРЕМЕННАЯ=значение`:
- `DEBUG` — дебаг-режим. Поставьте `True` для включения, `False` — для 
выключения отладочного режима. По умолчанию дебаг-режим отключен.
- `SECRET_KEY` — секретный ключ проекта, например: `fwei3$@K!fjslfji;erfkdsewyiwerlfskfhfjdslfsf3`
- `ALLOWED_HOSTS` — список разрешенных хостов.

## Установка и запуск на локальном сервере

- Скачайте код из репозитория
- Установите зависимости командой:
```shell
pip install -r requirements.txt
```
- Создайте файл `.env` в корневой папке и пропишите необходимые переменные 
окружения в формате: `ПЕРЕМЕННАЯ=значение`


- Выполните миграцию БД:
```commandline
python manage.py makemigrations
python manage.py migrate
```
- Запустите скрипт командой:
```commandline
python manage.py runserver
```

### Настройка деактивации карт с истекшим сроком действия

Для настройки деактивации карт с истекшик сроком действия необходимо [создать задачу](http://127.0.0.1:8000/admin/django_q/schedule/).

В поле `Func` указать  `cards.tasks.deactivate_expired_cards`.

В поле `Schedule Type` задать переодичность запуска задачи.

В поле `Repeats` задать количество повторений (-1 - всегда).

В поле `Next Run` задать время следующего запуска.

Для запуска задачи не останавливая сервера выполнить комманду:
```commandline
python manage.py qcluster 
```

### Панель администратора

Панель администратора сайта доступна по адресу `sitename/admin/`. Для
создания учетной записи администратора используйте команду:
```commandline
python manage.py createsuperuser
```