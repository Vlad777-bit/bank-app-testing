from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_card_number_validation(browser, app_url):
    """Тестирование формы ввода карты на валидацию номера карты"""
    browser.get(app_url)
    
    # Находим поле ввода номера карты
    card_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='Номер карты']")
    
    # Вводим 17 символов
    card_input.send_keys("9999 9999 9999 9999 9")
    
    # Проверяем, что введено не более 16 символов
    assert len(card_input.get_attribute("value").replace(" ", "")) <= 16

def test_balance_input_validation(browser, app_url):
    """Ввод некорректных значений в баланс счета"""
    browser.get(app_url.replace("balance=30000", "balance=gdd"))
    
    # Проверяем отображение NaN
    balance_element = browser.find_element(By.XPATH, "//div[contains(text(), 'На счету:')]")
    assert "NaN" not in balance_element.text

def test_currency_switch(browser, app_url):
    """Проверка актуального остатка после переключения на другую валюту"""
    browser.get(app_url)
    
    # Находим элементы для перевода
    amount_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='Сумма перевода']")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    # Вводим сумму перевода
    amount_input.send_keys("22500")
    submit_button.click()
    
    # Переключаемся на доллары
    dollar_tab = browser.find_element(By.XPATH, "//button[contains(text(), 'Доллары')]")
    dollar_tab.click()
    
    # Проверяем, что перевод невозможен (должен быть disabled)
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    assert submit_button.is_enabled() is False

def test_card_input_character_validation(browser, app_url):
    """Тестирование формы ввода карты на валидацию символов"""
    browser.get(app_url)
    
    card_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='Номер карты']")
    card_input.send_keys("abcd")
    
    assert card_input.get_attribute("value") == ""

def test_insufficient_funds(browser, app_url):
    """Тестирование механизма запрета перевода при недостатке средств"""
    browser.get(app_url)
    
    amount_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='Сумма перевода']")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    amount_input.send_keys("288000")
    submit_button.click()
    
    # Проверяем сообщение об ошибке
    error_message = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message"))
    )
    assert "Недостаточно средств на счете" in error_message.text