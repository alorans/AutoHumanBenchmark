import time
from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# create run function
def run_verbal_memory(browser):
    # ask user for target score
    while True:
        target_score = input('Target score: ')
        try:
            target_score = int(target_score)
            break
        except ValueError:
            print('Invalid input. Please try again.')

    try:
        if browser.current_url == 'https://humanbenchmark.com/tests/verbal-memory':
            browser.get('https://humanbenchmark.com/dashboard')
        browser.get('https://humanbenchmark.com/tests/verbal-memory')
    except WebDriverException:
        print('Failed to load website')
        browser.quit()

    # create an explicit wait function for a max of 10 seconds
    wait = WebDriverWait(browser, 10)

    # wait for load function
    def wait_for_load(xpath):
        try:
            return wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print('Browser timeout')
            browser.quit()

    # click start
    while browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[4]/button').text != 'Start':
        time.sleep(0.05)
    browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[4]/button').click()

    # click seen if word has been seen before, otherwise new
    seen_words = []
    for score in range(target_score):
        wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div')
        word = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div').text
        if word in seen_words:
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[3]/button[1]').click()
        else:
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[3]/button[2]').click()
            seen_words.append(word)
        print("\r" + " " * 50 + "\r", end='', flush=True)
        print(f'\rScore: {score + 1} of {target_score}', end='', flush=True)

    # get 3 wrong answers
    for wrong in range(3):
        wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div')
        word = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div').text
        if word in seen_words:
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[3]/button[2]').click()
        else:
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[3]/button[1]').click()
            seen_words.append(word)

    # save score
    while True:
        yes_no = input('\nSave score (y/n): ').lower()
        if yes_no == 'y':
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div[3]/button[1]').click()
            break
        elif yes_no == 'n':
            browser.get('https://humanbenchmark.com/dashboard')
            break
        else:
            print('Please enter either "y" or "n".')
