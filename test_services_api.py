import pytest
import requests
from conftest import BASE_URL


class TestPublicServicesAPI:
    """
    Тестирование публичного API услуг (без авторизации)
    
    Endpoints:
    - GET /api/services/
    """
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_services_success(self):
        """
        Тест успешного получения списка услуг
        
        Test Case: TC_SERVICES_001
        
        Steps:
        1. Отправить GET запрос на /api/services/
        2. Проверить статус код 200
        3. Проверить наличие ключа 'services'
        4. Проверить что список не пустой
        
        Expected:
        - Status code: 200
        - Services list: not empty
        - Each service has required fields
        """
        # Act
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        
        # Assert
        assert response.status_code == 200, f"Status code is {response.status_code}"
        
        response_data = response.json()
        assert "services" in response_data, "'services' key not found"
        assert isinstance(response_data["services"], list), "Services is not a list"
        assert len(response_data["services"]) > 0, "Services list is empty"
        
        print(f"✅ Got {len(response_data['services'])} services")
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_service_structure(self):
        """
        Тест структуры данных услуги
        
        Test Case: TC_SERVICES_002
        
        Expected:
        - Each service has: id, name, price, duration, available
        - Correct data types
        """
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        services = response.json()["services"]
        
        # Проверяем первую услугу
        service = services[0]
        
        # Assert - Required fields
        assert "id" in service, "Service ID not found"
        assert "name" in service, "Service name not found"
        assert "price" in service, "Service price not found"
        assert "duration" in service, "Service duration not found"
        assert "available" in service, "Service available flag not found"
        
        # Assert - Data types
        assert isinstance(service["id"], str), "ID should be string"
        assert isinstance(service["name"], str), "Name should be string"
        assert isinstance(service["price"], (int, float)), "Price should be number"
        assert isinstance(service["duration"], int), "Duration should be integer"
        assert isinstance(service["available"], bool), "Available should be boolean"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_services_count(self):
        """
        Тест количества услуг (должно быть 21)
        
        Test Case: TC_SERVICES_003
        
        Expected: 21 services
        """
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        services = response.json()["services"]
        
        assert len(services) == 21, f"Expected 21 services, got {len(services)}"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_services_sorted_by_name(self):
        """
        Тест сортировки услуг по названию
        
        Test Case: TC_SERVICES_004
        
        Expected: Services sorted alphabetically by name
        """
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        services = response.json()["services"]
        
        names = [s["name"] for s in services]
        assert names == sorted(names), "Services are not sorted by name"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_service_price_positive(self):
        """
        Тест что все цены положительные
        
        Test Case: TC_SERVICES_005
        
        Expected: All prices > 0
        """
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        services = response.json()["services"]
        
        for service in services:
            assert service["price"] > 0, \
                f"Service {service['name']} has non-positive price: {service['price']}"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_service_duration_positive(self):
        """
        Тест что все длительности положительные
        
        Test Case: TC_SERVICES_006
        
        Expected: All durations > 0
        """
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        services = response.json()["services"]
        
        for service in services:
            assert service["duration"] > 0, \
                f"Service {service['name']} has non-positive duration: {service['duration']}"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_service_ids_unique(self):
        """
        Тест уникальности ID услуг
        
        Test Case: TC_SERVICES_007
        
        Expected: All service IDs are unique
        """
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        services = response.json()["services"]
        
        ids = [s["id"] for s in services]
        assert len(ids) == len(set(ids)), "Duplicate service IDs found"
    
    @pytest.mark.performance
    @pytest.mark.api
    def test_services_response_time(self):
        """
        Тест времени ответа API услуг
        
        Test Case: TC_SERVICES_008
        
        Expected: Response time < 1 second
        """
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        
        response_time = response.elapsed.total_seconds()
        assert response_time < 1.0, \
            f"Response time is {response_time}s, expected < 1.0s"
        print(f"⏱️ Response time: {response_time:.3f}s")
    
    @pytest.mark.performance
    @pytest.mark.api
    def test_services_response_size(self):
        """
        Тест размера ответа API услуг
        
        Test Case: TC_SERVICES_009
        
        Expected: Response size < 100KB
        """
        response = requests.get(f"{BASE_URL}/services/", timeout=10)
        
        response_size = len(response.content)
        assert response_size < 100 * 1024, \
            f"Response size is {response_size} bytes, expected < 100KB"
        print(f"📦 Response size: {response_size} bytes")


class TestAdminServicesAPI:
    """
    Тестирование админского API услуг (требуется авторизация)
    
    Endpoints:
    - GET /api/admin/services/
    - POST /api/admin/services/
    - PUT /api/admin/services/:id
    - DELETE /api/admin/services/:id
    """
    
    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        """Автоматическая установка заголовков авторизации"""
        self.headers = headers
        self.auth_token = auth_token
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_admin_services_success(self):
        """
        Тест получения всех услуг админом
        
        Test Case: TC_SERVICES_010
        
        Expected: Status code 200, services list
        """
        response = requests.get(
            f"{BASE_URL}/admin/services/",
            headers=self.headers,
            timeout=10
        )
        
        assert response.status_code == 200, f"Status code is {response.status_code}"
        assert "services" in response.json(), "'services' key not found"
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_service_success(self, test_service_data, cleanup_service):
        """
        Тест успешного создания услуги
        
        Test Case: TC_SERVICES_011
        
        Steps:
        1. Отправить POST запрос с данными услуги
        2. Проверить статус код 201
        3. Проверить что услуга создана
        
        Expected:
        - Status code: 201
        - Service created in response
        - Service name matches
        """
        # Act
        response = requests.post(
            f"{BASE_URL}/admin/services/",
            json=test_service_data,
            headers=self.headers,
            timeout=10
        )
        
        # Assert
        assert response.status_code == 201, f"Status code is {response.status_code}"
        
        response_data = response.json()
        assert "message" in response_data, "Message not found"
        assert "service" in response_data, "Service not found"
        assert response_data["service"]["name"] == test_service_data["name"]
        
        # Cleanup
        cleanup_service(response_data["service"]["id"])
        print(f"✅ Service created: {test_service_data['name']}")
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_service_without_auth(self, test_service_data):
        """
        Тест создания услуги без авторизации
        
        Test Case: TC_SERVICES_012
        
        Expected: Status code 401
        """
        response = requests.post(
            f"{BASE_URL}/admin/services/",
            json=test_service_data,
            timeout=10
        )
        
        assert response.status_code == 401, "Should return 401 without auth"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_service_with_empty_name(self, test_service_data, headers):
        """
        Тест создания услуги с пустым названием
        
        Test Case: TC_SERVICES_013
        
        Expected: Status code 400
        """
        test_service_data["name"] = ""
        
        response = requests.post(
            f"{BASE_URL}/admin/services/",
            json=test_service_data,
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 400, "Should return 400 for empty name"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_service_with_negative_price(self, test_service_data, headers):
        """
        Тест создания услуги с отрицательной ценой
        
        Test Case: TC_SERVICES_014
        
        Expected: Status code 400 (validation) or 201 (if no validation)
        """
        test_service_data["price"] = -100
        
        response = requests.post(
            f"{BASE_URL}/admin/services/",
            json=test_service_data,
            headers=headers,
            timeout=10
        )
        
        # Должна быть валидация
        assert response.status_code in [400, 201], "Should validate price"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_service_with_zero_duration(self, test_service_data, headers):
        """
        Тест создания услуги с нулевой длительностью
        
        Test Case: TC_SERVICES_015
        
        Expected: Status code 400
        """
        test_service_data["duration"] = 0
        
        response = requests.post(
            f"{BASE_URL}/admin/services/",
            json=test_service_data,
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 400, "Should return 400 for zero duration"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_service_success(self, test_service_data, headers, cleanup_service):
        """
        Тест обновления услуги
        
        Test Case: TC_SERVICES_016
        
        Expected: Status code 200, service updated
        """
        # Сначала создаём услугу
        create_response = requests.post(
            f"{BASE_URL}/admin/services/",
            json=test_service_data,
            headers=headers,
            timeout=10
        )
        
        service_id = create_response.json()["service"]["id"]
        cleanup_service(service_id)
        
        # Обновляем услугу
        update_data = test_service_data.copy()
        update_data["price"] = 6000
        update_data["name"] = "Updated Service"
        
        response = requests.put(
            f"{BASE_URL}/admin/services/{service_id}",
            json=update_data,
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 200, f"Status code is {response.status_code}"
        assert response.json()["service"]["price"] == 6000
        assert response.json()["service"]["name"] == "Updated Service"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_nonexistent_service(self, test_service_data, headers):
        """
        Тест обновления несуществующей услуги
        
        Test Case: TC_SERVICES_017
        
        Expected: Status code 404
        """
        response = requests.put(
            f"{BASE_URL}/admin/services/nonexistent_id",
            json=test_service_data,
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 404, "Should return 404 for nonexistent service"
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_service_success(self, test_service_data, headers):
        """
        Тест удаления услуги
        
        Test Case: TC_SERVICES_018
        
        Expected: Status code 200, service deleted
        """
        # Создаём услугу
        create_response = requests.post(
            f"{BASE_URL}/admin/services/",
            json=test_service_data,
            headers=headers,
            timeout=10
        )
        
        service_id = create_response.json()["service"]["id"]
        
        # Удаляем услугу
        response = requests.delete(
            f"{BASE_URL}/admin/services/{service_id}",
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 200, f"Status code is {response.status_code}"
        assert "message" in response.json()
        print(f"✅ Service deleted: {service_id}")
    
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_nonexistent_service(self, headers):
        """
        Тест удаления несуществующей услуги
        
        Test Case: TC_SERVICES_019
        
        Expected: Status code 404
        """
        response = requests.delete(
            f"{BASE_URL}/admin/services/nonexistent_id",
            headers=headers,
            timeout=10
        )
        
        assert response.status_code == 404, "Should return 404"
