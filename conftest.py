import pytest
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()


# Базовый URL API (из переменных окружения или по умолчанию)
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080/api")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


@pytest.fixture(scope="session")
def base_url():
    """
    Фикстура возвращает базовый URL API.
    
    Returns:
        str: Базовый URL API
    """
    return BASE_URL


@pytest.fixture(scope="session")
def frontend_url():
    """
    Фикстура возвращает URL frontend.
    
    Returns:
        str: URL frontend
    """
    return FRONTEND_URL


@pytest.fixture(scope="session")
def auth_token():
    """
    Фикстура для получения токена аутентификации.
    Выполняется один раз за сессию (session scope).
    
    Returns:
        str: JWT токен для авторизации
    
    Raises:
        pytest.fail: Если не удалось получить токен
    """
    login_data = {"password": "novicarsAdminPass"}
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json()["token"]
            print(f"\n✅ Auth token received: {token[:20]}...")
            return token
        else:
            pytest.fail(f"Не удалось получить токен аутентификации. Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        pytest.fail("Backend недоступен. Убедитесь что сервер запущен на порту 8080")
    except Exception as e:
        pytest.fail(f"Ошибка при получении токена: {str(e)}")


@pytest.fixture
def headers(auth_token):
    """
    Заголовки HTTP с авторизацией.
    
    Args:
        auth_token: JWT токен из фикстуры
    
    Returns:
        dict: Заголовки для API запросов
    """
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }


@pytest.fixture
def public_headers():
    """
    Заголовки для публичных API (без авторизации).
    
    Returns:
        dict: Заголовки для публичных запросов
    """
    return {
        "Content-Type": "application/json"
    }


@pytest.fixture
def test_service_data():
    """
    Тестовые данные для создания услуги.
    
    Returns:
        dict: Данные услуги для тестов
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "name": f"Test Service {timestamp}",
        "description": "Test service description for QA testing",
        "price": 5000,
        "duration": 60,
        "available": True
    }


@pytest.fixture
def test_booking_data():
    """
    Тестовые данные для создания заявки.
    
    Returns:
        dict: Данные заявки для тестов
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "customer_name": f"Test User {timestamp}",
        "customer_phone": "+7 (999) 123-45-67",
        "car_brand": "Toyota",
        "car_model": "Camry",
        "service_id": "svc_1",
        "comment": f"Test comment {timestamp}"
    }


@pytest.fixture
def test_review_data():
    """
    Тестовые данные для создания отзыва.

    Returns:
        dict: Данные отзыва для тестов
    """
    return {
        "name": "Тестовый Клиент",
        "car_brand": "Toyota",
        "car_model": "Camry",
        "rating": 5,
        "text": "Отличный сервис! Быстро и качественно сделали работу. Рекомендую!"
    }


@pytest.fixture
def test_user_data():
    """
    Тестовые данные для создания пользователя.
    
    Returns:
        dict: Данные пользователя для тестов
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "email": f"test{timestamp}@example.com",
        "password": "TestPassword123!",
        "role": "user"
    }


@pytest.fixture(autouse=True)
def log_test_start(request):
    """
    Автоматическая фикстура для логирования начала каждого теста.
    Выполняется для каждого теста (autouse=True).
    
    Args:
        request: pytest request object
    """
    print(f"\n{'='*60}")
    print(f"🧪 Starting test: {request.node.name}")
    print(f"{'='*60}")
    yield
    print(f"✅ Finished test: {request.node.name}")


@pytest.fixture
def api_session():
    """
    Сессия requests для эффективной работы с API.
    Закрывается автоматически после использования.
    
    Yields:
        requests.Session: Сессия для HTTP запросов
    """
    session = requests.Session()
    session.base_url = BASE_URL
    yield session
    session.close()


@pytest.fixture
def wait():
    """
    Фикстура для ожидания (delay между действиями).
    
    Returns:
        function: Функция wait(seconds)
    """
    def _wait(seconds):
        time.sleep(seconds)
    return _wait


@pytest.fixture
def cleanup_booking(auth_token, headers):
    """
    Фикстура для автоматической очистки созданных заявок.
    
    Args:
        auth_token: Токен авторизации
        headers: Заголовки с авторизацией
    
    Yields:
        function: Функция для добавления booking_id в список на удаление
    """
    booking_ids = []
    
    yield lambda bid: booking_ids.append(bid)
    
    # Cleanup после теста
    for bid in booking_ids:
        try:
            requests.delete(
                f"{BASE_URL}/admin/bookings/{bid}",
                headers=headers,
                timeout=5
            )
            print(f"🧹 Cleaned up booking: {bid}")
        except Exception as e:
            print(f"⚠️ Failed to cleanup booking {bid}: {e}")


@pytest.fixture
def cleanup_service(auth_token, headers):
    """
    Фикстура для автоматической очистки созданных услуг.
    
    Args:
        auth_token: Токен авторизации
        headers: Заголовки с авторизацией
    
    Yields:
        function: Функция для добавления service_id в список на удаление
    """
    service_ids = []
    
    yield lambda sid: service_ids.append(sid)
    
    # Cleanup после теста
    for sid in service_ids:
        try:
            requests.delete(
                f"{BASE_URL}/admin/services/{sid}",
                headers=headers,
                timeout=5
            )
            print(f"🧹 Cleaned up service: {sid}")
        except Exception as e:
            print(f"⚠️ Failed to cleanup service {sid}: {e}")
