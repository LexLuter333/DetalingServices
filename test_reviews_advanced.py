import pytest
import requests
import time
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from conftest import BASE_URL


class TestReviewsAdvancedValidation:
    """
    Продвинутая валидация данных отзывов
    """

    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        """Автоматическая установка заголовков авторизации"""
        self.headers = headers
        self.auth_token = auth_token
        self.created_review_ids = []

    def teardown_method(self, method):
        """Очистка после каждого теста"""
        for review_id in self.created_review_ids:
            try:
                requests.delete(
                    f"{BASE_URL}/admin/reviews/{review_id}",
                    headers=self.headers,
                    timeout=5
                )
            except:
                pass
        self.created_review_ids.clear()

    @pytest.mark.advanced
    @pytest.mark.parametrize("name,expected_status", [
        ("А", 400),  # 1 символ
        ("Аа", 201),  # 2 символа
        ("А" * 50, 201),  # Длинное имя
        ("А" * 100, 201),  # Очень длинное имя
        ("", 400),  # Пустое
        ("Test123", 201),  # С цифрами
        ("Test@#$", 201),  # Со спецсимволами
        ("Иван-Мария", 201),  # С дефисом
        ("Jean-Pierre", 201),  # Латиница с дефисом
    ])
    def test_review_name_validation(self, name, expected_status):
        """
        Тест валидации имени клиента с параметризацией

        Test Case: TC_ADV_REV_001
        """
        review_data = {
            "name": name,
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 5,
            "text": "Тестовый отзыв"
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == expected_status, \
            f"Expected {expected_status} for name '{name[:20]}...', got {response.status_code}"

        if response.status_code == 201:
            self.created_review_ids.append(response.json()["review"]["id"])

    @pytest.mark.advanced
    @pytest.mark.parametrize("car_brand,expected_status", [
        ("A", 201),  # 1 символ
        ("A" * 30, 201),  # Длинная марка
        ("Mercedes-Benz", 201),  # С дефисом
        ("BMW M", 201),  # С пробелом
        ("", 400),  # Пустое
        ("123", 201),  # Цифры
    ])
    def test_review_car_brand_validation(self, car_brand, expected_status):
        """
        Тест валидации марки автомобиля

        Test Case: TC_ADV_REV_002
        """
        review_data = {
            "name": "Тест",
            "car_brand": car_brand,
            "car_model": "Camry",
            "rating": 5,
            "text": "Тест"
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == expected_status

        if response.status_code == 201:
            self.created_review_ids.append(response.json()["review"]["id"])

    @pytest.mark.advanced
    @pytest.mark.parametrize("car_model,expected_status", [
        ("A", 201),
        ("X5 M Competition", 201),
        ("C-Class", 201),
        ("", 400),
        ("123", 201),
    ])
    def test_review_car_model_validation(self, car_model, expected_status):
        """
        Тест валидации модели автомобиля

        Test Case: TC_ADV_REV_003
        """
        review_data = {
            "name": "Тест",
            "car_brand": "BMW",
            "car_model": car_model,
            "rating": 5,
            "text": "Тест"
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == expected_status

        if response.status_code == 201:
            self.created_review_ids.append(response.json()["review"]["id"])

    @pytest.mark.advanced
    @pytest.mark.parametrize("rating,expected_status", [
        (0, 400),
        (1, 201),
        (2, 201),
        (3, 201),
        (4, 201),
        (5, 201),
        (6, 400),
        (10, 400),
        (-1, 400),
        (3.5, 400),  # Дробное число
    ])
    def test_review_rating_validation(self, rating, expected_status):
        """
        Тест валидации рейтинга (целые числа 1-5)

        Test Case: TC_ADV_REV_004
        """
        review_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": rating,
            "text": "Тест"
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == expected_status, \
            f"Expected {expected_status} for rating {rating}, got {response.status_code}"

        if response.status_code == 201:
            self.created_review_ids.append(response.json()["review"]["id"])

    @pytest.mark.advanced
    @pytest.mark.parametrize("text,expected_status", [
        ("А", 201),  # 1 символ
        ("А" * 10, 201),  # 10 символов
        ("А" * 500, 201),  # Длинный текст
        ("А" * 1000, 201),  # Очень длинный
        ("А" * 5000, 201),  # Экстремально длинный
        ("", 400),  # Пустой
        ("Отлично! 100%", 201),  # Со спецсимволами
        ("<script>alert('xss')</script>", 201),  # XSS попытка
    ])
    def test_review_text_validation(self, text, expected_status):
        """
        Тест валидации текста отзыва

        Test Case: TC_ADV_REV_005
        """
        review_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 5,
            "text": text
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == expected_status

        if response.status_code == 201:
            self.created_review_ids.append(response.json()["review"]["id"])

    @pytest.mark.advanced
    def test_review_xss_protection(self):
        """
        Тест защиты от XSS атак

        Test Case: TC_ADV_REV_006
        """
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
        ]

        for payload in xss_payloads:
            review_data = {
                "name": payload,
                "car_brand": "Toyota",
                "car_model": "Camry",
                "rating": 5,
                "text": "Тест"
            }

            response = requests.post(
                f"{BASE_URL}/admin/reviews/",
                json=review_data,
                headers=self.headers,
                timeout=10
            )

            assert response.status_code == 201, f"XSS payload was not accepted: {payload[:30]}"
            review_id = response.json()["review"]["id"]
            self.created_review_ids.append(review_id)

            # Проверяем что данные экранированы при получении
            get_response = requests.get(
                f"{BASE_URL}/admin/reviews/",
                headers=self.headers,
                timeout=10
            )

            reviews = get_response.json()["reviews"]
            created_review = next((r for r in reviews if r["id"] == review_id), None)

            assert created_review is not None, "Review not found in list"
            # Проверяем что скрипт не выполняется (данные экранированы)
            assert "<script>" not in created_review["name"] or \
                   "&lt;script&gt;" in created_review["name"], \
                "XSS script was not escaped!"

    @pytest.mark.advanced
    def test_review_sql_injection_protection(self):
        """
        Тест защиты от SQL инъекций

        Test Case: TC_ADV_REV_007
        """
        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE reviews; --",
            "' UNION SELECT * FROM users --",
            "1; DELETE FROM reviews",
        ]

        for payload in sql_payloads:
            review_data = {
                "name": payload,
                "car_brand": "Toyota",
                "car_model": "Camry",
                "rating": 5,
                "text": "Тест"
            }

            response = requests.post(
                f"{BASE_URL}/admin/reviews/",
                json=review_data,
                headers=self.headers,
                timeout=10
            )

            # Должен принимать как обычный текст
            assert response.status_code == 201, f"SQL payload was rejected: {payload[:30]}"
            self.created_review_ids.append(response.json()["review"]["id"])

        # Проверяем что база данных цела
        get_response = requests.get(
            f"{BASE_URL}/admin/reviews/",
            headers=self.headers,
            timeout=10
        )

        assert get_response.status_code == 200, "Database may be compromised!"


class TestReviewsConcurrency:
    """
    Тесты конкурентного доступа
    """

    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        self.headers = headers
        self.created_review_ids = []

    def teardown_method(self, method):
        """Очистка после теста"""
        for review_id in self.created_review_ids:
            try:
                requests.delete(
                    f"{BASE_URL}/admin/reviews/{review_id}",
                    headers=self.headers,
                    timeout=5
                )
            except:
                pass

    @pytest.mark.advanced
    @pytest.mark.performance
    def test_concurrent_review_creation(self):
        """
        Тест одновременного создания нескольких отзывов

        Test Case: TC_ADV_REV_008

        Expected: Все отзывы создаются успешно без конфликтов
        """
        def create_review(index):
            review_data = {
                "name": f"Клиент {index}",
                "car_brand": "Toyota",
                "car_model": "Camry",
                "rating": random.randint(1, 5),
                "text": f"Отзыв номер {index}"
            }

            response = requests.post(
                f"{BASE_URL}/admin/reviews/",
                json=review_data,
                headers=self.headers,
                timeout=10
            )

            return response.status_code, response.json() if response.status_code == 201 else None

        # Создаём 10 отзывов одновременно
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_review, i) for i in range(10)]

            success_count = 0
            for future in as_completed(futures):
                status_code, data = future.result()
                if status_code == 201:
                    success_count += 1
                    self.created_review_ids.append(data["review"]["id"])

        assert success_count == 10, f"Only {success_count}/10 reviews created successfully"

    @pytest.mark.advanced
    @pytest.mark.performance
    def test_rapid_sequential_requests(self):
        """
        Тест быстрых последовательных запросов

        Test Case: TC_ADV_REV_009

        Expected: Все запросы обрабатываются корректно
        """
        review_ids = []

        try:
            # Создаём 20 отзывов быстро один за другим
            for i in range(20):
                review_data = {
                    "name": f"Быстрый клиент {i}",
                    "car_brand": "BMW",
                    "car_model": "X5",
                    "rating": 5,
                    "text": f"Быстрый отзыв {i}"
                }

                response = requests.post(
                    f"{BASE_URL}/admin/reviews/",
                    json=review_data,
                    headers=self.headers,
                    timeout=10
                )

                assert response.status_code == 201, \
                    f"Review {i} failed with status {response.status_code}"

                review_ids.append(response.json()["review"]["id"])

            # Проверяем что все отзывы в списке
            list_response = requests.get(
                f"{BASE_URL}/admin/reviews/",
                headers=self.headers,
                timeout=10
            )

            created_ids = [r["id"] for r in list_response.json()["reviews"]]

            for review_id in review_ids:
                assert review_id in created_ids, f"Review {review_id} not found in list"

        finally:
            # Очистка
            for review_id in review_ids:
                try:
                    requests.delete(
                        f"{BASE_URL}/admin/reviews/{review_id}",
                        headers=self.headers,
                        timeout=5
                    )
                except:
                    pass


class TestReviewsDataIntegrity:
    """
    Тесты целостности данных
    """

    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        self.headers = headers
        self.created_review_ids = []

    def teardown_method(self, method):
        for review_id in self.created_review_ids:
            try:
                requests.delete(
                    f"{BASE_URL}/admin/reviews/{review_id}",
                    headers=self.headers,
                    timeout=5
                )
            except:
                pass

    @pytest.mark.advanced
    def test_review_id_uniqueness(self):
        """
        Тест уникальности ID отзывов

        Test Case: TC_ADV_REV_010

        Expected: Все ID уникальны
        """
        review_ids = []

        # Создаём 5 отзывов
        for i in range(5):
            review_data = {
                "name": f"Клиент {i}",
                "car_brand": "Toyota",
                "car_model": "Camry",
                "rating": 5,
                "text": "Тест"
            }

            response = requests.post(
                f"{BASE_URL}/admin/reviews/",
                json=review_data,
                headers=self.headers,
                timeout=10
            )

            assert response.status_code == 201
            review_id = response.json()["review"]["id"]
            review_ids.append(review_id)
            self.created_review_ids.append(review_id)

        # Проверяем уникальность
        assert len(review_ids) == len(set(review_ids)), "Duplicate review IDs found!"

    @pytest.mark.advanced
    def test_review_data_persistence(self):
        """
        Тест сохранения данных отзыва

        Test Case: TC_ADV_REV_011

        Expected: Данные отзыва сохраняются и извлекаются корректно
        """
        original_data = {
            "name": "Постоянный Клиент",
            "car_brand": "Mercedes",
            "car_model": "S-Class",
            "rating": 5,
            "text": "Превосходный сервис! Рекомендую всем."
        }

        # Создаём отзыв
        create_response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=original_data,
            headers=self.headers,
            timeout=10
        )

        assert create_response.status_code == 201
        review_id = create_response.json()["review"]["id"]
        self.created_review_ids.append(review_id)

        # Получаем отзыв
        get_response = requests.get(
            f"{BASE_URL}/admin/reviews/",
            headers=self.headers,
            timeout=10
        )

        reviews = get_response.json()["reviews"]
        retrieved_review = next((r for r in reviews if r["id"] == review_id), None)

        assert retrieved_review is not None, "Review not found"
        assert retrieved_review["name"] == original_data["name"]
        assert retrieved_review["car_brand"] == original_data["car_brand"]
        assert retrieved_review["car_model"] == original_data["car_model"]
        assert retrieved_review["rating"] == original_data["rating"]
        assert retrieved_review["text"] == original_data["text"]

    @pytest.mark.advanced
    def test_review_update_integrity(self):
        """
        Тест целостности при обновлении

        Test Case: TC_ADV_REV_012

        Expected: Обновление не ломает данные
        """
        # Создаём
        create_data = {
            "name": "Исходный",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 3,
            "text": "Исходный текст"
        }

        create_response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=create_data,
            headers=self.headers,
            timeout=10
        )

        review_id = create_response.json()["review"]["id"]
        self.created_review_ids.append(review_id)

        # Обновляем
        update_data = {
            "name": "Обновлённый",
            "car_brand": "BMW",
            "car_model": "X5",
            "rating": 5,
            "text": "Обновлённый текст"
        }

        update_response = requests.put(
            f"{BASE_URL}/admin/reviews/{review_id}",
            json=update_data,
            headers=self.headers,
            timeout=10
        )

        assert update_response.status_code == 200

        # Проверяем
        get_response = requests.get(
            f"{BASE_URL}/admin/reviews/",
            headers=self.headers,
            timeout=10
        )

        reviews = get_response.json()["reviews"]
        updated_review = next((r for r in reviews if r["id"] == review_id), None)

        assert updated_review is not None
        assert updated_review["name"] == "Обновлённый"
        assert updated_review["car_brand"] == "BMW"
        assert updated_review["car_model"] == "X5"
        assert updated_review["rating"] == 5
        assert updated_review["text"] == "Обновлённый текст"


class TestReviewsEdgeCases:
    """
    Тесты граничных случаев и особых сценариев
    """

    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        self.headers = headers
        self.created_review_ids = []

    def teardown_method(self, method):
        for review_id in self.created_review_ids:
            try:
                requests.delete(
                    f"{BASE_URL}/admin/reviews/{review_id}",
                    headers=self.headers,
                    timeout=5
                )
            except:
                pass

    @pytest.mark.advanced
    def test_create_review_with_unicode_characters(self):
        """
        Тест с Unicode символами

        Test Case: TC_ADV_REV_013

        Expected: Unicode символы обрабатываются корректно
        """
        review_data = {
            "name": "田中太郎",  # Японский
            "car_brand": "トヨタ",  # Катакана
            "car_model": "Camry",
            "rating": 5,
            "text": "素晴らしいサービス！🚗🎉"  # С эмодзи
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 201
        self.created_review_ids.append(response.json()["review"]["id"])

    @pytest.mark.advanced
    def test_create_review_with_whitespace(self):
        """
        Тест с пробельными символами

        Test Case: TC_ADV_REV_014

        Expected: Пробелы обрабатываются корректно
        """
        review_data = {
            "name": "  Иван  ",  # С пробелами
            "car_brand": " Toyota ",
            "car_model": " Camry ",
            "rating": 5,
            "text": "  Отличный сервис  "
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 201
        self.created_review_ids.append(response.json()["review"]["id"])

    @pytest.mark.advanced
    def test_delete_nonexistent_review(self):
        """
        Тест удаления несуществующего отзыва

        Test Case: TC_ADV_REV_015

        Expected: 404 ошибка
        """
        response = requests.delete(
            f"{BASE_URL}/admin/reviews/nonexistent_id_12345",
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 404

    @pytest.mark.advanced
    def test_update_with_partial_data(self):
        """
        Тест обновления с частичными данными

        Test Case: TC_ADV_REV_016

        Expected: Обновление только указанных полей
        """
        # Создаём
        create_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 3,
            "text": "Тест"
        }

        create_response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=create_data,
            headers=self.headers,
            timeout=10
        )

        review_id = create_response.json()["review"]["id"]
        self.created_review_ids.append(review_id)

        # Обновляем только рейтинг и текст
        update_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 5,
            "text": "Обновлённый текст"
        }

        update_response = requests.put(
            f"{BASE_URL}/admin/reviews/{review_id}",
            json=update_data,
            headers=self.headers,
            timeout=10
        )

        assert update_response.status_code == 200
        assert update_response.json()["review"]["rating"] == 5
        assert update_response.json()["review"]["text"] == "Обновлённый текст"

    @pytest.mark.advanced
    def test_stats_accuracy(self):
        """
        Тест точности статистики

        Test Case: TC_ADV_REV_017

        Expected: Статистика рассчитывается корректно
        """
        # Создаём отзывы с известными рейтингами
        ratings = [5, 4, 3, 2, 1]
        expected_avg = sum(ratings) / len(ratings)

        try:
            for rating in ratings:
                review_data = {
                    "name": f"Клиент {rating}",
                    "car_brand": "Toyota",
                    "car_model": "Camry",
                    "rating": rating,
                    "text": "Тест"
                }

                response = requests.post(
                    f"{BASE_URL}/admin/reviews/",
                    json=review_data,
                    headers=self.headers,
                    timeout=10
                )

                assert response.status_code == 201
                self.created_review_ids.append(response.json()["review"]["id"])

            # Проверяем статистику
            stats_response = requests.get(
                f"{BASE_URL}/admin/reviews/stats",
                headers=self.headers,
                timeout=10
            )

            stats = stats_response.json()["stats"]

            assert stats["total_reviews"] >= 5, "Not enough reviews"

            # Проверяем средний рейтинг с допустимой погрешностью
            assert abs(stats["average_rating"] - expected_avg) < 0.1, \
                f"Average rating is {stats['average_rating']}, expected {expected_avg}"

            # Проверяем распределение
            rating_breakdown = stats["rating_breakdown"]
            for rating in ["1", "2", "3", "4", "5"]:
                assert rating in rating_breakdown or int(rating) in rating_breakdown, \
                    f"Rating {rating} not in breakdown"

        except Exception as e:
            pytest.fail(f"Stats test failed: {str(e)}")


class TestReviewsLoadTesting:
    """
    Нагрузочные тесты
    """

    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        self.headers = headers
        self.created_review_ids = []

    def teardown_method(self, method):
        for review_id in self.created_review_ids:
            try:
                requests.delete(
                    f"{BASE_URL}/admin/reviews/{review_id}",
                    headers=self.headers,
                    timeout=5
                )
            except:
                pass

    @pytest.mark.advanced
    @pytest.mark.performance
    def test_bulk_review_creation(self):
        """
        Массовое создание отзывов

        Test Case: TC_ADV_REV_018

        Expected: 50 отзывов создаются за разумное время
        """
        start_time = time.time()

        try:
            for i in range(50):
                review_data = {
                    "name": f"Массовый клиент {i}",
                    "car_brand": random.choice(["Toyota", "BMW", "Mercedes", "Audi"]),
                    "car_model": random.choice(["Camry", "X5", "E-Class", "A4"]),
                    "rating": random.randint(1, 5),
                    "text": f"Массовый отзыв номер {i}"
                }

                response = requests.post(
                    f"{BASE_URL}/admin/reviews/",
                    json=review_data,
                    headers=self.headers,
                    timeout=10
                )

                assert response.status_code == 201, \
                    f"Review {i} failed: {response.status_code}"

                self.created_review_ids.append(response.json()["review"]["id"])

            end_time = time.time()
            total_time = end_time - start_time

            print(f"\n⏱️ Created 50 reviews in {total_time:.2f} seconds")
            print(f"📊 Average: {total_time/50*1000:.2f}ms per review")

            assert total_time < 60, f"Bulk creation took too long: {total_time}s"

        except Exception as e:
            pytest.fail(f"Bulk creation failed: {str(e)}")

    @pytest.mark.advanced
    @pytest.mark.performance
    def test_api_response_time_under_load(self):
        """
        Тест времени ответа под нагрузкой

        Test Case: TC_ADV_REV_019

        Expected: Время ответа остаётся приемлемым
        """
        # Сначала создаём нагрузку (10 отзывов)
        for i in range(10):
            review_data = {
                "name": f"Нагрузка {i}",
                "car_brand": "Toyota",
                "car_model": "Camry",
                "rating": 5,
                "text": "Тест"
            }

            response = requests.post(
                f"{BASE_URL}/admin/reviews/",
                json=review_data,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 201:
                self.created_review_ids.append(response.json()["review"]["id"])

        # Замеряем время ответа GET запроса
        response_times = []

        for _ in range(5):
            start = time.time()
            response = requests.get(
                f"{BASE_URL}/admin/reviews/",
                headers=self.headers,
                timeout=10
            )
            end = time.time()

            assert response.status_code == 200
            response_times.append((end - start) * 1000)  # ms

        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)

        print(f"\n⏱️ Average response time: {avg_response_time:.2f}ms")
        print(f"⏱️ Max response time: {max_response_time:.2f}ms")

        assert avg_response_time < 1000, f"Average response time too high: {avg_response_time}ms"
        assert max_response_time < 2000, f"Max response time too high: {max_response_time}ms"
