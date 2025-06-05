import os
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
    
    driver_path = ChromeDriverManager().install()
    if "THIRD_PARTY_NOTICES" in driver_path:
        driver_path = driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver")
        os.chmod(driver_path, 0o755)

    driver = webdriver.Chrome(
        service=ChromeService(driver_path),
        options=options,
    )
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def app_url():
    return "http://localhost:8000/?balance=30000&reserved=20001"