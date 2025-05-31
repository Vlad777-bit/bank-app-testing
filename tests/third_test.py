from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

def test_negative_balance(browser):
    """Ввод отрицательного баланса счета"""
    browser.get("http://localhost:8000/?balance=-38000")
    
    try:
        balance_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'На счету:')]"))
        )
        assert "-" not in balance_element.text
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_commission_for_100(browser, app_url):
    """Тестирование расчета комиссии"""
    browser.get(app_url)
    
    try:
        amount_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[name='amount']"))
        )
        amount_input.send_keys("100")
        
        commission_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".commission, [data-testid='commission']"))
        )
        assert "10" in commission_element.text
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_invalid_card_number(browser, app_url):
    """Проверка валидации номера карты"""
    browser.get(app_url)
    
    try:
        card_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][placeholder*='карты'], input[name='card']"))
        )
        card_input.send_keys("1111 1111 1111 1111")
        
        submit_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], [data-testid='submit']"))
        )
        submit_button.click()
        
        error_message = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message, [role='alert']"))
        )
        assert "Неверный номер карты" in error_message.text
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_cyrillic_input(browser):
    """Ввод кириллицы в сумму резерва"""
    browser.get("http://localhost:8000/?reserved=восемьдесят")
    
    try:
        reserved_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Резерв:')]"))
        )
        assert "NaN" not in reserved_element.text
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_currency_selection(browser, app_url):
    """Проверка функционала выбора валюты"""
    browser.get(app_url)
    
    try:
        dollar_tab = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Доллары')]"))
        )
        dollar_tab.click()
        
        amount_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[name='amount']"))
        )
        amount_input.send_keys("50")
        
        submit_button = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], [data-testid='submit']"))
        )
        submit_button.click()
        
        success_message = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-message, [data-testid='success']"))
        )
        assert "$" in success_message.text
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")
        