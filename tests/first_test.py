from playwright.sync_api import Page


def open_rubles(page: Page, url: str) -> None:
    page.goto(url)
    page.get_by_text("Рубли").click()


def fill_card(page: Page, number: str):
    card_input = page.locator("input[placeholder='0000 0000 0000 0000']")
    card_input.fill(number)
    page.wait_for_timeout(100)
    return card_input


def fill_amount(page: Page, amount: str):
    amount_input = page.locator("input").nth(1)
    amount_input.fill(amount)
    return amount_input


def test_card_number_validation(page: Page, app_url: str):
    """Ввод более 16 символов в поле номера карты"""
    open_rubles(page, app_url)
    card = fill_card(page, "9999 9999 9999 9999 9")
    value = card.input_value().replace(" ", "")
    assert len(value) <= 16


def test_balance_input_validation(page: Page, app_url: str):
    """Некорректное значение баланса не должно выводить NaN"""
    page.goto(app_url.replace("balance=30000", "balance=gdd"))
    balance_text = page.locator("#rub-sum").inner_text()
    assert "NaN" not in balance_text


def test_currency_switch(page: Page, app_url: str):
    """После перевода в рублях кнопка перевода в долларах недоступна"""
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    fill_amount(page, "22500")
    page.get_by_role("button", name="Перевести").click()
    page.get_by_text("Доллары").click()
    submit = page.get_by_role("button", name="Перевести")
    assert not submit.is_enabled()


def test_card_input_character_validation(page: Page, app_url: str):
    """Буквы в номере карты не принимаются"""
    open_rubles(page, app_url)
    card_input = fill_card(page, "abcd")
    assert card_input.input_value() == ""


def test_insufficient_funds(page: Page, app_url: str):
    """Перевод больше остатка вызывает сообщение об ошибке"""
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    fill_amount(page, "288000")
    page.get_by_role("button", name="Перевести").click()
    error = page.locator(".error-message")
    error.wait_for()
    assert "Недостаточно средств" in error.inner_text()

