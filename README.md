# Test-work
Задание
Необходимо написать веб сервис, который конвертирует файлы формата 'png', 'bmp', 'jpg', 'jpeg', 'eps' в 'pdf'.
По определенному endpoint’у необходимо загружать файлы и отложено конвертировать.
По-другому endpoint’у необходимо получить полный список загруженных файлов, также с возможностью выгрузить один из них. Как формате загружаемом, так и в формате pdf.

Примечания:

    1. Необходимо использовать веб фреймворки fastapi, litestar или можно написать на aiohttp [это со звездочкой 😊]
    2. Для работы с базой необходимо использовать sqlalchemy (опять же выбор СУБД на свое усмотрение)
    3. Было бы классно если файлы привязывались к определенной сессии и выгружались для определенной сессии
