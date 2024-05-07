
#hotmail|pass_hotmail|proxy|user_name|pass|payeer|pass_payeer|Secret_сode





import concurrent.futures
import os
import threading
import random
import time
import base64
import string , re
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

file_path = os.getcwd() + "/data/data.json"
def check_data_captcha(id):
    # Đường dẫn đến file JSON
    file_path = ".//images//captcha.json"
    
    try:
        # Đọc dữ liệu từ file JSON hiện có
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # Nếu file không tồn tại, trả về False
        return False

    if id in data :
        return data[id]
    else:
        return False

def add_data_captcha(id, password):
    # Đường dẫn đến file JSON
    file_path = ".//images//captcha.json"
    
    try:
        # Đọc dữ liệu từ file JSON hiện có
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # Nếu file không tồn tại, tạo một dictionary mới
        data = {}

    # Thêm id mới cùng với dữ liệu vào dictionary
    data[id] = password
        
    # Ghi dữ liệu mới vào file JSON
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
        

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
while(True):
    url = f"http://api.cap.guru/res.php?action=getbalance&key={api_key1}"
    response = requests.get(url)
    if float(response.text) > 0:
        print(response.text)
        break
    else:
        print("cap.guru het tien")
        exit()
def get_data():
    global stt_acc
    with lock:
        file_path = os.path.join(os.getcwd() + "\\data\\acc_seotask.txt")
        with open(file_path, "r") as file:
            data = file.readlines()
            if stt_acc < len(data):
                acc_data = data[stt_acc]
                stt_acc += 1
                return acc_data
            else:
                exit()
                
current_date = datetime.now().date()
if not os.path.exists(current_date.strftime("%Y-%m-%d") + "_history.txt"):
    with open(current_date.strftime("%Y-%m-%d") + "_history.txt", "x"):
        pass

def create_or_load_profile(profile_path):
    if not os.path.exists(profile_path):
        try:
            # Tạo mới profile nếu thư mục không tồn tại
            shutil.copytree("default_profile", profile_path)  # Thay "default_profile" bằng thư mục mẫu hoặc trống
            print("Created a new profile.")
        except FileNotFoundError:
            print("Thư mục mẫu 'default_profile' không tồn tại.")
    else:
        print("Using an existing profile.")

def get_messages_seo_task(email, password):
    url = "https://tools.dongvanfb.net/api/get_messages"
    params = {
        "mail": email,
        "pass": password
    }
    response = requests.get(url, params=params)
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

def get_messages_payeer(email, password):
    url = "https://tools.dongvanfb.net/api/get_messages"
    params = {
        "mail": email,
        "pass": password
    }
    response = requests.get(url, params=params)
    data = response.json()
    # Check if the response contains messages
    if "messages" in data:
        # Extract the verification code from the third message
        message_content = str(data["messages"][0])
        print(message_content)
        return message_content.split('border-radius: 10px;\\n           padding: 11px 24px 9px 24px;\\n      ">')[1].split('</span>')[0]
    else:
        return None

def sim24_phone(api_key2):
    url = f"https://sim24.cc/api?action=number&service=microsoft&apikey={api_key2}"
    response = requests.request("GET",url)
    return json.loads(response.text)['Result']['number'], json.loads(response.text)['Result']['id']

def sim24_code(id_phone):
    timer = 0
    while(True):
        url = f"https://sim24.cc/api?action=code&id={id_phone}&apikey=e4pzt06n9etef454jszymcvzpoworpi2"
        response = requests.request("GET",url)
        if json.loads(response.text)['ResponseCode'] == 0 : 
            return json.loads(response.text)['ResponseCode'] , json.loads(response.text)['Result']['otp']
            break
        elif json.loads(response.text)['ResponseCode'] == 1 :
            time.sleep(1)
            if timer == 180:
                return None , None
                break
        elif json.loads(response.text)['ResponseCode'] == 2 : 
            return None , None
            break

def unlock_hotmail(driver,email,pass_word,api_key2):
    driver.get("https://login.live.com/")
    time.sleep(5)
    input_element = driver.find_element(By.XPATH, '//input[@name="loginfmt"]')
    input_element.click()
    for char in email:
        input_element.send_keys(char)
        time.sleep(0.25)
    driver.find_element(By.XPATH, '//button[@id="idSIButton9"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="passwd"]')))
    input_element = driver.find_element(By.XPATH, '//input[@name="passwd"]')
    input_element.click()
    for char in pass_word:
        input_element.send_keys(char)
        time.sleep(0.25)
    driver.find_element(By.XPATH, '//button[@id="idSIButton9"]').click()
    while True:
        if len(driver.find_elements(By.XPATH, '//div[@id="interruptContainer"]')) != 0:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@id="id__0"]'))).click()
        time.sleep(2)
        if len(driver.find_elements(By.XPATH, '//div[@id="kmsiTitle"]')) != 0:
            break
            print(driver.find_elements(By.XPATH, '//div[@id="kmsiTitle"]')[0].text)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="acceptButton"]'))).click()
            time.sleep(10)
            if len(driver.find_elements(By.XPATH, '//div[@id="iPageTitle"]')) != 0:
                driver.find_elements(By.XPATH, '//div[@id="iPageTitle"]')[0].text
                input_element = driver.find_element(By.XPATH, '//input[@id="EmailAddress"]')
                input_element.click()
                response = requests.request("GET","https://api.dongvanfb.net/user/create_mail_domain?apikey=8da1f79743b7f1f84012ba573610ecd5&type=mailtm")
                email_reset = json.loads(response.text)['email']
                for char in email_reset:
                    input_element.send_keys(char)
                    time.sleep(0.25)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="iNext"]'))).click()
                time.sleep(3)
                input_element = driver.find_element(By.XPATH, '//input[@id="iOttText"]')
                
                response = requests.request(f"GET","https://api.dongvanfb.net/user/get_code_mail_domain?apikey=8da1f79743b7f1f84012ba573610ecd5&email={email_reset}")
                code_mail = json.loads(response.text)['code']
                input_element.click()
                for char in code_mail:
                    input_element.send_keys(char)
                    time.sleep(0.25)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="iNext"]'))).click()
            time.sleep(2)
            driver.get("https://outlook.live.com/")
            time.sleep(3)
            driver.get("https://outlook.live.com/mail/0/options/mail/layout")
            time.sleep(3)
            driver.find_element(By.XPATH, '//button[text()="Sync email"]').click()
            time.sleep(10)
            action = ActionChains(driver)
            radio_button = driver.find_elements(By.CLASS_NAME, "fui-Radio__indicator.rwtekvw")[1]
            action.click(radio_button).perform()
            action.reset_actions()
            time.sleep(5)
            action.click(driver.find_element(By.XPATH, '//button[text()="Save"]')).perform()
            action.reset_actions()
            break
        elif len(driver.find_elements(By.XPATH, '//div[@id="StartHeader"]')) != 0:
            driver.find_element(By.XPATH, '//div[@id="StartHeader"]').text
            if driver.find_element(By.XPATH, '//div[@id="StartHeader"]').text == "Your account has been locked":
                driver.find_element(By.XPATH, '//input[@id="StartAction"]').click()
            time.sleep(5)
            select_element = driver.find_element(By.XPATH, "//select[@aria-label='Country code']")
            dropdown = Select(select_element)
            dropdown.select_by_value('VN')
            driver.find_element(By.XPATH, "//select[@aria-label='Country code']").click()
            time.sleep(2)
            driver.find_elements(By.CLASS_NAME, "form-control.input-max-width")[1].click()
            time.sleep(2)
            error_phone = 0
            while True:
                driver.find_elements(By.CLASS_NAME, "form-control.input-max-width")[1].click()
                time.sleep(2)
                input_element = driver.find_element(By.CLASS_NAME, 'form-control.input-max-width.c_nobdr')
                error_code = 0
                phone, id_phone = sim24_phone(api_key2)
                input_element.clear()
                for char in phone:
                    input_element.send_keys(char)
                    time.sleep(0.25)
                element = driver.find_element(By.XPATH, '//a[@title="Send code"]')
                element.click()
                time.sleep(5)
                alert_elements = driver.find_elements(By.XPATH, '//div[@class="alert alert-error"]')
                for element in alert_elements:
                    style = element.get_attribute('style')
                    if "text-align: left; display: inline;" in style:
                        print("Alert text:", element.text)
                        error_code = 1
                        error_phone += 1 
                if error_phone == 5:
                    data_error = email + "|" + pass_word + "\n"
                    file_error = os.path.join(os.getcwd() + "\\data", "unlock_done.txt")
                    break
                if error_code == 0:
                    error_phone = 0
                    break
            if error_phone == 0:
                code_phone = sim24_code(id_phone)
                input_element = driver.find_elements(By.CLASS_NAME, "form-control.input-max-width")[2].click()
                time.sleep(2)
                input_element = driver.find_element(By.CLASS_NAME, 'form-control.input-max-width.c_nobdr')
                for char in code_phone:
                    input_element.send_keys(char)
                    time.sleep(0.25)
                driver.find_element(By.ID, "ProofAction").click()
                time.sleep(5)
                driver.find_element(By.XPATH, '//input[@id="finishHeader"]').text
                break
    file_done = os.path.join(os.getcwd() + "\\data", "unlock_done.txt")
    data_done = email + "|" + pass_word + "\n"
    time.sleep(10)

def reg_payup(driver,proxy,email,pass_mail):
    driver.get("https://payeer.com/en/auth/?register=yes")
    time.sleep(4)
    input_element = driver.find_element(By.XPATH, '//input[@name="email"]')
    input_element.click()
    for char in email:
        input_element.send_keys(char)
        time.sleep(0.25)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Create Account')]").click()
    time.sleep(1)
    check = 0
    try:
        # Chờ cho phần tử input có tên "email" và có class "error" xuất hiện trong vòng 10 giây
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email'].error"))
        )
        print("Tai Khoan Duoc Tao")
        time.sleep(5)
        driver.close()
        return None
    except TimeoutException :
        if len(driver.find_elements(By.XPATH, "//iframe[@id='cf-chl-widget-lb0zp']")) != 0:
            print("Dinh captcha chưa biet cach giai")
            time.sleep(5)
            driver.close()
            return None
        else :
            time.sleep(5)
            #code = get_messages(email, pass_mail)
            code = input("code:")
            input_element = driver.find_element(By.XPATH, '//input[@name="code"]')
            input_element.click()
            for char in code:
                input_element.send_keys(char)
                time.sleep(0.25)
            time.sleep(2)
            button_element = driver.find_element(By.XPATH, "//button[@class='login-form__login-btn step2']")
            button_element.click()
            time.sleep(5)
            input_element_1 = driver.find_element(By.XPATH, '//input[@name="new_password"]')
            value_1 = input_element_1.get_attribute("value")
            #print("Giá trị của new_password:", value_1)
            # Tìm phần tử input thứ hai
            input_element_2 = driver.find_element(By.XPATH, '//input[@name="secret_word"]')
            value_2 = input_element_2.get_attribute("value")
            #print("Giá trị của secret_word:", value_2)
            input_element_3 = driver.find_element(By.XPATH, '//input[@name="nick"]')
            value_3 = input_element_3.get_attribute("value")
            #print("Giá trị của nick:", value_3)
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
            # Click vào nút "Done"
            done_button.click()
            data_done = email+'|'+pass_mail+"|"+proxy+"|"+value_3+'|'+value_1+'|'+value_2
            file_path = os.path.join(os.getcwd() + "\\data", "test.txt")
            time.sleep(5)
            driver.close()
            return value_3

def check_captcha(driver,name):
    captcha_text_check = 0
    while (True):  
        if captcha_text_check == 15:
            return False
        if len(driver.find_elements(By.CLASS_NAME,"block_captcha")) != 0 :
            print(f"[{name}]:Dinh captcha text")
            time.sleep(5)
            img_element  = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH,"//div[@class='captcha_img']/img"))
            )
            img_url = img_element.get_attribute("src")
            os.makedirs(os.getcwd() + "\\images", exist_ok=True)
            id = img_url.split("=")[-1]
            file_name = os.path.join(os.getcwd() + "\\images", f"{id}.png")
            img_element.screenshot(file_name)   
            text = captcha_text(id,name)
            if text == None:
                text = str(random.randint(10000, 99999)) 
            input_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@ID="go_code"]'))
                )
            input_element.click()
            input_element.clear()
            for char in text:
                input_element.send_keys(char)
                time.sleep(0.25)      
            driver.find_element(By.CLASS_NAME, "load_butt_pop").click()
            time.sleep(10)
            captcha_text_check = +1
        else :
            break

def captcha_text(id,name):
    while(True):
        print(f"[{name}]:Giai captcha bang google")
        extracted_data = None  # Khởi tạo extracted_data để đảm bảo rằng biến này được xác định dù không có kết quả từ regex
        image_path = os.getcwd() + f'\\images\\{id}.png'
        endpoint_url = 'https://lens.google.com/v3/upload'
        # Read the image file as binary data
        with open(image_path, 'rb') as file:
            image_data = file.read()
        files = {'encoded_image': ('image.jpg', image_data, 'image/jpeg')}
        response = requests.post(endpoint_url, files=files, timeout=10)
        regex_pattern = r'",\[\[(\[.*?\])\]'
        match = re.search(regex_pattern, response.text)
        print(match)
        if match:
            if '$' in match.group(1):  # Thay đổi cách kiểm tra ký tự "$"
                    # Thay thế ký tự "$" bằng "5"
                extracted_data = match.group(1).replace("$", "5").split('"')[1].split('"')[0]
                print(f"[{name}]:{extracted_data}")
                break
            elif match.group(1):
                extracted_data = match.group(1).split('"')[1].split('"')[0]
                print(f"[{name}]:{extracted_data}")
                break
            if not bool(re.match(r"^\d{5}$", extracted_data)):
                print(f"[{name}]:giai captcha guru sai")
                extracted_data = captcha_text_1(id,api_key1,name)
                break
            elif any(char.isalpha() for char in extracted_data):
                print(f"[{name}]:giai captcha guru sai")
                extracted_data = captcha_text_1(id,api_key1,name)
                break
        else: 
            extracted_data = captcha_text_1(id,api_key1,name)
            break
        # Xác định giá trị trả về của hàm
    return extracted_data
    


def captcha_text_1(id, api_key1,name):
    image_path = f'./images/{id}.png'  # Thay đổi đường dẫn đến tệp ảnh của bạn
    try:
        # Đọc tệp ảnh dưới dạng dữ liệu nhị phân
        with open(image_path, 'rb') as file:
            image_data = file.read()
        # Mã hóa dữ liệu ảnh thành base64
        encoded_image = base64.b64encode(image_data)
        payload = {'key': api_key1, 'method': 'base64', 'body': encoded_image}
        r = requests.post("http://api.cap.guru/in.php", data=payload)
        print(r.text)
        while(True):
            rt = r.text.split('|')
            url = 'http://api.cap.guru/res.php?key=' + api_key1 + '&id=' + rt[1]
            response = requests.get(url)
            print(response.text)
            # Kiểm tra nếu response.content không rỗng và là dạng bytes trước khi thực hiện phép chia
            if response.text == "CAPCHA_NOT_READY":
                time.sleep(1)
            elif response.text=="ERROR_CAPTCHA_UNSOLVABLE":
                return None
            else :
                if response.content and isinstance(response.content, bytes):
                    extracted_data = response.text.split("|")[1]
                    print(f"[{name}]:{extracted_data}")
                    if not bool(re.match(r"^\d{5}$", extracted_data)):
                        return None
                    elif any(char.isalpha() for char in extracted_data):
                        return None
                    return extracted_data
                else:
                    return None
    except Exception as e:
        print('Error processing:', str(e))
        return None




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
        mail , pass_mail , proxy , user_payeer , pass_payeer , Secret_сode,key_master  = acc.split("|")
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
    elif len(acc.split("|")) >= 3 :
        mail , pass_mail , proxy = acc.split("|")
        user_payeer = ""
        pass_payeer = ""
        if proxy != "":
            if len(proxy.split(":")) == 4 :
                ip_proxy, port_proxy,user_proxy, pass_proxy = proxy.split(":")
            else:
                user_proxy = ""
                pass_proxy = ""
                ip_proxy, port_proxy = proxy.split(":")
            print(user_proxy)
            proxies_extension = proxies(user_proxy, pass_proxy.split("\n")[0], ip_proxy, port_proxy)
            time.sleep(2)
            chrome_options.add_extension(os.getcwd()+f"\\{ip_proxy}_{port_proxy}\\proxies_extension.zip")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://kiemtraip.com/raw.php")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    ip_address = soup.body.get_text()
    if "https://kiemtraip.com/raw.php" in ip_address:
        print("Proxy lỗi rồi")
        exit()
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
        time.sleep(0)
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
    return driver,mail , pass_mail , proxy , user_payeer , pass_payeer
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

def pay_out(driver,job_done,user_payeer):
    driver.get("https://seo-task.com/pay_out")
    time.sleep(2)
    name = driver.find_elements(By.XPATH, "//div[@class='balance_top']")[2].text.split(" ")[0]
    money = driver.find_element(By.XPATH, "//b[@class='balance_out']").text
    money_stop = float(money.split(" ")[0])
    print(f"[{name}]:Hoan Thanh {job_done}      So du {money_stop} ")
    if len(driver.find_elements(By.XPATH, "//div[@class='pay-cur pay-t-min ']")) != 0 :
        if driver.find_element(By.XPATH, "//div[@class='pay-cur pay-t-min ']").text =="Укажите кошелек" :
            print("Chua Them vi")
            if user_payeer != "":
                driver.find_element(By.XPATH, "//div[@class='pay-in-button pay-in-payeer']").click()
                time.sleep(3)
                driver.find_element(By.XPATH, "//button[@class='button.button_grey.button-gray']").click()
                input_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='payeer']"))
                )
                input_element.click()
                for char in user_payeer:
                    input_element.send_keys(char)
                    time.sleep(0.25)
                input_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@name='pin_code']"))
                )
                input_element.click()
                code = ""
                for char in code:
                    input_element.send_keys(char)
                    time.sleep(0.25)
                driver.find_element(By.XPATH, "//button[@class='button.button_grey.f-spinner.payeer_spin']").click()
            else :
                rut = 0
        else:
            if money_stop > 5.00:
                vi = driver.find_element(By.XPATH, "//div[@class='pay-cur pay-t-min ']").text
                driver.find_element(By.XPATH, "//div[@class='pay-cur pay-t-min ']").click()
                time.sleep(3)
                driver.find_element(By.XPATH, "//button[@class='button f-spinner']").click()
                print(f"[{name}]:Da rut {money} ve vi {vi}")
                time.sleep(10)
                rut = 1
            else:
                print(f"[{name}]:Khong du so du ")
                rut = 0
    else:
        rut = 0
    return  money_stop,rut

def start():
    driver, mail , pass_mail , proxy , user_payeer , pass_payeer = login(api_key1)
    time.sleep(5)
    stt_job = 0
    video_error = 0
    error_ip = 1
    check =0
    while(True):
        if len(driver.find_elements(By.XPATH, "//b[@class='balance_out']")) != 0:
            money = driver.find_element(By.XPATH, "//b[@class='balance_out']").text
            break
        else:
            time.sleep(1)
            check = check+1
            if check == 10 :
                exit()
    money_start = float(money.split(" ")[0])
    job_done = 0
    error_ip = 1
    while(True):
        print("check_002")
        if len(driver.find_elements(By.CLASS_NAME, 'info.info_warning'))!=0 :
            if driver.find_elements(By.CLASS_NAME, 'info.info_warning')[0].text == "Нет доступных сайтов":
                break
        try:
            name = driver.find_elements(By.XPATH, "//div[@class='balance_top']")[2].text.split(" ")[0]
            link_job = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'list-name'))
            )
            if len(driver.find_elements(By.CLASS_NAME, 'list-name')) == 0:
                driver.refresh()
                time.sleep(3)
                if len(driver.find_elements(By.CLASS_NAME, 'list-name')) == 0:
                    driver.quit()
                link_job = driver.find_element(By.CLASS_NAME, 'list-name')
            link_youtube_1 = link_job.get_attribute("onclick")
            link_youtube = link_youtube_1.split("ajax_func=")[1].split("'")[0]
            actions = ActionChains(driver)
            actions.move_to_element(link_job).perform()
            if len(driver.find_elements(By.CLASS_NAME, 'policy_button')) != 0 :
                driver.find_element(By.CLASS_NAME, 'policy_button').click()
                time.sleep(1)
            link_job.click()
            actions.reset_actions()
            time.sleep(5)
            if len(driver.find_elements(By.XPATH, "//div[@class='red']")) < error_ip:
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                timer_check = 0
                while(True):
                    if not "online-works.ru" or "seo-task.com" in driver.current_url:
                        error_ip = error_ip+1
                        print("["+name+"]:Failed")
                        driver.close()
                        driver.switch_to.window(handles[0])
                        break
                    else:
                        print("check_001")
                    timer_element = driver.find_elements(By.ID , "timer")
                    if  len(timer_element) == 1:
                        time.sleep(1)
                    else :
                        print("check")
                        time.sleep(2)
                        try:
                            button = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//span[text()='Подтвердить просмотр']"))
                            )
                            button.click()
                            print("["+name+"]:Success")
                            job_done = job_done+1
                            random_number = random.randint(4, 8)
                            time.sleep(random_number)
                            driver.close()
                            driver.switch_to.window(handles[0])
                            break
                        except TimeoutException :
                            print("["+name+"]:Failed")
                            driver.close()
                            driver.switch_to.window(handles[0])
                            break
                time.sleep(3)
            else :
                error_ip = error_ip+1
                print("["+name+"]:Failed")
        except TimeoutException :
            driver.refresh()
        random_number = random.randint(1, 20)
        time.sleep(random_number)
    time.sleep(3)
    reload = 0
    driver.get("https://seo-task.com/job_youtube")
    while(True):
        if video_error >= 4 and reload == 1:  
            video_error = 0
            break
        if len(driver.find_elements(By.CLASS_NAME, 'info.info_warning'))==1 :
            if driver.find_elements(By.CLASS_NAME, 'info.info_warning')[0].text == "Нет доступных сайтов":
                break
        try:
            name = driver.find_elements(By.XPATH, "//div[@class='balance_top']")[2].text.split(" ")[0]
            link_job = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'list-name'))
            )
            if len(driver.find_elements(By.CLASS_NAME, 'list-name')) == 0:
                driver.refresh()
                time.sleep(3)
                if len(driver.find_elements(By.CLASS_NAME, 'list-name')) == 0:
                    driver.quit()
                link_job = driver.find_element(By.CLASS_NAME, 'list-name')
            link_youtube_1 = link_job.get_attribute("onclick")
            link_youtube = link_youtube_1.split("ajax_func=")[1].split("'")[0]
            actions = ActionChains(driver)
            actions.move_to_element(link_job)
            driver.execute_script("arguments[0].click();", link_job)
            actions.reset_actions()
            if len(driver.find_elements(By.CLASS_NAME, 'policy_button')) != 0 :
                driver.find_element(By.CLASS_NAME, 'policy_button').click()
                time.sleep(1)
            link_job.click()
            time.sleep(5)
            if len(driver.find_elements(By.XPATH, "//div[@class='red']")) < error_ip:
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                try:
                    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "id_video")))
                except TimeoutException:
                    captcha_text_stats = check_captcha(driver,name)
                    if captcha_text_stats == False:
                        break
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "id_video")))
                try:
                    play_youtube = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'ytp-large-play-button'))
                    )
                    print("["+name+"]:start")
                    if video_error == 3:
                        break
                    time.sleep(4)
                    if len(driver.find_elements(By.CLASS_NAME, 'ytp-offline-slate.ytp-offline-slate-collapsed')) != 0:
                        driver.switch_to.default_content()
                        driver.find_element(By.CLASS_NAME, 'butt_skip').click()
                        print("["+name+"]:Failed")
                        video_error = video_error + 1
                        time.sleep(5)
                    elif len(driver.find_elements(By.CLASS_NAME, 'ytp-error-content-wrap-reason')) != 0 :
                        driver.switch_to.default_content()
                        driver.find_element(By.CLASS_NAME, 'butt_skip').click()
                        video_error = video_error + 1
                        print("["+name+"]:Failed")
                        time.sleep(5)
                    else:
                        video_error = 0
                        play_youtube.click()
                        print("["+name+"]:started")
                        driver.switch_to.default_content()
                        timer_element = driver.find_element(By.ID , "timer").text
                        time.sleep(5)
                        driver.switch_to.frame("id_video")
                        while(True):
                            if  "youtube.com" in driver.current_url :
                                error_ip = error_ip+1
                                print("["+name+"]:Done")
                                break
                            if len(driver.find_elements(By.CLASS_NAME, 'ytp-offline-slate.ytp-offline-slate-collapsed')) != 0:
                                video_error = video_error + 1
                                driver.switch_to.default_content()
                                driver.find_element(By.CLASS_NAME, 'butt_skip').click()
                                print("["+name+"]:Failed") 
                                time.sleep(5)
                                break
                            if len(driver.find_elements(By.ID, 'sub-frame-error')) != 0:
                                video_error = video_error + 1
                                driver.switch_to.default_content()
                                driver.find_element(By.CLASS_NAME, 'butt_skip').click()
                                print("["+name+"]:Failed") 
                                time.sleep(5)
                                break
                            driver.switch_to.default_content()
                            timer_start = driver.find_elements(By.ID , "timer")
                            if  len(timer_start) == 1:
                                timer_element1 = driver.find_elements(By.ID , "timer")
                                if len(timer_element1) !=0 :
                                    if timer_element1[0].text == timer_element:
                                        driver.switch_to.frame("id_video")
                                        play_youtube = WebDriverWait(driver, 20).until(
                                            EC.presence_of_element_located((By.CLASS_NAME, 'ytp-large-play-button'))
                                        )
                                        if len(driver.find_elements(By.CLASS_NAME, 'ytp-error-content-wrap-reason')) != 0 :
                                            driver.switch_to.default_content()
                                            driver.find_element(By.CLASS_NAME, 'butt_skip').click()
                                            print("["+name+"]:Failed")
                                            time.sleep(3)
                                            break
                                        else:
                                            play_youtube.click()
                                            driver.switch_to.default_content()
                                            check_captcha(driver,name)
                except TimeoutException:
                    print("Phần tử không xuất hiện sau thời gian chờ")
                    break
                driver.close()
                driver.switch_to.window(handles[0]) 
            else :
                error_ip = error_ip+1
                print("["+name+"]:failed")
        except TimeoutException :
            driver.refresh()
            reload = 1
        random_number = random.randint(1, 20)
        time.sleep(random_number)
    money_stop , rut = pay_out(driver,job_done,user_payeer)
    if rut == 1:
        payment_status = "Success"
    else:
        payment_status = "Failure"
    data = "Account:"+name+"Jobs Done:"+str(job_done)+"Money:"+str(money_stop)+"Payment Status:"+payment_status
    with open(current_date.strftime("%Y-%m-%d") + "_history.txt", "a") as file:
        file.write(data + "\n")
    print("["+name+"]:Done job")
    driver.quit()
max_workers = 4
stt_acc = 0
lock = threading.Lock()
def run_threads(max_workers):
    while True:  # Lặp vô hạn cho đến khi hết dữ liệu trong file
        stt_acc = 0  # Thiết lập lại stt_acc cho mỗi lần lặp
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            time.sleep(2)
            futures = {executor.submit(start, ) for _ in range(max_workers)}
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()

                except Exception as exc:
                    print(f"Error processing threads: {exc}")
        # Kiểm tra xem dữ liệu còn trong file hay không
        file_path = os.path.join(os.getcwd() + "\\data", "acc_seotask.txt")
        with open(file_path, "r") as file:
            data = file.readlines()
            if stt_acc >= len(data):  # Nếu stt_acc lớn hơn hoặc bằng tổng số dòng trong file
                break  # Dừng vòng lặp
if __name__ == "__main__":
    run_threads(max_workers)