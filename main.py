from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://koshelek.ru/authorization/signup")


def extract_shadow_elements():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="remoteComponent"]'))
    )
    shadow_host = driver.find_element(By.XPATH, '//div[@class="remoteComponent"]')
    email_input = driver.execute_script("return arguments[0].shadowRoot.querySelector('input[name=\"username\"]')", shadow_host)
    new_password_input = driver.execute_script("return arguments[0].shadowRoot.querySelector('input[name=\"new-password\"]')", shadow_host)
    user_name = driver.execute_script("return arguments[0].shadowRoot.querySelector('input#input-129')", shadow_host)  
    checkbox = driver.execute_script("return arguments[0].shadowRoot.querySelector('input[role=\"checkbox\"]')", shadow_host)
    submit_button = driver.execute_script("return arguments[0].shadowRoot.querySelector('button[type=\"submit\"]')", shadow_host)
    return user_name, email_input, new_password_input, checkbox, submit_button


def clear_and_fill(element, value):
    driver.execute_script("arguments[0].value = '';", element)
    element.send_keys(value)


def register(user_name_value="", email_value="", password_value=""):
    user_name, email_input, new_password_input, checkbox, submit_button = extract_shadow_elements()
    WebDriverWait(driver, 50).until(
        EC.visibility_of(user_name)
    )
    clear_and_fill(user_name, user_name_value)
    clear_and_fill(email_input, email_value)
    clear_and_fill(new_password_input, password_value)  
    checkbox.click()  
    submit_button.click()


def wait_for_shadow_element_with_text(driver, shadow_host, expected_text):
    try:
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("""
                const shadowRoot = arguments[0].shadowRoot;
                if (!shadowRoot) return false;
                const matchingElement = Array.from(shadowRoot.querySelectorAll('*')).find(el => el.textContent.trim() === arguments[1]);
                return matchingElement !== undefined;
            """, shadow_host, expected_text)
        )
        print("Элемент с нужным текстом найден:", expected_text)
    except TimeoutException:
        print("Не удалось найти элемент с текстом:", expected_text)


# первый тест
register("testtest1", "test", "Qwerty123!")
wait_for_shadow_element_with_text(driver, driver.find_element(By.XPATH, '//div[@class="remoteComponent"]'), "Формат e-mail: username@test.ru")
driver.refresh()

# второй тест
register("testtest1", "lexakif281@opposir.com", "123")
wait_for_shadow_element_with_text(driver, driver.find_element(By.XPATH, '//div[@class="remoteComponent"]'), "Пароль должен содержать минимум 8 символов")
driver.refresh()


driver.quit()
