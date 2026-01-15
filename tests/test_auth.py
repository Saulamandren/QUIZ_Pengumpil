import os, time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def make_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver():
    d = make_driver()
    yield d
    d.quit()


# ==========================
# LOGIN TEST CASE (FT_001)
# ==========================
def test_login_valid(driver):
    driver.get(f"{BASE_URL}/login.php")

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()

    assert "login" not in driver.current_url.lower()


# ==========================
# REGISTER TEST CASE (FT_010)
# ==========================
def test_register_valid(driver):
    driver.get(f"{BASE_URL}/register.php")

    username = f"user_{int(time.time())}"

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.TAG_NAME, "button").click()

    assert "register" not in driver.current_url.lower()


# ==========================
# REGISTER FIELD NAME KOSONG (FT_012)
# ==========================
def test_register_empty_name(driver):
    driver.get(f"{BASE_URL}/register.php")

    username = f"user_noname_{int(time.time())}"

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.TAG_NAME, "button").click()

    assert "Fatal error" not in driver.page_source
