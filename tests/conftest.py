import os
import pytest
import subprocess
import time
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def server():
    # start simple HTTP server serving ./dist
    proc = subprocess.Popen(
        ["python", "-m", "http.server", "8000", "--directory", "dist"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)  # give server time to start
    yield "http://localhost:8000"
    proc.terminate()
    proc.wait()


@pytest.fixture(scope="function")
def page(server):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()

@pytest.fixture
def app_url(server):
    return f"{server}/?balance=30000&reserved=20001"
