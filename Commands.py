from selenium import webdriver
from selenium.common import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def log_in(browser, logged_in):
    if not logged_in:
        with open('login.txt', 'r') as login_file:
            login_text = login_file.read()
            if login_text == '':
                print('Username and password must be set before logging in.')
            else:
                try:
                    browser.get('https://humanbenchmark.com/login')
                except WebDriverException:
                    print('Failed to load website')
                    browser.quit()
                wait = WebDriverWait(browser, 10)
                username, password = login_text.split('\n')
                wait.until(ec.visibility_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div[4]/div/div/form/p[1]/input'))).send_keys(username)
                browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div/form/p[2]/input').send_keys(password)
                browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div/div/form/p[3]/input').click()
                try:
                    WebDriverWait(browser, 2).until(ec.url_changes('https://humanbenchmark.com/login'))
                    print('Login successful!')
                    return True
                except TimeoutException:
                    print('Failed to log in. Check login information.')
    else:
        print('Must be logged out to log in.')


def log_out(browser, logged_in):
    if logged_in:
        browser.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/a').click()
        print('Successfully logged out.')
    else:
        print('Must be logged in to log out.')
    return False


def set_login():
    username = input('Username: ')
    password = input('Password: ')
    if input('Save new login? (y/n): ').lower() == 'y':
        with open('login.txt', 'w') as login_file:
            login_file.write(username + '\n' + password)


def get_login():
    with open('login.txt', 'r') as login_file:
        login_text = login_file.read()
        if login_text == '':
            print('No data available. Username and password must be set first.')
        else:
            username, password = login_text.split('\n')
            print(f'Username: {username}\nPassword: {password}')


def get_average_scores(browser):
    browser.get('https://humanbenchmark.com/dashboard')
    WebDriverWait(browser, 10).until(ec.visibility_of_all_elements_located((
        By.XPATH, '//*[@id="root"]/div/div[4]/div/div/div[2]/div[2]/div/table[1]/tbody')))
    test_data = []
    for test_index in range(8):
        test_data.append([])
        xpath = f'//*[@id="root"]/div/div[4]/div/div/div[2]/div[2]/div/table[1]/tbody/tr[{test_index + 2}]'
        test_data[-1].append(browser.find_element(By.XPATH, xpath + '/td[1]/div').text)
        test_data[-1].append(browser.find_element(By.XPATH, xpath + '/td[3]/div').text)
        if test_data[-1][-1] != '?':
            try:
                test_data[-1].append(browser.find_element(By.XPATH, xpath + '/td[4]/div/div/div').text)
            except NoSuchElementException:
                test_data[-1].append(browser.find_element(By.XPATH, xpath + '/td[4]/div/span').text)
    longest_score = 0
    for test in test_data:
        score_length = len(test[1])
        if score_length > longest_score:
            longest_score = score_length
    for test in test_data:
        print(test[0] + ' ' * (18 - len(test[0])), end='')
        print(test[1] + ' ' * (longest_score - len(test[1])), end='')
        if len(test) == 3:
            print('   ' + test[2], end='')
        print('')


def new_browser(browser=None):
    if browser is not None:
        browser.quit()
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    while True:
        browser_visible = input('Browser is visible (y/n): ').lower()
        if browser_visible == 'n':
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=%s" % "1920,1080")
            break
        elif browser_visible == 'y':
            break
        print('Please enter either "y" or "n".')
    chrome_service = Service(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(options=chrome_options, service=chrome_service)
