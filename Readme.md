Приложение для создания продуктов, уроков и групп для студентов.

Для запуска необходимо:

1. в папке src/config/ создать файл db.sqlite3;
2. применить миграции командой python manage.py migrate;
3. создать пользователя командой python manage.py createsuperuser;
4. запустить приложение командой python manage.py runserver.
Все комады запуска выполняются из папки /src

После запуска OpenAPI доступен по адресу: http://127.0.0.1:8000/api/schema/swagger-ui/
В ОpenAPI доступно:

1. Добавление студента к продукту:
- в случае, если продукт уже стартовал, студент добавляется в наименее заполненную группу. Если свободных мест в группах нет, возвращается ошибка;
- в случае, если продукт не стартовал, студент добавляется в наиболее заполненную группу, если свободной группы нет, автоматически создается новая группа. После добавления студента происходит балансировка загруженности групп таким образом, чтобы количество в каждой группе не отличилось более чем на 1 (за исключением "пустых" групп).
2. просмотр всех продуктов с выводом информации по продукту и количеству связанных уроков;
3. просмотр всех уроков по конкретному продукту с информаций по каждому уроку.

Админ панель доступна по адресу: http://127.0.0.1:8000/admin/
Администратору доступно: создание продукта, уроков и групп для продукта.