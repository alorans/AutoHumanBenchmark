from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# create run function
def run_chimp_test(browser):
    # ask user for target score
    while True:
        target_score = input('Target score (4-41): ')
        try:
            target_score = int(target_score)
            if 4 <= target_score <= 41:
                break
            else:
                print('Invalid input. Please try again.')
        except ValueError:
            print('Invalid input. Please try again.')

    try:
        if browser.current_url == 'https://humanbenchmark.com/tests/chimp':
            browser.get('https://humanbenchmark.com/dashboard')
        browser.get('https://humanbenchmark.com/tests/chimp')
    except WebDriverException:
        print('Failed to load website')
        browser.quit()

    # create an explicit wait function for a max of 10 seconds
    wait = WebDriverWait(browser, 10)

    # wait for load function
    def wait_for_load(xpath_):
        while True:
            try:
                return wait.until(ec.visibility_of_element_located((By.XPATH, xpath_)))
            except TimeoutException:
                print('Browser timeout')
                browser.quit()

    # click start
    wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div[2]/button').click()

    print("\r" + " " * 50 + "\r", end='', flush=True)
    print(f'\rScore: 4 of {target_score}', end='', flush=True)
    for score in range(target_score - 4):
        # get dictionary of squares
        squares = {}
        for row in range(5):
            for column in range(8):
                xpath = f'//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div/div/div[{row + 1}]/div[{column + 1}]'
                number = wait_for_load(xpath).get_attribute('data-cellnumber')
                if number is not None:
                    squares[int(number)] = xpath
        # click on the squares in order
        for square_index in range(score + 4):
            browser.find_element(By.XPATH, squares[square_index + 1]).click()
        # click continue
        if score + 5 < 41:
            wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div[3]/button').click()
        print("\r" + " " * 50 + "\r", end='', flush=True)
        print(f'\rScore: {score + 5} of {target_score}', end='', flush=True)

    # get 3 wrong
    if target_score != 41:
        for wrong in range(3):
            found_square = False
            for row in range(5):
                for column in range(8):
                    xpath = f'//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div/div/div[{row + 1}]/div[{column + 1}]'
                    number = wait_for_load(xpath).get_attribute('data-cellnumber')
                    if number is not None and number != '1':
                        found_square = True
                        break
                if found_square:
                    break
            wait_for_load(xpath).click()
            if wrong != 2:
                wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div[3]/button').click()

    # save score
    while True:
        yes_no = input('\nSave score (y/n): ').lower()
        if yes_no == 'y':
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div[3]/button[1]').click()
            break
        elif yes_no == 'n':
            browser.get('https://humanbenchmark.com/dashboard')
            break
        else:
            print('Please enter either "y" or "n".')
