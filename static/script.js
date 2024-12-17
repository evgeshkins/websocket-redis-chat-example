// Установка WebSocket соединения с сервером
const ws = new WebSocket("ws://localhost:8888/websocket");

// Обработчик входящих сообщений от сервера
ws.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);

        // Обработка приветственного сообщения
        if (data.type === "welcome") {
            displayChatMessage("System", data.message, "system");
        }

        // Обработка обычных сообщений
        if (data.type === "message") {
            const { sender, message } = data.data;
            displayChatMessage(sender, message, "user");
        }

        // Обновление списка клиентов онлайн
        if (data.type === "clients") {
            updateClientsList(data.clients);
        }
    } catch (error) {
        console.error("Ошибка при обработке входящего сообщения:", error);
        console.error("Содержимое сообщения:", event.data);
    }
};

// Функция для отображения сообщения в чате
const displayChatMessage = (sender, message, messageType) => {
    const chat = document.getElementById("chat");
    const messageElement = document.createElement("div");

    // Стилизация сообщений в зависимости от типа
    messageElement.textContent = `${sender}: ${message}`;
    messageElement.classList.add("message");
    if (messageType === "system") {
        messageElement.classList.add("system");
    } else {
        messageElement.classList.add("user");
    }

    chat.appendChild(messageElement);

    // Автопрокрутка вниз для новых сообщений
    chat.scrollTop = chat.scrollHeight;
};

// Функция для обновления списка клиентов онлайн
const updateClientsList = (clients) => {
    const clientsList = document.getElementById("clients");
    clientsList.innerHTML = ""; // Очистка текущего списка

    clients.forEach((client) => {
        const clientItem = document.createElement("div");
        clientItem.textContent = client;
        clientItem.classList.add("client");
        clientsList.appendChild(clientItem);
    });
};

// Функция для отправки сообщения
const sendMessage = () => {
    const input = document.getElementById("message");
    const message = input.value.trim();

    if (message) {
        ws.send(message); // Отправка сообщения через WebSocket
        input.value = ""; // Очистка поля ввода
    }
};

