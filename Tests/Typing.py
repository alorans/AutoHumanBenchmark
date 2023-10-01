import time
from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# create run function
def run_typing(browser):
    # ask user for target score
    while True:
        wpm = input('Target WPM: ')
        try:
            wpm = int(wpm)
            if wpm > 0:
                break
            else:
                print('Invalid input. Please try again.')
        except ValueError:
            print('Invalid input. Please try again.')

    try:
        if browser.current_url == 'https://humanbenchmark.com/tests/typing':
            browser.get('https://humanbenchmark.com/dashboard')
        browser.get('https://humanbenchmark.com/tests/typing')
    except WebDriverException:
        print('Failed to load website')
        browser.quit()

    # create an explicit wait function for a max of 10 seconds
    wait = WebDriverWait(browser, 10)

    # wait for load
    try:
        wait.until(ec.visibility_of_element_located((
            By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[2]/div/span[1]')))
    except TimeoutException:
        print('Browser timeout')
        browser.quit()

    # get html text list
    html_text = browser.find_elements(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[2]/div/span')

    # loop through and extract text
    plain_text = ''
    for html_char_index in range(len(html_text)):
        html_char = html_text[html_char_index]
        char = html_char.text
        if char == '':
            char = ' '
        plain_text = plain_text + char
        print("\r" + " " * 50 + "\r", end='', flush=True)
        print(f'\rReading character {html_char_index + 1} of {len(html_text)}', end='', flush=True)
    print('')

    # get start time
    start_time = time.time()

    # send all keys but last one
    field = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[2]/div')
    field.send_keys(plain_text[:-1])

    # wait for website wpm to equal specified wpm
    while True:
        web_wpm = int(browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[1]/h1').text)
        if web_wpm <= wpm:
            break
        current_char = int((time.time() - start_time) * (wpm / 12))
        if current_char < len(plain_text):
            print("\r" + " " * 50 + "\r", end='', flush=True)
            print(f'\rTyping character {current_char} of {len(plain_text)}', end='', flush=True)
        time.sleep(0.01)

    # send last character
    field.send_keys(char)
    print("\r" + " " * 50 + "\r", end='', flush=True)
    print(f'\rTyping character {len(plain_text)} of {len(plain_text)}', end='', flush=True)

    # wait for load function
    def wait_for_load(xpath):
        while True:
            try:
                return wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
            except TimeoutException:
                pass

    # print result
    print('\nResult: {}'.format(wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div[2]/h1').text))

    # save score
    while True:
        yes_no = input('Save score (y/n): ').lower()
        if yes_no == 'y':
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[3]/button[1]').click()
            break
        elif yes_no == 'n':
            browser.get('https://humanbenchmark.com/dashboard')
            break
        else:
            print('Please enter either "y" or "n".')
