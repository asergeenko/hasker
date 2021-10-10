# Hasker
## Poor man's stackoverflow

## Детали реализации
Каркас Django-приложения создан с помощью [cookiecutter](https://github.com/pydanny/cookiecutter-django) (с удалёнными впоследствии добавками вроде allauth по условию задания).
В качестве UI библиотеки используются [Bootstrap 4](https://getbootstrap.com/), для добавления тэгов [Slim Select](https://slimselectjs.com/) и [Crispy Forms](https://django-crispy-forms.readthedocs.io/) для красивой отрисовки форм.

## Тестирование
Приложение развёрнуто [здесь](http://80.78.254.59:9000/) в следующем окружении:
- Ubuntu 16.04
- nginx
- uwsgi
- Postgres 9.5
