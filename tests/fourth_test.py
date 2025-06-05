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


def test_short_card_number(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 34")
    submit = page.get_by_role("button", name="Перевести")
    assert not submit.is_enabled()


def test_negative_transfer(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    amt = fill_amount(page, "-8080")
    submit = page.get_by_role("button", name="Перевести")
    assert not submit.is_enabled()


def test_small_amount_commission(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    fill_amount(page, "10")
    commission = page.locator("#comission").inner_text()
    assert commission != "0"


def test_transfer_amount_input_validation(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    amount_input = fill_amount(page, "abc")
    assert amount_input.input_value() == ""


def test_large_number_input(page: Page, app_url: str):
    open_rubles(page, app_url)
    fill_card(page, "1234 5678 9012 3456")
    amount_input = fill_amount(page, "80000000000000000000")
    value = amount_input.input_value()
    assert len(value) < 20 and value != "80000000000000000000"

