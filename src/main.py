import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# OPTIONS
auto_evaluate_course = True
auto_evaluate_faculty = True

course_rating = None
faculty_rating = None


def main(_eval_code, _do_confirm, _ans, ):
    print("🎛 Loading drivers...")
    options = Options()
    if _do_confirm == 'n':
        options.add_argument('--headless')

    options.add_experimental_option('detach', True)

    service = Service('../drivers/chromedriver')
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
        if radios[i].get_attribute("name")[0] == 'c':
            if i % 4 == course_rating:
                radios[i].click()
        else:
            if i % 4 == faculty_rating:
                radios[i].click()

    if _do_confirm == 'n':
        print('📸 Taking screenshot...')
        save_screenshot(driver, f'./screenshots/{eval_code}-{datetime.now()}.png')

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
            if 0 < n < 5:
                return n
        except:
            continue


if __name__ == '__main__':
    ans = list()
    eval_code = input("Course evaluation code: ")
    do_confirm = input("Confirm before submit? [Y/n]: ")

    course_rating = must_input("Course rating [1 (Best) - 4 (Worst)]: ")
    faculty_rating = must_input("Faculty Rating [1 (Best) - 4 (Worst)]: ")

    main(eval_code, do_confirm, ans)
