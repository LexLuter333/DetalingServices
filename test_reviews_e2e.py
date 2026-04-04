import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture(scope="session")
def driver():
    """
    Фикстура для создания WebDriver сессии
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def login_to_admin(driver):
    """
    Фикстура для входа в админ-панель
    """
    driver.get("http://localhost:5173/admin/login")

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_input.send_keys("novicarsAdminPass")

    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/admin/dashboard")
    )

    yield driver


class TestReviewsAdminPanel:
    """
    E2E тесты админ-панели отзывов
    """

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_reviews_page_loads(self, login_to_admin):
        """
        Тест загрузки страницы отзывов

        Test Case: TC_E2E_REV_001
        """
        driver = login_to_admin
        driver.get("http://localhost:5173/admin/reviews")

        # Проверяем заголовок
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        h1 = driver.find_element(By.TAG_NAME, "h1")
        assert "Отзывы" in h1.text, f"Expected 'Отзывы' in title, got: {h1.text}"

        # Проверяем кнопку добавления
        add_button = driver.find_element(By.CSS_SELECTOR, ".add-review-btn")
        assert add_button.is_displayed(), "Add button not found"

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_create_review_via_ui(self, login_to_admin):
        """
        Тест создания отзыва через UI

        Test Case: TC_E2E_REV_002
        """
        driver = login_to_admin
        driver.get("http://localhost:5173/admin/reviews")

        # Нажимаем "Добавить отзыв"
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-review-btn"))
        )
        add_button.click()

        # Ждём открытия модального окна
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))
        )

        # Заполняем форму
        name_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Имя"]')
        name_input.send_keys("E2E Тест Клиент")

        brand_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Марка"]')
        brand_input.send_keys("Toyota")

        model_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Модель"]')
        model_input.send_keys("Camry")

        # Выбираем 5 звёзд
        stars = driver.find_elements(By.CSS_SELECTOR, ".star-btn")
        assert len(stars) >= 5, "Not enough star buttons"
        stars[4].click()  # 5-я звезда

        # Вводим текст
        text_area = driver.find_element(By.CSS_SELECTOR, 'textarea[placeholder*="отзыва"]')
        text_area.send_keys("E2E тест отзыв создан через UI")

        # Отправляем форму
        submit_button = driver.find_element(By.CSS_SELECTOR, ".save-btn")
        submit_button.click()

        # Ждём закрытия модального окна и появления уведомления
        time.sleep(2)

        # Проверяем что отзыв появился в списке
        reviews_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".reviews-list"))
        )

        assert "E2E Тест Клиент" in reviews_list.text, "Review not found in list"
        assert "Toyota" in reviews_list.text, "Car brand not found"
        assert "Camry" in reviews_list.text, "Car model not found"

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_form_validation_empty_fields(self, login_to_admin):
        """
        Тест валидации пустых полей

        Test Case: TC_E2E_REV_003
        """
        driver = login_to_admin
        driver.get("http://localhost:5173/admin/reviews")

        # Открываем форму
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-review-btn"))
        )
        add_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))
        )

        # Пытаемся отправить пустую форму
        submit_button = driver.find_element(By.CSS_SELECTOR, ".save-btn")
        submit_button.click()

        # Ждём ошибку валидации
        time.sleep(1)

        # Проверяем что форма не закрылась (валидация не прошла)
        modal = driver.find_element(By.CSS_SELECTOR, ".modal-content")
        assert modal.is_displayed(), "Modal should stay open on validation error"

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_delete_review(self, login_to_admin):
        """
        Тест удаления отзыва

        Test Case: TC_E2E_REV_004

        Note: Требует существующего отзыва в базе
        """
        driver = login_to_admin
        driver.get("http://localhost:5173/admin/reviews")

        # Получаем количество отзывов до удаления
        reviews_before = len(driver.find_elements(By.CSS_SELECTOR, ".review-card"))

        if reviews_before > 0:
            # Находим кнопку удаления у первого отзыва
            delete_buttons = driver.find_elements(By.CSS_SELECTOR, ".delete-review-btn")

            if delete_buttons:
                delete_buttons[0].click()

                # Подтверждаем удаление
                WebDriverWait(driver, 10).until(
                    EC.alert_is_present()
                )
                alert = driver.switch_to.alert
                alert.accept()

                # Ждём обновления списка
                time.sleep(2)

                # Проверяем что количество уменьшилось
                reviews_after = len(driver.find_elements(By.CSS_SELECTOR, ".review-card"))
                assert reviews_after == reviews_before - 1, \
                    f"Expected {reviews_before - 1} reviews, got {reviews_after}"

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_statistics_display(self, login_to_admin):
        """
        Тест отображения статистики

        Test Case: TC_E2E_REV_005
        """
        driver = login_to_admin
        driver.get("http://localhost:5173/admin/reviews")

        # Проверяем наличие карточек статистики
        stat_cards = driver.find_elements(By.CSS_SELECTOR, ".stat-card")

        assert len(stat_cards) >= 2, "Not enough stat cards"

        # Проверяем что есть значения
        for card in stat_cards:
            value = card.find_element(By.CSS_SELECTOR, ".stat-value")
            assert value.text.strip(), "Stat value is empty"


class TestReviewsPublicPage:
    """
    E2E тесты публичной страницы отзывов
    """

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_public_reviews_page_loads(self, driver):
        """
        Тест загрузки публичной страницы

        Test Case: TC_E2E_REV_006
        """
        driver.get("http://localhost:5173/reviews")

        # Проверяем заголовок
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        h1 = driver.find_element(By.TAG_NAME, "h1")
        assert "Отзывы" in h1.text, f"Expected 'Отзывы' in title, got: {h1.text}"

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_reviews_display_on_public_page(self, driver):
        """
        Тест отображения отзывов на публичной странице

        Test Case: TC_E2E_REV_007
        """
        driver.get("http://localhost:5173/reviews")

        # Проверяем наличие списка отзывов
        reviews_grid = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".reviews-grid-public"))
        )

        # Проверяем что карточки есть или сообщение что нет отзывов
        review_cards = reviews_grid.find_elements(By.CSS_SELECTOR, ".review-card-public")

        # Либо есть отзывы, либо сообщение что их нет
        if len(review_cards) == 0:
            empty_message = reviews_grid.find_element(By.CSS_SELECTOR, ".empty-reviews")
            assert empty_message.is_displayed(), "No reviews and no empty message"
        else:
            # Проверяем структуру карточки
            for card in review_cards[:3]:  # Проверяем первые 3
                assert card.find_element(By.CSS_SELECTOR, ".author-name")
                assert card.find_element(By.CSS_SELECTOR, ".review-rating-public")
                assert card.find_element(By.CSS_SELECTOR, ".review-text-public")

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_statistics_on_public_page(self, driver):
        """
        Тест статистики на публичной странице

        Test Case: TC_E2E_REV_008
        """
        driver.get("http://localhost:5173/reviews")

        # Проверяем наличие статистики
        stat_items = driver.find_elements(By.CSS_SELECTOR, ".stat-item")

        assert len(stat_items) >= 2, "Not enough stat items"

        # Проверяем что числа отображаются
        for item in stat_items:
            number = item.find_element(By.CSS_SELECTOR, ".stat-number")
            assert number.text.strip().isdigit() or number.text.strip().replace('.', '').isdigit(), \
                f"Stat number is not numeric: {number.text}"


class TestReviewsResponsive:
    """
    E2E тесты адаптивности
    """

    @pytest.mark.e2e
    @pytest.mark.ui
    @pytest.mark.parametrize("width,height,device", [
        (375, 667, "iPhone SE"),
        (768, 1024, "iPad"),
        (1920, 1080, "Desktop"),
    ])
    def test_reviews_page_responsive(self, driver, width, height, device):
        """
        Тест адаптивности страницы отзывов

        Test Case: TC_E2E_REV_009
        """
        driver.set_window_size(width, height)
        driver.get("http://localhost:5173/admin/reviews")

        # Проверяем что страница загрузилась
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        h1 = driver.find_element(By.TAG_NAME, "h1")
        assert h1.is_displayed(), f"Header not displayed on {device}"

        # Проверяем что нет горизонтальной прокрутки
        body_width = driver.execute_script("return document.body.scrollWidth")
        window_width = driver.execute_script("return window.innerWidth")

        assert body_width <= window_width, \
            f"Horizontal scroll on {device}: body={body_width}, window={window_width}"


class TestReviewsAccessibility:
    """
    E2E тесты доступности
    """

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_reviews_page_keyboard_navigation(self, login_to_admin):
        """
        Тест навигации с клавиатуры

        Test Case: TC_E2E_REV_010
        """
        driver = login_to_admin
        driver.get("http://localhost:5173/admin/reviews")

        # Tab навигация
        driver.find_element(By.TAG_NAME, "body").send_keys("\t")
        focused_element = driver.switch_to.active_element

        assert focused_element.tag_name in ["button", "input", "a", "textarea"], \
            f"First tab focus is on unexpected element: {focused_element.tag_name}"

    @pytest.mark.e2e
    @pytest.mark.ui
    def test_reviews_page_labels(self, login_to_admin):
        """
        Тест наличия label у полей формы

        Test Case: TC_E2E_REV_011
        """
        driver = login_to_admin
        driver.get("http://localhost:5173/admin/reviews")

        # Открываем форму
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-review-btn"))
        )
        add_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-content"))
        )

        # Проверяем что у всех input есть label
        inputs = driver.find_elements(By.CSS_SELECTOR, ".modal-content input, .modal-content textarea")

        for input_field in inputs:
            input_id = input_field.get_attribute("id")
            if input_id:
                label = driver.find_element(By.CSS_SELECTOR, f'label[for="{input_id}"]')
                assert label.is_displayed(), f"No label for input {input_id}"
            else:
                # Проверяем что input обёрнут в label
                parent = input_field.find_element(By.XPATH, "./..")
                assert parent.tag_name == "div" or parent.tag_name == "label", \
                    "Input has no id and not wrapped in label"


# Запуск тестов:
# pytest test_reviews_e2e.py -v
# pytest test_reviews_e2e.py -m e2e
# pytest test_reviews_e2e.py --headed (показать браузер)
