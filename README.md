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
- [**Tag**](https://github.com/asergeenko/hasker/blob/47616c9d35deffd1d0b7619360719efacb3aca96/hasker/qa/models.py#L6) - тэги вопросов
- [**AbstractPost**](https://github.com/asergeenko/hasker/blob/47616c9d35deffd1d0b7619360719efacb3aca96/hasker/qa/models.py#L13) - абстрактная модель, от которой наследуются **Answer** и **Question**
- [**Question**](https://github.com/asergeenko/hasker/blob/47616c9d35deffd1d0b7619360719efacb3aca96/hasker/qa/models.py#L21) - вопросы
- [**Answer**](https://github.com/asergeenko/hasker/blob/47616c9d35deffd1d0b7619360719efacb3aca96/hasker/qa/models.py#L31) - ответы

<img src="https://github.com/asergeenko/hasker/raw/main/docs/img/abstract_post.png"/>

- [**AbstractVote**](https://github.com/asergeenko/hasker/blob/47616c9d35deffd1d0b7619360719efacb3aca96/hasker/qa/models.py#L43) - абстрактная модель, от которой наследуются **VoteQuestion** и **VoteAnswer**
- [**VoteQuestion**](https://github.com/asergeenko/hasker/blob/47616c9d35deffd1d0b7619360719efacb3aca96/hasker/qa/models.py#L52) - голоса за вопросы
- [**VoteAnswer**](https://github.com/asergeenko/hasker/blob/47616c9d35deffd1d0b7619360719efacb3aca96/hasker/qa/models.py#L61) - голоса за ответы

<img src="https://github.com/asergeenko/hasker/raw/main/docs/img/abstract_vote.png"/>

### users
Логика, связанная с управлением пользователями

#### Модели
- [**User**](https://github.com/asergeenko/hasker/blob/47616c9d35deffd1d0b7619360719efacb3aca96/hasker/users/models.py#L7) - данные пользователей

## Тестирование

    pytest

Приложение развёрнуто [здесь](http://80.78.254.59:9000/) в следующем окружении:
- Ubuntu 16.04
- nginx
- uwsgi
- Postgres 9.5
