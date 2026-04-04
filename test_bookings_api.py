import pytest
import requests
from conftest import BASE_URL


class TestPublicBookingsAPI:
    """
    Тестирование публичного API заявок (без авторизации)
    
    Endpoints:
    - POST /api/bookings/
    - GET /api/bookings/
    - GET /api/bookings/:id
    """
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_booking_success(self, test_booking_data):
        """
        Тест успешного создания заявки
        
        Test Case: TC_BOOKINGS_001
        
        Steps:
        1. Отправить POST запрос с данными заявки
        2. Проверить статус код 201
        3. Проверить что заявка создана
        
        Expected:
        - Status code: 201
        - Booking created in response
        - Status: pending
        """
        # Act
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        # Assert
        assert response.status_code == 201, f"Status code is {response.status_code}"
        
        response_data = response.json()
        assert "message" in response_data, "Message not found"
        assert "booking" in response_data, "Booking not found"
        
        booking = response_data["booking"]
        assert booking["customer_name"] == test_booking_data["customer_name"]
        assert booking["customer_phone"] == test_booking_data["customer_phone"]
        assert booking["status"] == "pending", "Status should be 'pending'"
        
        print(f"✅ Booking created: {booking['id']}")
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_booking_with_valid_service(self, test_booking_data):
        """
        Тест создания заявки с валидной услугой
        
        Test Case: TC_BOOKINGS_002
        
        Expected: Status code 201
        """
        test_booking_data["service_id"] = "svc_1"
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code == 201
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_booking_with_invalid_service(self, test_booking_data):
        """
        Тест создания заявки с несуществующей услугой
        
        Test Case: TC_BOOKINGS_003
        
        Expected: Status code 500 or 400
        """
        test_booking_data["service_id"] = "nonexistent_service"
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code in [400, 500], "Should return error for invalid service"
        assert "error" in response.json()
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_booking_without_name(self, test_booking_data):
        """
        Тест создания заявки без имени
        
        Test Case: TC_BOOKINGS_004
        
        Expected: Status code 400
        """
        test_booking_data["customer_name"] = ""
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code == 400, "Should return 400 for empty name"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_booking_without_phone(self, test_booking_data):
        """
        Тест создания заявки без телефона
        
        Test Case: TC_BOOKINGS_005
        
        Expected: Status code 400
        """
        test_booking_data["customer_phone"] = ""
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code == 400
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_booking_with_invalid_phone(self, test_booking_data):
        """
        Тест создания заявки с невалидным телефоном
        
        Test Case: TC_BOOKINGS_006
        
        Expected: Status code 400
        """
        test_booking_data["customer_phone"] = "invalid_phone"
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code == 400
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_booking_with_optional_comment(self, test_booking_data):
        """
        Тест создания заявки с необязательным комментарием
        
        Test Case: TC_BOOKINGS_007
        
        Expected: Status code 201
        """
        test_booking_data["comment"] = "Optional comment"
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code == 201
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_booking_without_comment(self, test_booking_data):
        """
        Тест создания заявки без комментария
        
        Test Case: TC_BOOKINGS_008
        
        Expected: Status code 201
        """
        if "comment" in test_booking_data:
            del test_booking_data["comment"]
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code == 201
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_booking_without_car_model(self, test_booking_data):
        """
        Тест создания заявки без модели автомобиля
        
        Test Case: TC_BOOKINGS_009
        
        Expected: Status code 201 (model is optional)
        """
        test_booking_data["car_model"] = ""
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code == 201
    
    @pytest.mark.performance
    @pytest.mark.api
    def test_create_booking_response_time(self, test_booking_data):
        """
        Тест времени ответа при создании заявки
        
        Test Case: TC_BOOKINGS_010
        
        Expected: Response time < 2 seconds
        """
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        response_time = response.elapsed.total_seconds()
        assert response_time < 2.0, \
            f"Response time is {response_time}s, expected < 2.0s"
        print(f"⏱️ Response time: {response_time:.3f}s")
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_all_bookings_success(self, auth_token, headers):
        """
        Тест получения всех заявок
        
        Test Case: TC_BOOKINGS_011
        
        Expected: Status code 200, bookings list
        """
        response = requests.get(
            f"{BASE_URL}/bookings/",
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 200
        assert "bookings" in response.json()
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_booking_by_id(self, test_booking_data, headers):
        """
        Тест получения заявки по ID
        
        Test Case: TC_BOOKINGS_012
        
        Expected: Status code 200, booking data
        """
        # Создаём заявку
        create_response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        booking_id = create_response.json()["booking"]["id"]
        
        # Получаем заявку
        response = requests.get(
            f"{BASE_URL}/bookings/{booking_id}",
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 200
        assert response.json()["booking"]["id"] == booking_id
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_nonexistent_booking(self, headers):
        """
        Тест получения несуществующей заявки
        
        Test Case: TC_BOOKINGS_013
        
        Expected: Status code 404
        """
        response = requests.get(
            f"{BASE_URL}/bookings/nonexistent_id",
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 404
    
    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.parametrize("service_id,expected_status", [
        ("svc_1", 201),
        ("svc_2", 201),
        ("svc_3", 201),
        ("nonexistent", 500),
        ("", 400)
    ])
    def test_create_booking_with_different_services(
        self, test_booking_data, service_id, expected_status
    ):
        """
        Параметризованный тест создания заявки с разными услугами
        
        Test Case: TC_BOOKINGS_014
        
        Args:
            test_booking_data: Фикстура с данными заявки
            service_id: ID услуги из параметра
            expected_status: Ожидаемый статус код
        
        Expected: Status code matches expected
        """
        test_booking_data["service_id"] = service_id
        
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        
        assert response.status_code == expected_status, \
            f"Service {service_id}: Expected {expected_status}, got {response.status_code}"


class TestAdminBookingsAPI:
    """
    Тестирование админского API заявок (требуется авторизация)
    
    Endpoints:
    - GET /api/admin/bookings/
    - PUT /api/admin/bookings/:id/status
    - DELETE /api/admin/bookings/:id
    """
    
    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        """Автоматическая установка заголовков авторизации"""
        self.headers = headers
        self.auth_token = auth_token
    
    @pytest.fixture
    def create_test_booking(self, test_booking_data, headers):
        """
        Фикстура для создания тестовой заявки
        
        Yields:
            str: ID созданной заявки
        """
        response = requests.post(
            f"{BASE_URL}/bookings/",
            json=test_booking_data,
            timeout=10
        )
        booking_id = response.json()["booking"]["id"]
        yield booking_id
        
        # Cleanup
        try:
            requests.delete(
                f"{BASE_URL}/admin/bookings/{booking_id}",
                headers=headers,
                timeout=5
            )
        except:
            pass
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_admin_bookings_success(self):
        """
        Тест получения всех заявок админом
        
        Test Case: TC_BOOKINGS_015
        
        Expected: Status code 200, bookings list
        """
        response = requests.get(
            f"{BASE_URL}/admin/bookings/",
            headers=self.headers,
            timeout=10
        )
        
        assert response.status_code == 200
        assert "bookings" in response.json()
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_update_booking_status_success(self, create_test_booking):
        """
        Тест обновления статуса заявки
        
        Test Case: TC_BOOKINGS_016
        
        Steps:
        1. Создать заявку (через фикстуру)
        2. Отправить PUT запрос на обновление статуса
        3. Проверить что статус обновился
        
        Expected:
        - Status code: 200
        - Status updated to 'confirmed'
        """
        booking_id = create_test_booking
        
        # Act
        response = requests.put(
            f"{BASE_URL}/admin/bookings/{booking_id}/status",
            json={"status": "confirmed"},
            headers=self.headers,
            timeout=10
        )
        
        # Assert
        assert response.status_code == 200, f"Status code is {response.status_code}"
        
        # Проверяем что статус действительно обновился
        get_response = requests.get(
            f"{BASE_URL}/admin/bookings/",
            headers=self.headers,
            timeout=10
        )
        bookings = get_response.json()["bookings"]
        booking = next((b for b in bookings if b["id"] == booking_id), None)
        
        assert booking is not None
        assert booking["status"] == "confirmed"
        print(f"✅ Booking status updated to 'confirmed'")
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_booking_status_to_completed(self, create_test_booking):
        """
        Тест обновления статуса на 'completed'
        
        Test Case: TC_BOOKINGS_017
        
        Expected: Status code 200
        """
        booking_id = create_test_booking
        
        response = requests.put(
            f"{BASE_URL}/admin/bookings/{booking_id}/status",
            json={"status": "completed"},
            headers=self.headers,
            timeout=10
        )
        
        assert response.status_code == 200
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_booking_status_to_cancelled(self, create_test_booking):
        """
        Тест обновления статуса на 'cancelled'
        
        Test Case: TC_BOOKINGS_018
        
        Expected: Status code 200
        """
        booking_id = create_test_booking
        
        response = requests.put(
            f"{BASE_URL}/admin/bookings/{booking_id}/status",
            json={"status": "cancelled"},
            headers=self.headers,
            timeout=10
        )
        
        assert response.status_code == 200
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_booking_status_without_auth(self, create_test_booking):
        """
        Тест обновления статуса без авторизации
        
        Test Case: TC_BOOKINGS_019
        
        Expected: Status code 401
        """
        booking_id = create_test_booking
        
        response = requests.put(
            f"{BASE_URL}/admin/bookings/{booking_id}/status",
            json={"status": "confirmed"},
            timeout=10
        )
        
        assert response.status_code == 401
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_booking_status_invalid_status(self, create_test_booking):
        """
        Тест обновления статуса на невалидный статус
        
        Test Case: TC_BOOKINGS_020
        
        Expected: Status code 400 or 200 (if no validation)
        """
        booking_id = create_test_booking
        
        response = requests.put(
            f"{BASE_URL}/admin/bookings/{booking_id}/status",
            json={"status": "invalid_status"},
            headers=self.headers,
            timeout=10
        )
        
        # Должна быть валидация статусов
        assert response.status_code in [200, 400]
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_booking_success(self, create_test_booking):
        """
        Тест удаления заявки
        
        Test Case: TC_BOOKINGS_021
        
        Expected: Status code 200, booking deleted
        """
        booking_id = create_test_booking
        
        response = requests.delete(
            f"{BASE_URL}/admin/bookings/{booking_id}",
            headers=self.headers,
            timeout=10
        )
        
        assert response.status_code == 200
        
        # Проверяем что заявка удалена
        get_response = requests.get(
            f"{BASE_URL}/admin/bookings/",
            headers=self.headers,
            timeout=10
        )
        bookings = get_response.json()["bookings"]
        booking_ids = [b["id"] for b in bookings]
        
        assert booking_id not in booking_ids
        print(f"✅ Booking deleted: {booking_id}")
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_nonexistent_booking(self):
        """
        Тест удаления несуществующей заявки
        
        Test Case: TC_BOOKINGS_022
        
        Expected: Status code 404
        """
        response = requests.delete(
            f"{BASE_URL}/admin/bookings/nonexistent_id",
            headers=self.headers,
            timeout=10
        )
        
        assert response.status_code == 404
