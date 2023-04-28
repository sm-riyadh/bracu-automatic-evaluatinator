import os
import time
import datetime
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

system = platform.system()

# OPTIONS
auto_evaluate_course = True
auto_evaluate_faculty = True

course_rating = None
faculty_rating = None

course_rating_catagory = {
    1: "Strongly Agree",
    2: "Agree",
    3: "Neutral",
    4: "Disagree",
    5: "Strongly Disagree"
}

faculty_rating_catagory = {
    1: "Excellent",
    2: "Very Good",
    3: "Good",
    4: "Satisfactory",
    5: "Poor"
}


def main(_eval_code, _do_confirm, _ans, ):
    print("🎛 Loading drivers...")
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    if _do_confirm != 'n' or  _do_confirm != 'N':
        options.add_argument('--headless')

    options.add_experimental_option('detach', True)

    if system == 'Linux':
        service = Service('../drivers/linux64/chromedriver')
    elif system == 'Windows':
        service = Service('../drivers/win32/chromedriver')
    elif system == 'Darwin':
        if platform.mac_ver()[0].startswith('12'):
            service = Service('../drivers/mac-arm64/chromedriver')
        else:
            service = Service('../drivers/mac64/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)

    url = 'https://bout.eveneer.xyz/evaluation-form'
    driver.get(url)
    print("🖊 Evaluation...")
    time.sleep(4)

    input_field = driver.find_element(By.TAG_NAME, 'input')
    input_field.send_keys(_eval_code)
    button = driver.find_element(By.TAG_NAME, 'button')
    button.click()
    time.sleep(4)

    radios = driver.find_elements(By.XPATH, '//input[@type=\'radio\']')

    for i in range(len(radios)):
        if radios[i].get_attribute("name")[0] == 'c' and radios[i].get_attribute("value") == course_rating_catagory[course_rating]:
            radios[i].click()
        elif radios[i].get_attribute("name")[0] == 'f' and radios[i].get_attribute("value") == faculty_rating_catagory[faculty_rating]:
            radios[i].click()

    if _do_confirm != 'n' or _do_confirm != 'N':
        print('📸 Taking screenshot...')

        ss_folder = 'screenshots'

        if not os.path.exists(ss_folder):
            os.makedirs(ss_folder)

        save_screenshot(driver, f'./{ss_folder}/{eval_code}-{datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.png')

        button = driver.find_element(By.TAG_NAME, 'button')
        button.click()

        time.sleep(4)
        if 'Evaluation submitted' in driver.page_source:
            print("🎉 DONE EVALUATION! 🥳")

        driver.close()


def save_screenshot(driver, path):
    body = driver.find_element(By.TAG_NAME, 'body')
    driver.set_window_size(1920, body.size["height"] + 1000)
    driver.save_screenshot(path)


def must_input(t):
    while True:
        try:
            n = int(input(t))
            if 0 < n < 6:
                return n
        except:
            continue


if __name__ == '__main__':
    ans = list()
    eval_code = input("Course evaluation code: ")
    do_confirm = input("Run in ghost mode? [Y/n]: ")
    course_rating = must_input("Course rating [1 (Best) - 5 (Worst)]: ")
    faculty_rating = must_input("Faculty Rating [1 (Best) - 5 (Worst)]: ")

    main(eval_code, do_confirm, ans)
