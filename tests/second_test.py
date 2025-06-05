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
    amount_input = page.locator("input").nth(1)
    amount_input.fill(amount)
    return amount_input


def test_reserved_input_validation(page: Page, app_url: str):
    page.goto(app_url.replace("reserved=20001", "reserved=-20081"))
    reserved_text = page.locator("#rub-reserved").inner_text()
    assert "-" not in reserved_text


def test_reserved_string_input(page: Page, app_url: str):
    page.goto(app_url.replace("reserved=20001", "reserved=sdfkkij"))
    reserved_text = page.locator("#rub-reserved").inner_text()
    assert "NaN" not in reserved_text


def test_reserve_exceeds_balance(page: Page, app_url: str):
    page.goto(app_url.replace("balance=30000&reserved=20001", "balance=30008&reserved=1000000"))
    balance = int(page.locator("#rub-sum").inner_text().replace("'", ""))
    reserved = int(page.locator("#rub-reserved").inner_text().replace("'", ""))
    assert reserved <= balance


def test_transfer_amount_validation(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    amount_input = fill_amount(page, "abcd")
    assert amount_input.input_value() == ""


def test_commission_calculation(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    fill_amount(page, "103")
    commission = page.locator("#comission").inner_text()
    assert "10" in commission

