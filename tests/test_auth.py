import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
SCREENSHOT_DIR = "tests/screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# ============================
# Setup Chrome Driver (CI SAFE)
# ============================
def setup_driver():
    options = Options()

    # WAJIB untuk GitHub Actions
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Chromedriver bawaan Linux CI
    service = Service("/usr/bin/chromedriver")

    return webdriver.Chrome(service=service, options=options)


def take_screenshot(driver, name):
    path = f"{SCREENSHOT_DIR}/{name}.png"
    driver.save_screenshot(path)


# ============================
# TEST LOGIN
# ============================

def test_login_empty():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/login.php")
    take_screenshot(driver, "login_empty_page")

    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "login_empty_result")
    driver.quit()


def test_login_only_username():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/login.php")

    driver.find_element(By.NAME, "username").send_keys("ra")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "login_only_username")
    driver.quit()


def test_login_wrong_password():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/login.php")

    driver.find_element(By.NAME, "username").send_keys("ra")
    driver.find_element(By.NAME, "password").send_keys("sembarang")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "login_wrong_password")
    driver.quit()


def test_login_short_password():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/login.php")

    driver.find_element(By.NAME, "username").send_keys("ra")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "login_short_password")
    driver.quit()


def test_login_sql_injection():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/login.php")

    driver.find_element(By.NAME, "username").send_keys("OR '1'='1")
    driver.find_element(By.NAME, "password").send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "login_sql_injection")
    driver.quit()


# ============================
# TEST REGISTER
# ============================

def test_register_empty():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/register.php")
    take_screenshot(driver, "register_empty_page")

    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "register_empty_result")
    driver.quit()


def test_register_existing_user():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/register.php")

    driver.find_element(By.NAME, "username").send_keys("ra")
    driver.find_element(By.NAME, "email").send_keys("ra@email.com")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "confirm_password").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "register_existing_user")
    driver.quit()


def test_register_invalid_email():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/register.php")

    driver.find_element(By.NAME, "username").send_keys("userbaru1")
    driver.find_element(By.NAME, "email").send_keys("emailtanpaat")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "confirm_password").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "register_invalid_email")
    driver.quit()


def test_register_password_not_match():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/register.php")

    driver.find_element(By.NAME, "username").send_keys("userbaru2")
    driver.find_element(By.NAME, "email").send_keys("user2@email.com")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "confirm_password").send_keys("654321")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "register_password_not_match")
    driver.quit()


def test_register_success():
    driver = setup_driver()
    driver.get(f"{BASE_URL}/register.php")

    driver.find_element(By.NAME, "username").send_keys("userbaru3")
    driver.find_element(By.NAME, "email").send_keys("user3@email.com")
    driver.find_element(By.NAME, "password").send_keys("123456")
    driver.find_element(By.NAME, "confirm_password").send_keys("123456")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)

    take_screenshot(driver, "register_success")
    driver.quit()
