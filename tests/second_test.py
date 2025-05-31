from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

def test_reserved_input_validation(browser, app_url):
    """Ввод некорректных значений в резерв счета"""
    browser.get(app_url.replace("reserved=20001", "reserved=-20081"))
    
    try:
        reserved_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Резерв:')]"))
        )
        assert "-" not in reserved_element.text
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_reserved_string_input(browser, app_url):
    """Ввод строковых значений в резерв"""
    browser.get(app_url.replace("reserved=20001", "reserved=sdfkkij"))
    
    try:
        reserved_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Резерв:')]"))
        )
        assert "NaN" not in reserved_element.text
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_reserve_exceeds_balance(browser, app_url):
    """Проверка что сумма резерва не больше суммы на счету"""
    browser.get(app_url.replace("balance=30000&reserved=20001", "balance=30008&reserved=1000000"))
    
    try:
        balance_text = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'На счету:')]"))
        ).text
        reserved_text = browser.find_element(By.XPATH, "//*[contains(text(), 'Резерв:')]").text
        
        balance_amount = int(''.join(filter(str.isdigit, balance_text.split(":")[1])))
        reserved_amount = int(''.join(filter(str.isdigit, reserved_text.split(":")[1])))
        
        assert reserved_amount <= balance_amount
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_transfer_amount_validation(browser, app_url):
    """Тестирование валидации суммы перевода"""
    browser.get(app_url)
    
    try:
        amount_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[name='amount']"))
        )
        amount_input.send_keys("abcd")
        assert amount_input.get_attribute("value") == ""
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

def test_commission_calculation(browser, app_url):
    """Тестирование округления комиссии"""
    browser.get(app_url)
    
    try:
        amount_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number'], input[name='amount']"))
        )
        amount_input.send_keys("103")
        
        commission_element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".commission, [data-testid='commission']"))
        )
        assert "10" in commission_element.text
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")