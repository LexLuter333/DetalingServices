import pytest
import requests
import time
from conftest import BASE_URL


class TestAuthAPI:
    """
    Тестирование API аутентификации
    
    Endpoints:
    - POST /api/auth/login
    """
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_success_with_valid_password(self):
        """
        Тест успешного входа с правильным паролем
        
        Test Case: TC_AUTH_001
        
        Steps:
        1. Отправить POST запрос с правильным паролем
        2. Проверить статус код 200
        3. Проверить наличие токена
        4. Проверить данные пользователя
        
        Expected:
        - Status code: 200
        - Token: present and not empty
        - User role: admin
        """
        # Arrange
        login_data = {"password": "novicarsAdminPass"}
        
        # Act
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "token" in response_data, "Token not found in response"
        assert "user" in response_data, "User data not found in response"
        assert response_data["user"]["role"] == "admin", "User role is not admin"
        assert len(response_data["token"]) > 0, "Token is empty"
        assert "message" in response_data, "Message not found in response"
        
        print(f"✅ Login successful, token: {response_data['token'][:20]}...")
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_success_with_alternative_password(self):
        """
        Тест входа с альтернативным паролем (admin123)
        
        Test Case: TC_AUTH_002
        """
        login_data = {"password": "admin123"}
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert "token" in response.json(), "Token not found"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_fail_with_invalid_password(self):
        """
        Тест входа с неправильным паролем
        
        Test Case: TC_AUTH_003
        
        Expected: Status code 401
        """
        login_data = {"password": "wrongpassword"}
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        assert "error" in response.json(), "Error message not found"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_fail_with_empty_password(self):
        """
        Тест входа с пустым паролем
        
        Test Case: TC_AUTH_004
        
        Expected: Status code 400
        """
        login_data = {"password": ""}
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_fail_without_password_field(self):
        """
        Тест входа без поля password
        
        Test Case: TC_AUTH_005
        
        Expected: Status code 400
        """
        login_data = {}
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_fail_with_special_characters(self):
        """
        Тест входа с спецсимволами в пароле
        
        Test Case: TC_AUTH_006
        """
        login_data = {"password": "@#$%^&*()"}
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    @pytest.mark.performance
    @pytest.mark.api
    def test_login_response_time(self):
        """
        Тест времени ответа API логина
        
        Test Case: TC_AUTH_007
        
        Expected: Response time < 1 second
        """
        login_data = {"password": "novicarsAdminPass"}
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        response_time = response.elapsed.total_seconds()
        assert response_time < 1.0, f"Response time is {response_time}s, expected < 1.0s"
        print(f"⏱️ Response time: {response_time:.3f}s")
    
    @pytest.mark.performance
    @pytest.mark.api
    def test_login_multiple_sequential_requests(self):
        """
        Тест нескольких последовательных запросов входа
        
        Test Case: TC_AUTH_008
        
        Expected: All requests succeed, average time < 2s
        """
        login_data = {"password": "novicarsAdminPass"}
        response_times = []
        
        for i in range(5):
            start = time.time()
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
            end = time.time()
            
            assert response.status_code == 200, f"Request {i+1} failed"
            response_times.append(end - start)
        
        avg_time = sum(response_times) / len(response_times)
        assert avg_time < 2.0, f"Average response time is {avg_time:.3f}s, expected < 2.0s"
        print(f"⏱️ Average response time: {avg_time:.3f}s")
    
    @pytest.mark.regression
    @pytest.mark.parametrize("password,expected_status", [
        ("novicarsAdminPass", 200),
        ("admin123", 200),
        ("wrongpassword", 401),
        ("", 400),
        ("12345", 401),
        ("admin", 401),
        ("password", 401),
    ])
    def test_login_multiple_passwords(self, password, expected_status):
        """
        Параметризованный тест с разными паролями
        
        Test Case: TC_AUTH_009
        
        Args:
            password: Тестовый пароль из параметра
            expected_status: Ожидаемый статус код
        
        Expected: Status code matches expected
        """
        login_data = {"password": password}
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        assert response.status_code == expected_status, \
            f"Password '{password}': Expected {expected_status}, got {response.status_code}"
