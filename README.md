# Django app map
Карта Джанго приложения по папкам, файлам, объектам в файлах
## accounts
Приложение Джанго отвечающее за работу с пользователями
### templatetags/has_group.has_group
Функция для шаблонов, принадлежит ли пользователь группе.
### middleware.UserAuth
Класс для блокировки всех не авторизованных соединений, кроме исключений - страниц входа - выхода и статических файлов.
### models.UserMeta
Метаданные о пользователех.
### urls
Описание страниц, за которые отвечает приложение
### views
##### .UserCreate
[ GET ] - страница с формой для создания пользователей
[ POST ] - отправка и обработка формы для создания пользователей
##### .UsersList
[ GET ] - страница со списком всех пользователей
##### .UserDetail
[ GET ] - страница с подробной информацие о пользователе
##### .UserLogin
[ POST ] - обработка формы для входа пользователей
## customs
Техническая папка, вещи напряму не связанные с Джанго
### responce_handler.responce_handler
Декоратор обрабатывающий запросы на 403 и 404 ошибки, из-за разграничения на клиентов и сотрудников пришлось его сделать. После своей работы добавляет список с некоторой информацией, которую можно использовать.
### sftp_handler.Sftp_user
Класс для создания пользователя на SFTP, т.к. при регистрации пользователя, кроме доступа из веб - должен быть еще доступ и по SFTP. 

## main
Приложение Джанго отвечающее за работу с патчами (объектами)
### customs.patch.Patch
Используется при загрузки объектов.
### customs.patch.PatchParser
Используется при загрузки объектов. Просматривает содержимое.
### models
##### .Patch
Информация о патче
##### .Category
Катекория для патча
##### .SubCategory
Подкатегория для патча
##### .PatchMeta
Метаданные о патче
##### .PatchPermissions
Права доступа для клиентов
### urls
Описание страниц, за которые отвечает приложение
### views
##### .Patch
[ GET ] - страница с подробной информацие об объекте
##### .PatchPermissions
[ GET ] - json с правами на объект для конкретного пользователя
[ POST ] - обработка формы и назначение прав на объект для пользователя
##### .PatchUpload
[ GET ] - страница с формой для загрузки объектов
[ POST ] - обработка формы и проверка самого объекта перед загрузкой
##### .PatchDownload
[ GET ] - получение - скачивание объекта
##### .PatchesList
[ GET ] - страница со списком всех объектов

## publics
Кастомные загрузки клиентов
### customs.file.CustomFile
Используется для работы с файлами пользователей
### models.CustomFile
Информация о файле загруженном клиентом.

### urls
Описание страниц, за которые отвечает приложение
### views
##### .CustomFile
Информация о файле 
##### .CustomFileUpload
[ GET ] - страница с формой для загрузки файлов
[ POST ] - отправка и обработка формы для загрузки файлов
##### .CustomFilesList
[ GET ] - страница со списком всех файлов

##### .CustomFileDownload
[ GET ] - получение - скачивание файла
## registry
Информация о настройках Джанго
## static_second
Статические файлы, при сборке и развертывании попадают в папку static
## templates
Шаблоны
## user_logs
Приложение Джанго отвечающее за логи
### customs.log_entry.LogEntry
Используется для работы с Логами
### models.LogEntry
Информация о записи в журнале логов.
### urls
Описание страниц, за которые отвечает приложение
### views.LogsList
[ GET ] - страница со списком всех логов 

