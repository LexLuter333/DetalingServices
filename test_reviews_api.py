import pytest
import requests
from conftest import BASE_URL


class TestPublicReviewsAPI:
    """
    Тестирование публичного API отзывов (без авторизации)

    Endpoints:
    - GET /api/reviews/
    """

    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_public_reviews_success(self):
        """
        Тест успешного получения списка отзывов

        Test Case: TC_REVIEWS_001

        Steps:
        1. Отправить GET запрос на /api/reviews/
        2. Проверить статус код 200
        3. Проверить наличие ключа 'reviews'

        Expected:
        - Status code: 200
        - Reviews list exists
        - Each review has required fields
        """
        # Act
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)

        # Assert
        assert response.status_code == 200, f"Status code is {response.status_code}"

        response_data = response.json()
        assert "reviews" in response_data, "'reviews' key not found"
        assert isinstance(response_data["reviews"], list), "Reviews is not a list"

        print(f"✅ Got {len(response_data['reviews'])} reviews")

    @pytest.mark.smoke
    @pytest.mark.api
    def test_review_structure(self):
        """
        Тест структуры данных отзыва

        Test Case: TC_REVIEWS_002

        Expected:
        - Each review has: id, name, car_brand, car_model, rating, text, created_at
        - Correct data types
        """
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)

        # Если отзывов нет, пропускаем тест
        if len(response.json()["reviews"]) == 0:
            pytest.skip("No reviews available for structure test")

        reviews = response.json()["reviews"]
        review = reviews[0]

        # Assert - Required fields
        assert "id" in review, "Review ID not found"
        assert "name" in review, "Review name not found"
        assert "car_brand" in review, "Review car_brand not found"
        assert "car_model" in review, "Review car_model not found"
        assert "rating" in review, "Review rating not found"
        assert "text" in review, "Review text not found"
        assert "created_at" in review, "Review created_at not found"

        # Assert - Data types
        assert isinstance(review["id"], str), "ID should be string"
        assert isinstance(review["name"], str), "Name should be string"
        assert isinstance(review["car_brand"], str), "Car brand should be string"
        assert isinstance(review["car_model"], str), "Car model should be string"
        assert isinstance(review["rating"], int), "Rating should be integer"
        assert isinstance(review["text"], str), "Text should be string"

    @pytest.mark.regression
    @pytest.mark.api
    def test_reviews_sorted_by_date(self):
        """
        Тест сортировки отзывов по дате (новые сначала)

        Test Case: TC_REVIEWS_003

        Expected: Reviews sorted by created_at DESC
        """
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)
        reviews = response.json()["reviews"]

        if len(reviews) <= 1:
            pytest.skip("Not enough reviews to test sorting")

        # Проверяем что отзывы отсортированы по убыванию даты
        dates = [r["created_at"] for r in reviews]
        assert dates == sorted(dates, reverse=True), "Reviews are not sorted by date DESC"

    @pytest.mark.regression
    @pytest.mark.api
    def test_review_rating_range(self):
        """
        Тест диапазона рейтингов (1-5)

        Test Case: TC_REVIEWS_004

        Expected: All ratings between 1 and 5
        """
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)
        reviews = response.json()["reviews"]

        for review in reviews:
            assert 1 <= review["rating"] <= 5, \
                f"Rating {review['rating']} is out of range [1, 5]"

    @pytest.mark.regression
    @pytest.mark.api
    def test_review_name_not_empty(self):
        """
        Тест что имя клиента не пустое

        Test Case: TC_REVIEWS_005

        Expected: All names are non-empty strings
        """
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)
        reviews = response.json()["reviews"]

        for review in reviews:
            assert review["name"] and len(review["name"].strip()) > 0, \
                f"Review {review['id']} has empty name"

    @pytest.mark.regression
    @pytest.mark.api
    def test_review_text_not_empty(self):
        """
        Тест что текст отзыва не пустой

        Test Case: TC_REVIEWS_006

        Expected: All texts are non-empty strings
        """
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)
        reviews = response.json()["reviews"]

        for review in reviews:
            assert review["text"] and len(review["text"].strip()) > 0, \
                f"Review {review['id']} has empty text"

    @pytest.mark.regression
    @pytest.mark.api
    def test_review_car_brand_not_empty(self):
        """
        Тест что марка автомобиля не пустая

        Test Case: TC_REVIEWS_007

        Expected: All car brands are non-empty strings
        """
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)
        reviews = response.json()["reviews"]

        for review in reviews:
            assert review["car_brand"] and len(review["car_brand"].strip()) > 0, \
                f"Review {review['id']} has empty car_brand"

    @pytest.mark.performance
    @pytest.mark.api
    def test_reviews_response_time(self):
        """
        Тест времени ответа API отзывов

        Test Case: TC_REVIEWS_008

        Expected: Response time < 1 second
        """
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)

        response_time = response.elapsed.total_seconds()
        assert response_time < 1.0, \
            f"Response time is {response_time}s, expected < 1.0s"
        print(f"⏱️ Response time: {response_time:.3f}s")

    @pytest.mark.performance
    @pytest.mark.api
    def test_reviews_response_size(self):
        """
        Тест размера ответа API отзывов

        Test Case: TC_REVIEWS_009

        Expected: Response size < 100KB
        """
        response = requests.get(f"{BASE_URL}/reviews/", timeout=10)

        response_size = len(response.content)
        assert response_size < 100 * 1024, \
            f"Response size is {response_size} bytes, expected < 100KB"
        print(f"📦 Response size: {response_size} bytes")

    @pytest.mark.api
    def test_reviews_with_limit_parameter(self):
        """
        Тест параметра limit

        Test Case: TC_REVIEWS_010

        Expected: Returns limited number of reviews
        """
        response = requests.get(f"{BASE_URL}/reviews/?limit=5", timeout=10)
        reviews = response.json()["reviews"]

        assert len(reviews) <= 5, f"Expected <= 5 reviews, got {len(reviews)}"


class TestAdminReviewsAPI:
    """
    Тестирование админского API отзывов (требуется авторизация)

    Endpoints:
    - GET /api/admin/reviews/
    - POST /api/admin/reviews/
    - PUT /api/admin/reviews/:id
    - DELETE /api/admin/reviews/:id
    - GET /api/admin/reviews/stats
    """

    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        """Автоматическая установка заголовков авторизации"""
        self.headers = headers
        self.auth_token = auth_token

    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_admin_reviews_success(self):
        """
        Тест получения всех отзывов админом

        Test Case: TC_REVIEWS_011

        Expected: Status code 200, reviews list
        """
        response = requests.get(
            f"{BASE_URL}/admin/reviews/",
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 200, f"Status code is {response.status_code}"
        assert "reviews" in response.json(), "'reviews' key not found"

    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_review_success(self):
        """
        Тест успешного создания отзыва

        Test Case: TC_REVIEWS_012

        Steps:
        1. Отправить POST запрос с данными отзыва
        2. Проверить статус код 201
        3. Проверить что отзыв создан

        Expected:
        - Status code: 201
        - Review created in response
        - Review name matches
        """
        # Arrange
        review_data = {
            "name": "Тестовый Клиент",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 5,
            "text": "Отличный сервис! Быстро и качественно сделали работу. Рекомендую!"
        }

        # Act
        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        # Assert
        assert response.status_code == 201, f"Status code is {response.status_code}"

        response_data = response.json()
        assert "message" in response_data, "Message not found"
        assert "review" in response_data, "Review not found"
        assert response_data["review"]["name"] == review_data["name"]
        assert response_data["review"]["car_brand"] == review_data["car_brand"]
        assert response_data["review"]["car_model"] == review_data["car_model"]
        assert response_data["review"]["rating"] == review_data["rating"]
        assert response_data["review"]["text"] == review_data["text"]

        # Cleanup - удаляем созданный отзыв
        review_id = response_data["review"]["id"]
        requests.delete(
            f"{BASE_URL}/admin/reviews/{review_id}",
            headers=self.headers,
            timeout=5
        )

        print(f"✅ Review created and cleaned up: {review_data['name']}")

    @pytest.mark.regression
    @pytest.mark.api
    def test_create_review_without_auth(self):
        """
        Тест создания отзыва без авторизации

        Test Case: TC_REVIEWS_013

        Expected: Status code 401
        """
        review_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 5,
            "text": "Тестовый отзыв"
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            timeout=10
        )

        assert response.status_code == 401, "Should return 401 without auth"

    @pytest.mark.regression
    @pytest.mark.api
    def test_create_review_with_empty_name(self):
        """
        Тест создания отзыва с пустым именем

        Test Case: TC_REVIEWS_014

        Expected: Status code 400
        """
        review_data = {
            "name": "",
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

        assert response.status_code == 400, "Should return 400 for empty name"

    @pytest.mark.regression
    @pytest.mark.api
    def test_create_review_with_empty_car_brand(self):
        """
        Тест создания отзыва с пустой маркой авто

        Test Case: TC_REVIEWS_015

        Expected: Status code 400
        """
        review_data = {
            "name": "Тест",
            "car_brand": "",
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

        assert response.status_code == 400, "Should return 400 for empty car_brand"

    @pytest.mark.regression
    @pytest.mark.api
    def test_create_review_with_empty_car_model(self):
        """
        Тест создания отзыва с пустой моделью авто

        Test Case: TC_REVIEWS_016

        Expected: Status code 400
        """
        review_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "",
            "rating": 5,
            "text": "Тестовый отзыв"
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 400, "Should return 400 for empty car_model"

    @pytest.mark.regression
    @pytest.mark.api
    def test_create_review_with_empty_text(self):
        """
        Тест создания отзыва с пустым текстом

        Test Case: TC_REVIEWS_017

        Expected: Status code 400
        """
        review_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 5,
            "text": ""
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 400, "Should return 400 for empty text"

    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.parametrize("rating", [0, 6, 10, -1])
    def test_create_review_with_invalid_rating(self, rating):
        """
        Тест создания отзыва с невалидным рейтингом

        Test Case: TC_REVIEWS_018

        Expected: Status code 400
        """
        review_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": rating,
            "text": "Тестовый отзыв"
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 400, f"Should return 400 for rating {rating}"

    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.parametrize("valid_rating", [1, 2, 3, 4, 5])
    def test_create_review_with_valid_ratings(self, valid_rating):
        """
        Тест создания отзыва с валидными рейтингами

        Test Case: TC_REVIEWS_019

        Expected: Status code 201
        """
        review_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": valid_rating,
            "text": "Тестовый отзыв"
        }

        response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=review_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 201, f"Should return 201 for rating {valid_rating}"

        # Cleanup
        review_id = response.json()["review"]["id"]
        requests.delete(
            f"{BASE_URL}/admin/reviews/{review_id}",
            headers=self.headers,
            timeout=5
        )

    @pytest.mark.smoke
    @pytest.mark.api
    def test_update_review_success(self):
        """
        Тест успешного обновления отзыва

        Test Case: TC_REVIEWS_020

        Expected: Status code 200, review updated
        """
        # Сначала создаём отзыв
        create_data = {
            "name": "Тестовый Клиент",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 4,
            "text": "Хороший сервис"
        }

        create_response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=create_data,
            headers=self.headers,
            timeout=10
        )

        review_id = create_response.json()["review"]["id"]

        # Обновляем отзыв
        update_data = {
            "name": "Обновлённый Клиент",
            "car_brand": "BMW",
            "car_model": "X5",
            "rating": 5,
            "text": "Отличный сервис! Обновлённый текст."
        }

        response = requests.put(
            f"{BASE_URL}/admin/reviews/{review_id}",
            json=update_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 200, f"Status code is {response.status_code}"
        assert response.json()["review"]["name"] == "Обновлённый Клиент"
        assert response.json()["review"]["car_brand"] == "BMW"
        assert response.json()["review"]["car_model"] == "X5"
        assert response.json()["review"]["rating"] == 5

        # Cleanup
        requests.delete(
            f"{BASE_URL}/admin/reviews/{review_id}",
            headers=self.headers,
            timeout=5
        )

    @pytest.mark.regression
    @pytest.mark.api
    def test_update_nonexistent_review(self):
        """
        Тест обновления несуществующего отзыва

        Test Case: TC_REVIEWS_021

        Expected: Status code 404
        """
        update_data = {
            "name": "Тест",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 5,
            "text": "Тест"
        }

        response = requests.put(
            f"{BASE_URL}/admin/reviews/nonexistent_id",
            json=update_data,
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 404, "Should return 404 for nonexistent review"

    @pytest.mark.smoke
    @pytest.mark.api
    def test_delete_review_success(self):
        """
        Тест успешного удаления отзыва

        Test Case: TC_REVIEWS_022

        Expected: Status code 200, review deleted
        """
        # Создаём отзыв
        create_data = {
            "name": "Тестовый Клиент",
            "car_brand": "Toyota",
            "car_model": "Camry",
            "rating": 5,
            "text": "Тестовый отзыв для удаления"
        }

        create_response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=create_data,
            headers=self.headers,
            timeout=10
        )

        review_id = create_response.json()["review"]["id"]

        # Удаляем отзыв
        response = requests.delete(
            f"{BASE_URL}/admin/reviews/{review_id}",
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 200, f"Status code is {response.status_code}"
        assert "message" in response.json()
        print(f"✅ Review deleted: {review_id}")

    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_nonexistent_review(self):
        """
        Тест удаления несуществующего отзыва

        Test Case: TC_REVIEWS_023

        Expected: Status code 404
        """
        response = requests.delete(
            f"{BASE_URL}/admin/reviews/nonexistent_id",
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 404, "Should return 404"

    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_review_stats_success(self):
        """
        Тест получения статистики отзывов

        Test Case: TC_REVIEWS_024

        Expected: Status code 200, stats object
        """
        response = requests.get(
            f"{BASE_URL}/admin/reviews/stats",
            headers=self.headers,
            timeout=10
        )

        assert response.status_code == 200, f"Status code is {response.status_code}"
        assert "stats" in response.json(), "'stats' key not found"

        stats = response.json()["stats"]
        assert "total_reviews" in stats, "total_reviews not found"
        assert "average_rating" in stats, "average_rating not found"
        assert "rating_breakdown" in stats, "rating_breakdown not found"
        assert "recent_reviews" in stats, "recent_reviews not found"

    @pytest.mark.regression
    @pytest.mark.api
    def test_review_stats_average_rating(self):
        """
        Тест среднего рейтинга в статистике

        Test Case: TC_REVIEWS_025

        Expected: Average rating between 1.0 and 5.0
        """
        response = requests.get(
            f"{BASE_URL}/admin/reviews/stats",
            headers=self.headers,
            timeout=10
        )

        stats = response.json()["stats"]

        if stats["total_reviews"] > 0:
            assert 1.0 <= stats["average_rating"] <= 5.0, \
                f"Average rating {stats['average_rating']} is out of range"

    @pytest.mark.regression
    @pytest.mark.api
    def test_review_stats_rating_breakdown(self):
        """
        Тест распределения рейтингов в статистике

        Test Case: TC_REVIEWS_026

        Expected: rating_breakdown contains keys 1-5
        """
        response = requests.get(
            f"{BASE_URL}/admin/reviews/stats",
            headers=self.headers,
            timeout=10
        )

        stats = response.json()["stats"]
        rating_breakdown = stats["rating_breakdown"]

        # Проверяем что есть ключи для всех рейтингов 1-5
        for rating in ["1", "2", "3", "4", "5"]:
            assert rating in rating_breakdown or int(rating) in rating_breakdown, \
                f"Rating {rating} not found in breakdown"


class TestReviewsIntegration:
    """
    Интеграционные тесты для Reviews API

    Test complete workflows
    """

    @pytest.fixture(autouse=True)
    def setup_auth(self, auth_token, headers):
        """Автоматическая установка заголовков авторизации"""
        self.headers = headers

    @pytest.mark.integration
    def test_full_review_lifecycle(self):
        """
        Полный жизненный цикл отзыва

        Test Case: TC_REVIEWS_027

        Steps:
        1. Создать отзыв
        2. Проверить что он в списке
        3. Обновить отзыв
        4. Проверить изменения
        5. Удалить отзыв
        6. Проверить что удалён

        Expected: All operations successful
        """
        # 1. Create
        create_data = {
            "name": "Интеграционный Тест",
            "car_brand": "Mercedes",
            "car_model": "E-Class",
            "rating": 5,
            "text": "Интеграционный тест отзыва"
        }

        create_response = requests.post(
            f"{BASE_URL}/admin/reviews/",
            json=create_data,
            headers=self.headers,
            timeout=10
        )

        assert create_response.status_code == 201
        review_id = create_response.json()["review"]["id"]

        # 2. Verify in list
        list_response = requests.get(
            f"{BASE_URL}/admin/reviews/",
            headers=self.headers,
            timeout=10
        )

        reviews = list_response.json()["reviews"]
        review_ids = [r["id"] for r in reviews]
        assert review_id in review_ids, "Created review not found in list"

        # 3. Update
        update_data = {
            "name": "Обновлённый Интеграционный Тест",
            "car_brand": "BMW",
            "car_model": "M5",
            "rating": 4,
            "text": "Обновлённый текст интеграционного теста"
        }

        update_response = requests.put(
            f"{BASE_URL}/admin/reviews/{review_id}",
            json=update_data,
            headers=self.headers,
            timeout=10
        )

        assert update_response.status_code == 200
        assert update_response.json()["review"]["name"] == "Обновлённый Интеграционный Тест"

        # 4. Delete
        delete_response = requests.delete(
            f"{BASE_URL}/admin/reviews/{review_id}",
            headers=self.headers,
            timeout=10
        )

        assert delete_response.status_code == 200

        # 5. Verify deleted
        list_response_after = requests.get(
            f"{BASE_URL}/admin/reviews/",
            headers=self.headers,
            timeout=10
        )

        reviews_after = list_response_after.json()["reviews"]
        review_ids_after = [r["id"] for r in reviews_after]
        assert review_id not in review_ids_after, "Deleted review still in list"

        print(f"✅ Full review lifecycle test passed: {review_id}")

    @pytest.mark.integration
    def test_multiple_reviews_creation(self):
        """
        Тест создания нескольких отзывов

        Test Case: TC_REVIEWS_028

        Expected: Multiple reviews created successfully
        """
        test_data = [
            {"name": "Клиент 1", "car_brand": "Toyota", "car_model": "Camry", "rating": 5, "text": "Отлично"},
            {"name": "Клиент 2", "car_brand": "BMW", "car_model": "X5", "rating": 4, "text": "Хорошо"},
            {"name": "Клиент 3", "car_brand": "Mercedes", "car_model": "E-Class", "rating": 5, "text": "Превосходно"},
        ]

        created_ids = []

        try:
            # Create multiple reviews
            for data in test_data:
                response = requests.post(
                    f"{BASE_URL}/admin/reviews/",
                    json=data,
                    headers=self.headers,
                    timeout=10
                )
                assert response.status_code == 201
                created_ids.append(response.json()["review"]["id"])

            # Verify all exist
            list_response = requests.get(
                f"{BASE_URL}/admin/reviews/",
                headers=self.headers,
                timeout=10
            )

            reviews = list_response.json()["reviews"]
            review_ids = [r["id"] for r in reviews]

            for created_id in created_ids:
                assert created_id in review_ids, f"Review {created_id} not found"

            print(f"✅ Created {len(created_ids)} reviews successfully")

        finally:
            # Cleanup
            for review_id in created_ids:
                requests.delete(
                    f"{BASE_URL}/admin/reviews/{review_id}",
                    headers=self.headers,
                    timeout=5
                )
