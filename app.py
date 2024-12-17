import os
from dotenv import load_dotenv  # Для загрузки .env файла
import tornado.ioloop
import tornado.web
import threading
import asyncio
import redis
import json
import logging
from websocket_handler import WebSocketHandler  # Импорт WebSocketHandler

# Загрузка переменных окружения из .env
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки Redis из переменных окружения
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

# Подключение к Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Настройки Tornado из переменных окружения
TORNADO_PORT = int(os.getenv("TORNADO_PORT"))

async def redis_listener():
    """
    Асинхронный слушатель Pub/Sub канала Redis.
    """
    pubsub = redis_client.pubsub()
    pubsub.subscribe("chat_channel")  # Подписка на канал "chat_channel"
    for message in pubsub.listen():
        if message["type"] == "message":
            # Десериализация данных из сообщения
            data = json.loads(message["data"])
            # Отправка сообщения всем подключённым клиентам
            for client in WebSocketHandler.clients:
                client.write_message(json.dumps(data))


def start_redis_listener():
    """
    Запуск слушателя Redis в отдельном потоке.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(redis_listener())

if __name__ == "__main__":
    # Настройка приложения Tornado
    redis_client.delete("online_clients")
    app = tornado.web.Application([
        (r"/websocket", WebSocketHandler),  # Эндпоинт для WebSocket соединений
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./static", "default_filename": "index.html"})  # Статические файлы
    ])
    app.listen(TORNADO_PORT)  # Слушаем порт из переменной окружения

    logger.info(f"Сервер запущен: http://localhost:{TORNADO_PORT}")

    # Запуск Redis слушателя в отдельном потоке
    threading.Thread(target=start_redis_listener, daemon=True).start()

    # Запуск основного цикла Tornado
    tornado.ioloop.IOLoop.current().start()