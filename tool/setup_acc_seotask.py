import concurrent.futures
import os
import threading
import random
import time
import string
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from extension import proxies
import os, shutil, time, requests, random,json
from datetime import datetime


def ghi_vao_file(ten_file, du_lieu):
    if not os.path.exists(ten_file):
        with open(ten_file, "w") as file:
            file.write(du_lieu)
    else: 
        with open(ten_file, "a") as file:
            file.write(du_lieu)

def get_data():
    file_path = os.path.join(os.getcwd() + "\\data", "mail.txt")
    with open(file_path, "r+") as file:
        # Đọc tất cả các dòng trong file
        data = file.readlines()

        # Lấy dữ liệu từ dòng đầu tiên
        data_first_line = data.pop(0)

        # Ghi lại các dòng còn lại vào file
        file.seek(0)
        file.writelines(data)
        file.truncate()

        # Trả về dữ liệu từ dòng đầu tiên
        return data_first_line.strip()

def get_messages(email, password):
    url = "https://tools.dongvanfb.net/api/get_messages"
    params = {
        "mail": email,
        "pass": password
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "messages" in data:
        # Extract the verification code from the third message
        message_content = str(data["messages"][0])
        print(message_content)
        return message_content.split('border-radius: 10px;\\n           padding: 11px 24px 9px 24px;\\n      ">')[1].split('</span>')[0]
    else:
        return None

def get_pin_seo_task(email, password):
    time.sleep(10)
    url = "https://tools.dongvanfb.net/api/get_messages"
    params = {
        "mail": email,
        "pass": password
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "messages" in data:
        # Extract the verification code from the third message
        message_content = str(data["messages"][0])
        return message_content.split('Код:</b> ')[1].split('<br><br>')[0]
    else:
        return None

def get_messages_seo_task(email, password):
    url = "https://tools.dongvanfb.net/api/get_messages"
    params = {
        "mail": email,
        "pass": password
    }
    response = requests.get(url, params=params,timeout=30)
    data = response.json()
    # Check if the response contains messages
    if  data["status"] == False:
        return data["content"]
    else :
        if "messages" in data:
            # Extract the verification code from the third message
            message_content = str(data["messages"][0])
            return message_content.split('https://seo-task.com/active?code=')[1].split('\"')[0]
        else:
            return None

def reg_payup(driver,email,pass_mail,proxy):
    driver.execute_script("window.open('');")
    time.sleep(2)
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    driver.get("https://payeer.com/en/auth/?register=yes")
    time.sleep(4)
    ip_proxy, port_proxy,user_proxy, pass_proxy = proxy.split(":")
    input_element = driver.find_element(By.XPATH, '//input[@name="email"]')
    input_element.click()
    for char in email:
        input_element.send_keys(char)
        time.sleep(0.25)
    if len(driver.find_elements(By.TAG_NAME, "iframe")) != 0 :
        if len(driver.find_elements(By.TAG_NAME, "iframe")) != 0 :
            site_key = driver.find_element(By.TAG_NAME, "iframe").get_attribute("src").split("0x")[1].split("/")[0]
            proxy = {
                "http": f"http://{user_proxy}:{pass_proxy}@{ip_proxy}:{port_proxy}",
            }
            url = "http://api.cap.guru/in.php"
            payload = {
                "key": "3239dd0885ef73d7249e20bfc6cb63dc",
                "method": "turnstile",
                "sitekey": f"0x{site_key}",
                "pageurl": driver.current_url,
                "json": 1
            }
            response = requests.post(url, json=payload, proxies=proxy)
            result = response.json()
            id_captcha = result['request']
            print(result)
            check_bypass = 0
            while(True):
                url = "http://api.cap.guru/res.php"
                payload = {
                    "key": "3239dd0885ef73d7249e20bfc6cb63dc",
                    "action": "get",
                    "id": f"{id_captcha}",
                    "json": 1
                }
                response = requests.post(url, json=payload, proxies=proxy)
                result = response.json()
                print(result)
                if result['status'] == 1:
                    g_recaptcha_response = result['request']
                    print(":Giai thanh cong captcha v2")
                    break
                else :
                    if check_bypass == 15:
                        print(":Khong the giai captcha v2")
                        break
                    time.sleep(10)
                    check_bypass =  check_bypass + 1
    driver.find_element(By.XPATH, "//button[contains(text(), 'Create Account')]").click()
    
    driver.execute_script("document.getElementsByName(`g-recaptcha-response`)[0].value = arguments[0];", g_recaptcha_response)
    
    check = 0
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email'].error"))
        )
        print("Tai Khoan Duoc Tao")
        time.sleep(5)
        driver.close()
        user_payeer,pass_payeer,Secret_сode = "","",""
    except TimeoutException :
            time.sleep(8)
            code = get_messages(email, pass_mail)
            input_element = driver.find_element(By.XPATH, '//input[@name="code"]')
            input_element.click()
            print(code)
            for char in code:
                input_element.send_keys(char)
                time.sleep(0.25)
            time.sleep(5)
            button_element = driver.find_element(By.XPATH, "//button[@class='login-form__login-btn step2']")
            button_element.click()
            time.sleep(7)
            input_element_1 = driver.find_element(By.XPATH, '//input[@name="new_password"]')
            pass_payeer = input_element_1.get_attribute("value")
            print("Giá trị của new_password:", pass_payeer)
            # Tìm phần tử input thứ hai
            input_element_2 = driver.find_element(By.XPATH, '//input[@name="secret_word"]')
            Secret_сode = input_element_2.get_attribute("value")
            print("Giá trị của secret_word:", Secret_сode)
            input_element_3 = driver.find_element(By.XPATH, '//input[@name="nick"]')
            user_payeer = input_element_3.get_attribute("value")
            print("Giá trị của nick:", user_payeer)
            next_button = driver.find_element(By.CSS_SELECTOR, 'button.login-form__login-btn.mini-mid-btn')
            next_button.click()
            time.sleep(4)
            url = "https://api.name-fake.com/english-united-states/female"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            name_div = soup.find("div", class_="subj_div_45g45gg", id="copy1")
            name_payeer = name_div.text
            last_name_div = soup.find("div", class_="subj_div_45g45gg", id="copy2")
            last_name_payeer = name_div.text
            name_input = driver.find_element(By.NAME, "name")
            name_input.send_keys(name_payeer)
            last_name_input = driver.find_element(By.NAME, "last_name")
            last_name_input.send_keys(last_name_payeer)
            done_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="login-form__login-btn mini-mid-btn" and not(@disabled)]'))
            )
            done_button.click()
            time.sleep(10)
            data_acc_payeer = driver.find_elements(By.CLASS_NAME, 'info-security__data')
            if len(data_acc_payeer) != 0:
                key_master = data_acc_payeer[3].text
            time.sleep(5)
    driver.close()
    driver.switch_to.window(windows[0])
    return user_payeer,pass_payeer,Secret_сode,key_master

def login(api_key1):
    # Cấu hình ChromeOptions và DesiredCapabilities
    chrome_options = Options()
    profile_path = os.getcwd() + '/chrome'
    #create_or_load_profile(profile_path)
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-2d-canvas")
    chrome_options.add_argument("--disable-prompt-on-repost")
    chrome_options.add_argument("--disable-webgl-image-chromium")
    chrome_options.add_argument("--disable-webrtc")
    chrome_options.add_argument("--disable-audio-api")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--no-service-autorun')
    chrome_options.add_argument('--password-store-basic')
    chrome_options.add_argument('--no-service-autorun')
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-cpu') 
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "download_restrictions": 3
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--enable-main-frame-before-activation')
    chrome_options.add_argument('--display-capture-permissions-policy-allowed')
    chrome_options.add_argument('--device-scale-factor=1')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-plugins-discovery')
    chrome_options.add_argument('--disable-gpu-shader-disk-cache')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-page-load-check')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--force-device-scale-factor=0.25")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    thorium_binary_path = "C:\\Users\\ghost\\AppData\\Local\\Thorium\\Application\\thorium.exe"
    chrome_options.binary_location = thorium_binary_path
    browser_version = "120.0.6099.110"
    chrome_options.add_argument(f"--version={browser_version}")
    chrome_options.add_argument("--name=Chrome")
    acc = get_data()
    if len(acc.split("|")) == 2 :
        mail , pass_mail  = acc.split("|")
        proxy = ""
        user_payeer = ""
        pass_payeer = ""
        Secret_сode = ""
        key_master = ""
    elif len(acc.split("|")) == 9 :
        mail , pass_mail , proxy , user_payeer , pass_payeer , Secret_сode, key_master ,  mail_payeer , pass_payeer  = acc.split("|")
        if proxy != "":
            if len(proxy.split(":")) == 4 :
                ip_proxy, port_proxy,user_proxy, pass_proxy = proxy.split(":")
            else:
                user_proxy = ""
                pass_proxy = ""
                ip_proxy, port_proxy = proxy.split(":")
            proxies_extension = proxies(user_proxy, pass_proxy.split("\n")[0], ip_proxy, port_proxy)
            time.sleep(2)
            chrome_options.add_extension(os.getcwd()+f"\\{ip_proxy}_{port_proxy}\\proxies_extension.zip")
    elif len(acc.split("|")) >= 6 :
        mail , pass_mail , proxy , user_payeer , pass_payeer , Secret_сode , key_master  = acc.split("|")
        if proxy != "":
            if len(proxy.split(":")) == 4 :
                ip_proxy, port_proxy,user_proxy, pass_proxy = proxy.split(":")
            else:
                user_proxy = ""
                pass_proxy = ""
                ip_proxy, port_proxy = proxy.split(":")
            proxies_extension = proxies(user_proxy, pass_proxy.split("\n")[0], ip_proxy, port_proxy)
            time.sleep(2)
            chrome_options.add_extension(os.getcwd()+f"\\{ip_proxy}_{port_proxy}\\proxies_extension.zip")
    elif len(acc.split("|")) == 3 :
        mail , pass_mail , proxy = acc.split("|")
        user_payeer = ""
        pass_payeer = ""
        Secret_сode = ""
        key_master = ""
        if proxy != "":
            if len(proxy.split(":")) == 4 :
                ip_proxy, port_proxy,user_proxy, pass_proxy = proxy.split(":")
            else:
                user_proxy = ""
                pass_proxy = ""
                ip_proxy, port_proxy = proxy.split(":")
            proxies_extension = proxies(user_proxy, pass_proxy.split("\n")[0], ip_proxy, port_proxy)
            time.sleep(2)
            chrome_options.add_extension(os.getcwd()+f"\\{ip_proxy}_{port_proxy}\\proxies_extension.zip")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://kiemtraip.com/raw.php")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    ip_address = soup.body.get_text()
    driver.get("https://payeer.com/")
    time.sleep(10000)
    driver.get("https://seo-task.com/login")
    time.sleep(5)
    print("["+mail+"]:"+ip_address)
    try:
    # Lấy giá trị của thuộc tính 'src' của phần tử iframe
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe_src = iframe.get_attribute("src")
        site_key = iframe_src.split("https://google.com/recaptcha/api2/anchor?ar=1&k=")[1].split("&co=")[0]
        url = "http://api.cap.guru/in.php"
        payload = {
            "key": api_key1,
            "method": "userrecaptcha",
            "googlekey": f"{site_key}",
            "pageurl": "https://seo-task.com/login",
            "json": 1
        }
        response = requests.post(url, json=payload)
        result = response.json()
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="login"]'))
        )
        input_element.click()
        for char in mail:
            input_element.send_keys(char)
            time.sleep(0.25)      
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
        )
        input_element.click()
        for char in pass_mail:
            input_element.send_keys(char)
            time.sleep(0.25)
        check_bypass = 0
        id_captcha = result['request']
        while(True):
            url = "http://api.cap.guru/res.php"
            payload = {
                "key": api_key1,
                "action": "get",
                "id": f"{id_captcha}",
                "json": 1
            }
            # Отправка POST-запроса
            response = requests.post(url, json=payload)
            # Печать ответа от сервера
            result = response.json()
            if result['status'] == 1:
                g_recaptcha_response = result['request']
                print("["+mail+"]:Giai thanh cong captcha v2")
                break
            else :
                if check_bypass == 15:
                    print("["+mail+"]:Khong the giai captcha v2")
                    break
                time.sleep(10)
                check_bypass =  check_bypass + 1
        driver.execute_script("document.getElementsByClassName(`g-recaptcha-response`)[0].innerHTML = " f"'{g_recaptcha_response}';")
        driver.find_elements(By.XPATH, '//button[@class="button f-spinner"]')[0].click()
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.footer-error'))
            )
        if element:
            error_text = element.text.split("\n")[0]
            if  error_text == "Данный Логин или E-mail не зарегистрирован на проекте":
                print("["+mail+"]:Email khong ton tai")
                register(driver,mail,pass_mail,api_key1,api_key2)
    except:
        print("Không tìm thấy phần tử sau 10 giây.")
    return driver,mail , pass_mail , proxy , user_payeer,pass_payeer, Secret_сode,key_master

def register(driver,mail,pass_mail,api_key1,api_key2):
    driver.get("https://seo-task.com/register")
    time.sleep(5)
    try:
    # Lấy giá trị của thuộc tính 'src' của phần tử iframe
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        iframe_src = iframe.get_attribute("src")
        site_key = iframe_src.split("https://google.com/recaptcha/api2/anchor?ar=1&k=")[1].split("&co=")[0]
        input_element =driver.find_element(By.XPATH, '//input[@name="login"]')
        time.sleep(1)
        url = "http://api.cap.guru/in.php"
        payload = {
            "key": api_key1,
            "method": "userrecaptcha",
            "googlekey": f"{site_key}",
            "pageurl": "https://seo-task.com/register",
            "json": 1
        }
        response = requests.post(url, json=payload)
        result = response.json()
        input_element.click()
        url = "https://api.name-fake.com/english-united-states/female"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        name_div = soup.find("div", class_="subj_div_45g45gg", id="copy3")
        login = name_div.text
        if len(login) > 15:
            login = login[:15]
        elif len(login) < 4:
            login = login.ljust(4, 'x')
        for char in login:
            input_element.send_keys(char)
            time.sleep(0.25)      
        input_element = driver.find_element(By.XPATH, '//input[@name="email"]')
        input_element.click()
        for char in mail:
            input_element.send_keys(char)
            time.sleep(0.25)
        input_element = driver.find_element(By.XPATH, '//input[@name="password"]')
        input_element.click()
        for char in pass_mail:
            input_element.send_keys(char)
            time.sleep(0.25)
        check_bypass = 0
        id_captcha = result['request']
        while(True):
            url = "http://api.cap.guru/res.php"
            payload = {
                "key": api_key1,
                "action": "get",
                "id": f"{id_captcha}",
                "json": 1
            }
            response = requests.post(url, json=payload)
            result = response.json()
            if result['status'] == 1:
                g_recaptcha_response = result['request']
                print("["+mail+"]:Giai thanh cong captcha v2")
                break
            elif result['request'] == 0:
                print("lỗi")
            else :
                if check_bypass == 15:
                    print("["+mail+"]:Khong the giai captcha v2")
                    break
                time.sleep(10)
                check_bypass =  check_bypass + 1
        driver.execute_script("document.getElementsByClassName(`g-recaptcha-response`)[0].innerHTML = " f"'{g_recaptcha_response}';")
        driver.find_elements(By.XPATH, '//button[@class="button f-spinner"]')[0].click()
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.footer-error'))
            )
        if element:
            error_text = element.text.split("\n")[0]
            print(error_text)
            if  error_text == "Данный Логин или E-mail не зарегистрирован на проекте":
                print("["+mail+"]:Email khong ton tai")
                register(driver,mail,pass_mail,api_key1,api_key2)
            elif error_text == "С Вашего IP адреса регистрация не доступна. Для более подробной информации обратитесь в службу технической поддержки (1)." :
                print("["+mail+"]:IP bị chặn")
        else :   
            messages = get_messages_seo_task(mail, pass_mail)
            if messages == "Invalid email or password or IMAP disabled":
                print("Invalid email or password or IMAP disabled")
                #unlock_hotmail(driver,mail,pass_mail,api_key2)
            elif messages is None:
                print("Khong co mail")
            elif messages:
                driver.execute_script("window.open('');")
                time.sleep(2)
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                driver.get(f"https://seo-task.com/active?code={messages}")
                time.sleep(10)
                driver.close()
                driver.switch_to.window(windows[0])
    except:
        print("Không tìm thấy phần tử sau 20 giây.")

def get_data_setting():
    file_path = os.getcwd() + "/data/data.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as new_file:
            default_data = {"api_key_sim24": "", "api_key_cap_guru": ""}
            json.dump(default_data, new_file)
    with open(file_path, "r") as json_file:
        loaded_data = json.load(json_file)
    if loaded_data["api_key_sim24"] == "":
        loaded_data["api_key_sim24"] = input("Nhập Api key sim24: ")
        with open(file_path, "w") as json_file:
            json.dump(loaded_data, json_file)
    if loaded_data["api_key_cap_guru"] == "":
        loaded_data["api_key_cap_guru"] = input("Nhập Api key cap.guru: ")
        with open(file_path, "w") as json_file:
            json.dump(loaded_data, json_file)
    api_key2 = loaded_data["api_key_sim24"]
    api_key1 = loaded_data["api_key_cap_guru"]
    return api_key1,api_key2

def check_acc(email,password):
    driver.get("https://seo-task.com/users_setup")
    while(True):
        time.sleep(5)
        if len(driver.find_elements(By.CLASS_NAME, 'button.button_grey.f-spinner')) == 4:
            driver.find_elements(By.CLASS_NAME, 'button.button_grey.f-spinner')[0].click()
            time.sleep(3)
            driver.find_elements(By.CLASS_NAME, 'button.button_green.f-spinner.f-spinner-go')[0].click()
            time.sleep(10)
            messages = get_messages_seo_task(email, password)
            print(messages)
            if messages:
                driver.execute_script("window.open('');")
                time.sleep(2)
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                driver.get(f"https://seo-task.com/active?code={messages}")
                time.sleep(10)
                driver.close()
                driver.switch_to.window(windows[0])
                break
            else:
                break
        else:
            break

def add_payeer(user_payeer,email,password,proxy,pass_payeer,Secret_сode,key_master):
    driver.get("https://seo-task.com/pay_out")
    time.sleep(2)
    name = driver.find_elements(By.XPATH, "//div[@class='balance_top']")[2].text.split(" ")[0]
    money = driver.find_element(By.XPATH, "//b[@class='balance_out']").text
    money_stop = float(money.split(" ")[0])
    if len(driver.find_elements(By.XPATH, "//div[@class='pay-cur pay-t-min ']")) != 0 :
        if driver.find_element(By.XPATH, "//div[@class='pay-cur pay-t-min ']").text =="Укажите кошелек" :
            print("Chua Them vi")
            if user_payeer == "":
                user_payeer,pass_payeer,Secret_сode,key_master = reg_payup(driver,mail,pass_mail,proxy)
                print(user_payeer,pass_payeer,Secret_сode)
            if user_payeer != "":
                print(user_payeer)
                driver.find_element(By.XPATH, "//div[@class='pay-in-button pay-in-payeer']").click()
                time.sleep(5)
                if len(driver.find_elements(By.ID, "form-pin")) != 0:
                    driver.find_element(By.ID, "form-pin").click()
                    time.sleep(5)
                input_element = driver.find_element(By.XPATH, "//input[@name='payeer']")
                input_element.send_keys(user_payeer)
                input_element = driver.find_element(By.XPATH, "//input[@class='pin_code']")
                time.sleep(5)
                code = get_pin_seo_task(email, password)
                print(code)
                input_element.send_keys(code)
                time.sleep(5)
                driver.find_element(By.CLASS_NAME, "button.button_grey.f-spinner.payeer_spin").click()
        data_done = mail+'|'+pass_mail+"|"+proxy+"|"+user_payeer+'|'+pass_payeer+'|'+Secret_сode+"|"+key_master+"\n"
        file_path = os.path.join(os.getcwd() + "\\data", "acc_run.txt")
        ghi_vao_file(file_path, data_done)
api_key1,api_key2 = get_data_setting()

driver,mail , pass_mail , proxy , user_payeer,pass_payeer,Secret_сode,key_master = login(api_key1)
check_acc(mail,pass_mail)
#add_payeer(user_payeer,mail , pass_mail, proxy ,pass_payeer,Secret_сode,key_master)


time.sleep(10000)










