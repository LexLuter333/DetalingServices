# 🚀 Инструкция по запуску Deteleng

## Быстрый старт (без Docker)

### 1. Запуск Backend

```bash
cd D:\Deteleng\backend

# Установить зависимости (если еще не установлены)
go mod download

# Запустить сервер
go run ./cmd/api
```

**Backend запустится на:** `http://localhost:8080`

---

### 2. Запуск Frontend (в новом терминале)

```bash
cd D:\Deteleng\frontend

# Установить зависимости (если еще не установлены)
npm install

# Запустить dev-сервер
npm run dev
```

**Frontend запустится на:** `http://localhost:5173`

---

## Запуск через Docker

```bash
cd D:\Deteleng

# Запустить оба сервиса
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановить
docker-compose down
```

---

## 🔐 Доступ к админ-панели

1. Откройте `http://localhost:5173/admin/login`
2. Введите credentials:
   - **Email:** `admin@deteleng.com`
   - **Пароль:** `admin123`

---

## 📡 Проверка API

### Health Check
```bash
curl http://localhost:8080/api/ping
# Ответ: {"message":"pong"}
```

### Создание бронирования (тест)
```bash
curl -X POST http://localhost:8080/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Иван Тестов",
    "customer_phone": "+7 (999) 000-00-00",
    "car_brand": "BMW",
    "car_model": "X5",
    "service_id": "svc_3",
    "comment": "Тестовое бронирование"
  }'
```

### Login (получение токена)
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@deteleng.com",
    "password": "admin123"
  }'
```

---

## 🗂️ Структура проекта

```
D:\Deteleng\
├── backend/                    # Go Gin backend
│   ├── cmd/api/main.go        # Точка входа
│   ├── internal/
│   │   ├── config/            # Конфигурация
│   │   ├── handlers/          # HTTP обработчики
│   │   ├── middleware/        # Middleware (auth, cors)
│   │   ├── models/            # Модели данных
│   │   ├── repository/        # Доступ к данным
│   │   └── services/          # Бизнес-логика
│   ├── go.mod
│   └── Dockerfile
│
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── api/api.js         # API клиент
│   │   ├── context/           # React context (Auth)
│   │   ├── components/        # Компоненты
│   │   ├── pages/             # Страницы
│   │   │   ├── admin/         # Admin panel
│   │   │   ├── Home.jsx
│   │   │   ├── Services.jsx
│   │   │   └── Contacts.jsx
│   │   └── styles/            # CSS стили
│   ├── package.json
│   └── Dockerfile
│
└── docker-compose.yml
```

---

## ✅ Что работает

### Frontend → Backend Integration

| Компонент | API Endpoint | Статус |
|-----------|--------------|--------|
| Форма бронирования | `POST /api/bookings` | ✅ Работает |
| Login админа | `POST /api/auth/login` | ✅ Работает |
| Dashboard | `GET /api/admin/dashboard` | ✅ Работает |
| Управление бронированиями | `GET/PUT/DELETE /api/admin/bookings/*` | ✅ Работает |
| Управление услугами | `GET/PUT /api/admin/services/*` | ✅ Работает |
| Публичные услуги | `GET /api/services` | ✅ Работает |

---

## 🛠️ Решение проблем

### Backend не запускается

**Ошибка:** `module not found`
```bash
cd backend
go mod tidy
go run ./cmd/api
```

### Frontend не видит backend

**Проблема:** CORS ошибки в консоли

**Решение:**
1. Убедитесь, что backend запущен на порту 8080
2. Проверьте, что vite.config.js имеет proxy настройку
3. Перезапустите frontend: `npm run dev`

### Не работает login

**Проблема:** "Invalid credentials"

**Решение:**
1. Убедитесь, что используете правильные credentials:
   - Email: `admin@deteleng.com`
   - Пароль: `admin123`
2. Проверьте, что backend успешно запустился (пароль хешируется при старте)
3. Очистите localStorage в браузере

### Docker контейнер не запускается

**Проблема:** Port already in use

**Решение:**
```bash
# Остановить все контейнеры
docker-compose down

# Проверить занятые порты
netstat -ano | findstr :8080
netstat -ano | findstr :5173

# Убить процессы или изменить порты в docker-compose.yml
```

---

## 📱 Основные маршруты

### Публичный сайт
- `http://localhost:5173/` - Главная страница
- `http://localhost:5173/services` - Услуги
- `http://localhost:5173/contacts` - Контакты

### Админ-панель
- `http://localhost:5173/admin/login` - Вход
- `http://localhost:5173/admin/dashboard` - Дашборд
- `http://localhost:5173/admin/bookings` - Бронирования
- `http://localhost:5173/admin/services` - Услуги

---

## 🎯 Следующие шаги

1. **Протестируйте форму бронирования** на главной странице
2. **Войдите в админ-панель** и проверьте данные
3. **Измените статус бронирования** в админ-панели
4. **Отключите/включите услугу** в разделе Услуги

---

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи backend: `go run ./cmd/api` выводит логи в консоль
2. Проверьте консоль браузера на ошибки JavaScript
3. Убедитесь, что оба сервиса запущены одновременно
