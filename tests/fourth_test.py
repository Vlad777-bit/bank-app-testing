from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

def test_short_card_number(browser, app_url):
    """Валидация короткого номера карты"""
    browser.get(app_url)
    
    try:
        card_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][placeholder*='карты'], input[name='card']"))
        )
        card_input.send_keys("1234 5678 9012 34")
        
        submit_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit'], [data-testid='submit']"))
        )
        assert submit_button.is_enabled() is False
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_negative_transfer(browser, app_url):
    """Проверка отрицательного перевода"""
    browser.get(app_url)
    
    try:
        amount_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[name='amount']"))
        )
        amount_input.clear()
        amount_input.send_keys("-8080")
        
        submit_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit'], [data-testid='submit']"))
        )
        assert submit_button.is_enabled() is False
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_small_amount_commission(browser, app_url):
    """Тестирование комиссии для малой суммы"""
    browser.get(app_url)
    
    try:
        amount_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[name='amount']"))
        )
        amount_input.send_keys("10")
        
        commission_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".commission, [data-testid='commission']"))
        )
        assert commission_element.text != "0"
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_transfer_amount_input_validation(browser, app_url):
    """Тестирование ввода букв в сумму перевода"""
    browser.get(app_url)
    
    try:
        amount_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[name='amount']"))
        )
        amount_input.send_keys("abc")
        assert amount_input.get_attribute("value") == ""
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_large_number_input(browser, app_url):
    """Тестирование ввода большого числа"""
    browser.get(app_url)
    
    try:
        amount_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[name='amount']"))
        )
        amount_input.send_keys("80000000000000000000")
        value = amount_input.get_attribute("value")
        assert len(value) < 20 and value != "80000000000000000000"
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")