import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Имя вашего HTML-файла
HTML_FILE = "zaitsev.html.html"  # 👈 замените на ваше имя файла
OUTPUT_DIR = "screenshots"

# Папка для скриншотов
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Настройка драйвера
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # без открытия окна браузера
options.add_argument("--window-size=1280,900")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Открываем локальный HTML
    url = f"file:///{os.path.abspath(HTML_FILE)}"
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Ждём появления вкладок
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tab-btn")))

    # Собираем идентификаторы вкладок
    tab_buttons = driver.find_elements(By.CLASS_NAME, "tab-btn")
    tab_ids = [btn.get_attribute("data-tab") for btn in tab_buttons]

    for tab_id in tab_ids:
        # Кликаем по вкладке
        btn = driver.find_element(By.CSS_SELECTOR, f'[data-tab="{tab_id}"]')
        btn.click()
        time.sleep(0.5)  # ждём анимацию fadeIn

        # Имя файла по названию вкладки
        filename = f"{OUTPUT_DIR}/{tab_id}.png"
        driver.save_screenshot(filename)
        print(f"✔ Сохранён скриншот вкладки «{tab_id}» -> {filename}")

finally:
    driver.quit()
    print("\nГотово! Все скриншоты лежат в папке screenshots/")