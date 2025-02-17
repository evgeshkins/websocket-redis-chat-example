# websocket-redis-chat-example - простейший чат, реализующий паттерн pubsub с использованием протокола Websocket и NoSQL Redis.
Чат, содержащий поле ввода текста для отправки, список клиентов онлайн, виджет вывода отправленных и принятых сообщений. <br>
## Стек
- Python 3.10 <br>
- Redis <br>
- Websocket <br>
- Python Tornado <br>
## Использование
1. Клонируйте репозиторий: <br>
```git clone https://github.com/evgeshkins/websocket-redis-chat-example.git . ``` <br>
2. Создайте виртуальное окружение: <br>
```python -m venv venv``` <br>
либо <br>
```py -m venv venv``` <br>
3. Активируйте виртуальное окружение: <br>
На Windows: <br>
```.venv\Scripts\activate``` <br>
На Linux: <br>
```source venv/bin/activate``` <br>
4. Установите библиотеки: <br>
```pip install -r requirements.txt``` <br>
5. Создайте файл .env в корне проекта и внесите туда значения следующих переменных: <br>
```python
REDIS_HOST=хост для NoSQL Redis 
REDIS_PORT=порт для NoSQL Redis
TORNADO_PORT=порт для фреймворка Tornado
```
6. Запустите Redis: запустите redis-server.exe (в случае скачивания и распаковки архива репозитория на Windows) <br>
7. Запустите приложение:
```python
python app.py
```
8. Приложение успешно запущено! В случае указания параметров по умолчанию: <br>
```python
REDIS_HOST=localhost
REDIS_PORT=6379
TORNADO_PORT=8888
```
Приложение будет доступно по адресу localhost:8888.