import tornado.websocket
import redis
import json
import uuid

# Подключение к Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """
    Обработчик WebSocket соединений для чата.
    """
    clients = set()  # Хранение активных WebSocket соединений

    def open(self):
        """
        Срабатывает при открытии нового WebSocket соединения.
        """
        # Получение имени пользователя или генерация уникального имени
        self.username = self.get_argument("username", None)
        if not self.username:
            self.username = f"User-{str(uuid.uuid4())[:8]}"

        self.clients.add(self)  # Добавление клиента в активный список
        redis_client.sadd("online_clients", self.username)  # Сохранение имени пользователя в Redis

        self.update_clients_list()  # Обновление списка клиентов

        # Отправка приветственного сообщения
        self.write_message(json.dumps({
            "type": "welcome",
            "message": f"Добро пожаловать в чат, {self.username}!"
        }))

    def on_message(self, message):
        """
        Обработка входящих сообщений от клиента.
        """
        # Форматирование данных сообщения
        data = {
            "type": "message",
            "data": {
                "sender": self.username,
                "message": message
            }
        }
        # Публикация сообщения в Redis Pub/Sub
        redis_client.publish('chat_channel', json.dumps(data))

    def on_close(self):
        """
        Срабатывает при закрытии WebSocket соединения.
        """
        self.clients.remove(self)  # Удаление клиента из активного списка
        redis_client.srem("online_clients", self.username)  # Удаление клиента из Redis

        self.update_clients_list()  # Обновление списка клиентов

    def check_origin(self, origin):
        """
        Разрешение запросов с других доменов.
        """
        return True

    def update_clients_list(self):
        """
        Обновление списка активных клиентов.
        """
        online_clients = list(redis_client.smembers("online_clients"))  # Получение клиентов из Redis

        # Форматирование данных для отправки
        data = {
            "type": "clients",
            "clients": online_clients
        }

        # Отправка обновлённого списка всем подключённым клиентам
        for client in self.clients:
            client.write_message(json.dumps(data))