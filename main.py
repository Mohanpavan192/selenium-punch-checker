import pickle
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ChromeDriver path
chrome_driver_path = r"C:\Users\Lenovo\chromedriver\chromedriver.exe"
cookie_file = "cookies.pkl"


#remove pkl file at strt

if os.path.exists(cookie_file):
    os.remove(cookie_file)
    print("🧹 Cookie file removed.")
else:
    print(⚠️ Cookie file not found.")
# Setup Chrome options
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Start WebDriver
driver = webdriver.Chrome(service=service, options=options)
TELEGRAM_BOT_TOKEN = "7900029498:AAHjAVehomvxk6P1IjFUOfvgtKeCAwYoM2Y"
CHAT_ID = "802742951"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)
def save_cookies(driver, path):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, path, url):
    driver.get(url)
    with open(path, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()

def is_session_alive():
    try:
        
       # wait = WebDriverWait(driver, 20)
      
        punch_element = wait.until(
              EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Punch In-Out')]/following-sibling::*"))
    )      
        print(f"✅ Punch In/Out Value: {punch_element.text.strip()}")
        return True
    except TimeoutException:
        return False

# Main logic
url = "https://peoplefirst.ril.com/v2/#/home"
start_time = datetime.now()

try:
    try:
        load_cookies(driver, cookie_file, url)
    except FileNotFoundError:
        print("🔑 No cookies found. Please log in manually and cookies will be saved.")
        driver.get(url)
        wait = WebDriverWait(driver, 60)
        try:
              punch_element = wait.until(
              EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Punch In-Out')]/following-sibling::*"))
    )
              punch_value = punch_element.text.strip()

             
        except Exception as e:
           
            print(f"❌ Error: {e}")
            sys.exit()

        save_cookies(driver, cookie_file)
        print("✅ Cookies saved.")

    print("🚀 Session tracking started...\n")
    send_telegram_message("🚀 Session tracking started...")
    while True:
        if is_session_alive():
            print("🔄 Refreshing session in 1 minute...\n")
            send_telegram_message("🔄 Refreshing session in 1 minute...\n")
            time.sleep(60)
            driver.refresh()
        else:
            session_duration = datetime.now() - start_time
            print(f"❌ Session expired after {session_duration}.")
            send_telegram_message(f"❌ Session expired after {session_duration}.")
            break

except Exception as e:
    print(f"❌ Unexpected Error: {e}")

finally:
    driver.quit()
