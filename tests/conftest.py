import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def browser():
    # Настройка драйвера
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # для CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def app_url():
    return "http://localhost:8000/?balance=30000&reserved=20001"