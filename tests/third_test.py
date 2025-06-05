from playwright.sync_api import Page


def open_rubles(page: Page, url: str) -> None:
    page.goto(url)
    page.get_by_text("Рубли").click()


def fill_card(page: Page, number: str):
    card = page.locator("input[placeholder='0000 0000 0000 0000']")
    card.fill(number)
    page.wait_for_timeout(100)
    return card


def fill_amount(page: Page, amount: str):
    amt = page.locator("input").nth(1)
    amt.fill(amount)
    return amt


def test_negative_balance(page: Page):
    page.goto("http://localhost:8000/?balance=-38000")
    balance = page.locator("#rub-sum").inner_text()
    assert "-" not in balance


def test_commission_for_100(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    fill_amount(page, "100")
    commission = page.locator("#comission").inner_text()
    assert "10" in commission


def test_invalid_card_number(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1111 1111 1111 1111")
    page.get_by_role("button", name="Перевести").click()
    error = page.locator(".error-message")
    error.wait_for()
    assert "Неверный номер карты" in error.inner_text()


def test_cyrillic_input(page: Page):
    page.goto("http://localhost:8000/?reserved=восемьдесят")
    reserved = page.locator("#rub-reserved").inner_text()
    assert "NaN" not in reserved


def test_currency_selection(page: Page, app_url: str):
    page.goto(app_url)
    page.get_by_text("Доллары").click()
    fill_card(page, "1234 5678 9012 3456")
    fill_amount(page, "50")
    page.get_by_role("button", name="Перевести").click()
    success = page.locator(".success-message")
    success.wait_for()
    assert "$" in success.inner_text()

