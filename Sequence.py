import time
from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# create run function
def run_sequence(browser):
    # ask user for target score
    while True:
        target_score = input('Target score: ')
        try:
            target_score = int(target_score)
            break
        except ValueError:
            print('Invalid input. Please try again.')

    try:
        if browser.current_url == 'https://humanbenchmark.com/tests/sequence':
            browser.get('https://humanbenchmark.com/dashboard')
        browser.get('https://humanbenchmark.com/tests/sequence')
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

    # click start button
    wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/button').click()

    # create list of XPaths for the squares
    wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div/div[3]/div[3]')
    squares = []
    for row in range(3):
        for column in range(3):
            squares.append(f'//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div/div[{row + 1}]/div[{column + 1}]')

    # main loop
    for level in range(target_score):
        start_time = time.time()
        # create sequence list
        sequence = []
        sequence_step = 0
        # check squares during sequence
        while sequence_step <= level:
            for square_index in range(9):
                # append active square to sequence list
                if browser.find_element(By.XPATH, squares[square_index]).get_attribute('class') == 'square active':
                    if sequence == [] or square_index != sequence[-1]:
                        sequence.append(square_index)
                        sequence_step += 1
                        break
            remaining = sum([i * 0.5 + 1.1 for i in range(level, target_score)]) + (target_score * 0.5 + 1.1)
            remaining = remaining - (time.time() - start_time)
            if remaining <= 0:
                remaining = 0
            print("\r" + " " * 50 + "\r", end='', flush=True)
            print(f'\rLevel: {level + 1}   Est. time remaining: {remaining:.2f} sec',
                  end='', flush=True)
            time.sleep(0.05)
        # click on squares in the order of the sequence
        time.sleep(0.5)
        for square_index in sequence:
            browser.find_element(By.XPATH, squares[square_index]).click()

    # get one wrong
    start_time = time.time()
    sequence = []
    sequence_step = 0
    # check squares during sequence
    while sequence_step <= target_score:
        for square_index in range(9):
            # append active square to sequence list
            if browser.find_element(By.XPATH, squares[square_index]).get_attribute('class') == 'square active':
                if sequence == [] or square_index != sequence[-1]:
                    sequence.append(square_index)
                    sequence_step += 1
                    break
        remaining = target_score * 0.5 + 1.1 - (time.time() - start_time)
        if remaining <= 0:
            remaining = 0
        print("\r" + " " * 50 + "\r", end='', flush=True)
        print(f'\rEnding game...   Est. time remaining: {remaining:.2f} sec', end='', flush=True)
        time.sleep(0.05)
    print("\r" + " " * 50 + "\r", end='', flush=True)
    print(f'\rGame ended.   Est. time remaining: 0.00 sec', end='', flush=True)
    time.sleep(0.5)
    browser.find_element(By.XPATH, squares[1]).click()

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
            print('Please enter either "y" or "n".', end='')
