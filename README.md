ДЗ 11. annotate aggregate


Создать новый проект. (Не забыть все обязательные шаги - secret key, flake8, travis, gitignore, requirements, readme)
Добавить ddt или silk. создать новое приложение. использовать в приложении модели из джанго
доки (https://docs.djangoproject.com/en/3.2/topics/db/aggregation/)
заполнить базу большим количеством данных и предоставить мне возможность так же быстро заполнить базу:

1) создать менеджмент команду
2) создать фикстуры (dumpdata loaddata менеджмент команды)

Добавить модели в админку. Постараться использовать больше функционала (inline обязательно)
создать несколько темплейтов, вьюшек, урлов для вывода данных по моделям. (Только вывод данных из базы, без форм)
в вьюшках и темплейтах нужно стараться минимизировать количество запросов в базу.
(Префетчи, селекты, аннотации, агрегации)
на страницах выводить списки (в таблицах) или единичный элемент - например список магазинов или одного автора. Помимо
полей из модели обязательно выводить что-то ещё полученное с использованием «Префетчи, селекты, аннотации, агрегации».
количество доступных страниц - 8 (по списку и дитейлу на каждую модель)
со списка можно попасть на дитейл по ссылке которую вы должны сгенерировать в темплейте для каждой страницы. с дитейл
страницы должна быть ссылка на список.