# Hasker
## Poor man's stackoverflow



## Детали реализации
Каркас Django-приложения создан с помощью [cookiecutter](https://github.com/pydanny/cookiecutter-django) (с удалёнными добавками вроде allauth по условию задания).
В качестве UI библиотеки используются [Bootstrap 4](https://getbootstrap.com/), для добавления тэгов [Slim Select](https://slimselectjs.com/) и [Crispy Forms](https://django-crispy-forms.readthedocs.io/) для красивой отрисовки форм.
Почта отправляется с помощью **postfix** и в GMail по умолчанию попадет в спам.

## Django-приложения

### qa
Логика, связанная с вопросами и ответами, включая оценки.

#### Модели
- [**Tag**](https://github.com/asergeenko/hasker/blob/5149e3c2c0eec7f3855112ca4b833b9920a73335/hasker/qa/models.py#L11) - тэги вопросов
- [**AbstractPost**](https://github.com/asergeenko/hasker/blob/5149e3c2c0eec7f3855112ca4b833b9920a73335/hasker/qa/models.py#L18) - абстрактная модель, от которой наследуются **Answer** и **Question**
- [**Question**](https://github.com/asergeenko/hasker/blob/5149e3c2c0eec7f3855112ca4b833b9920a73335/hasker/qa/models.py#L26) - вопросы
- [**Answer**](https://github.com/asergeenko/hasker/blob/5149e3c2c0eec7f3855112ca4b833b9920a73335/hasker/qa/models.py#L36) - ответы

<img src="https://github.com/asergeenko/hasker/raw/main/docs/img/abstract_post.png"/>

- [**AbstractVote**](https://github.com/asergeenko/hasker/blob/5149e3c2c0eec7f3855112ca4b833b9920a73335/hasker/qa/models.py#L48) - абстрактная модель, от которой наследуются **VoteQuestion** и **VoteAnswer**
- [**VoteQuestion**](https://github.com/asergeenko/hasker/blob/5149e3c2c0eec7f3855112ca4b833b9920a73335/hasker/qa/models.py#L57) - голоса за вопросы
- [**VoteAnswer**](https://github.com/asergeenko/hasker/blob/5149e3c2c0eec7f3855112ca4b833b9920a73335/hasker/qa/models.py#L66) - голоса за ответы

<img src="https://github.com/asergeenko/hasker/raw/main/docs/img/abstract_vote.png"/>

### users
Логика, связанная с управлением пользователями

#### Модели
- [**User**](https://github.com/asergeenko/hasker/blob/a17519d65130ce4cbc3b1612786125b49b5a9bd5/hasker/users/models.py#L7) - данные пользователей

## Тестирование

    pytest

Приложение развёрнуто [здесь](http://80.78.254.59:9000/) в следующем окружении:
- Ubuntu 16.04
- nginx
- uwsgi
- Postgres 9.5
