from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# create run function
def run_number_memory(browser):
    # ask user for target score
    while True:
        target_score = input('Target score: ')
        try:
            target_score = int(target_score)
            break
        except ValueError:
            print('Invalid input. Please try again.')

    try:
        if browser.current_url == 'https://humanbenchmark.com/tests/number-memory':
            browser.get('https://humanbenchmark.com/dashboard')
        browser.get('https://humanbenchmark.com/tests/number-memory')
    except WebDriverException:
        print('Failed to load website')
        browser.quit()

    # click start
    while True:
        try:
            WebDriverWait(browser, 10).until(ec.visibility_of_element_located((
                By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[3]/button'))).click()
            break
        except TimeoutException:
            pass

    for level in range(target_score):
        # get number
        number = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[1]').text
        # wait for answer field to load then input number
        while True:
            try:
                WebDriverWait(browser, 0.02, 0.01).until(ec.visibility_of_element_located((
                    By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/form/div[2]/input'))).send_keys(number)
                break
            except TimeoutException:
                try:
                    width = browser.find_element(
                        By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div')
                    try:
                        lt = sum([i * 0.8 + 1.8 for i in range(level, target_score)])
                        lt = float(width.get_attribute("style")[7:].split("%")[0]) / 100 * (level * 0.8 + 1.8) + lt
                        print("\r" + " " * 50 + "\r", end='', flush=True)
                        print(f'\rDigits: {level + 1}   Est. time remaining: {lt:.2f} sec', end='', flush=True)
                    except StaleElementReferenceException:
                        pass
                except NoSuchElementException:
                    pass
        # press submit
        browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/form/div[3]/button').click()
        # press next
        browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/button').click()

    # get one wrong
    while True:
        try:
            WebDriverWait(browser, 0.02, 0.01).until(ec.visibility_of_element_located((
                By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/form/div[2]/input'))).send_keys('a')
            break
        except TimeoutException:
            try:
                width = browser.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div')
                try:
                    lt = float(width.get_attribute("style")[7:].split("%")[0]) / 100 * (target_score * 0.8 + 1.8)
                    print("\r" + " " * 50 + "\r", end='', flush=True)
                    print(f'\rEnding game...   Est. time remaining: {lt:.2f} sec', end='', flush=True)
                except StaleElementReferenceException:
                    pass
            except NoSuchElementException:
                pass
    browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/form/div[3]/button').click()
    print("\r" + " " * 50 + "\r", end='', flush=True)
    print(f'\rGame ended.   Est. time remaining: 0.00 sec', end='', flush=True)

    # save score
    while True:
        yes_no = input('\nSave score (y/n): ').lower()
        if yes_no == 'y':
            browser.find_element(By.XPATH,
                                 '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div/button[1]').click()
            break
        elif yes_no == 'n':
            browser.get('https://humanbenchmark.com/dashboard')
            break
        else:
            print('Please enter either "y" or "n".')
