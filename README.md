# Django Image Share

## Кратко о проекте

Данный проект представляет собой результат моей практики
для 2 семестра 3 курса института ЮРГПУ (НПИ) им. Платова, в котором я
сейчас прохожу обучение. Тема была произвольная, поэтому я решил выбрать
проект по своей будущей (надеюсь) специальности, а именно ВЕБ-разработке.
Сам django-проект представляет собой веб-приложение для загрузки/выгрузки
изображений.

---

## TODO список

- [x] Базовый каркас проекта с настроенной базой данных (PostgreSQL)
      и настроенным окружением с сокрытием private-only переменных (SECRET_KEY,
      PSQL_PASSWORD и т.д.).
- [x] Настроить виртуальное окружение проекта (в данном случае, poetry).
- [ ] Настроить отладку проекта:
  - [x] Установить django-debug-toolbar.
  - [x] Прописать работу со static и media-файлами в DEBUG-режиме.
- [x] Запрограммировать базовый вывод добашней страницы с навигационной
      панелью.
- [x] Запрограммировать модель для базы данных и совершить миграцию.
- [ ] реализовать систему аутентификации и авторизации на сайте.
- [ ] Реализовать CRUD для изображений:
  - [ ] Написать форму загрузки/выгрузки изображения.
  - [ ] Реализовать вывод всех добавленных изображений со ссылками на них.
  - [ ] Реализовать возможно удалять изображение или изменять его содержимое
        для авторов.
- [ ] Сделать личный кабинет пользователя; перенести туда возможность
      публиковать картинки.
- [ ] Мелкий функционал:
  - [ ] Реализовать форму поиска картинок.
  - [ ] Реализовать пагинацию списка картинок.

## Опциональный TODO список

- [ ] Реализовать не только поиск по тегам, но и по категориям.
- [ ] Оптимизировать выдачу картинок (AJAX-запросы или что-нибудь ещё).
- [ ] Начать вести статистику популярности картинок (лайки/дизлайки,
      активность в комментариях).
- [ ] Попробовать создать систему рекомендаций.

**Списки будет пополнять по мере работы моего воображения.**

---

## Запуск проекта

В проекте используется [poetry](https://github.com/python-poetry/poetry) -
менеджер зависимостей. Для его установки на OSX / Linuxosx / linux /
bashonwindows используейте команду:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

```

Для Windows:

```PowerShell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -

```

Для успешной установки всех зависимостей и запуска виртуального окружения
необходимо запустить последовательно следующие команды в консоли:

```bash
git clone git@github.com:ALittleMoron/django_imageShare.git
cd django_imageShare
poetry install
poetry shell
```
