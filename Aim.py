import time
from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# create run function
def run_aim(browser):
    # ask user for target time
    while True:
        target_time = input('Target time (milliseconds): ')
        try:
            target_time = int(target_time)
            if target_time > 0:
                break
            else:
                print('Invalid input. Please try again.')
        except ValueError:
            print('Invalid input. Please try again.')
    target_time /= 1000

    try:
        if browser.current_url == 'https://humanbenchmark.com/tests/aim':
            browser.get('https://humanbenchmark.com/dashboard')
        browser.get('https://humanbenchmark.com/tests/aim')
    except WebDriverException:
        print('Failed to load website')
        browser.quit()

    # create an explicit wait function for a max of 10 seconds
    wait = WebDriverWait(browser, 10)

    # wait for load
    try:
        wait.until(ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div/div/div/div[6]')))
    except TimeoutException:
        print('Browser timeout')
        browser.quit()

    # create a new wait function with faster polling
    wait = WebDriverWait(browser, 10, poll_frequency=0.01)

    # loop through 30 targets
    for target_counter in range(31):
        start_time = time.time()
        # click on target
        wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div/div/div/div[6]'))).click()
        end_time = time.time()
        elapsed_time = end_time - start_time
        if target_time > elapsed_time:
            time.sleep(target_time - elapsed_time)
        print("\r" + " " * 50 + "\r", end='', flush=True)
        print(f'Step {target_counter} of 30', end='', flush=True)

    # wait for load function
    def wait_for_load(xpath):
        while True:
            try:
                return wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
            except TimeoutException:
                pass

    # print result
    print('\nResult: {}'.format(wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div/div[2]/h1').text))

    # save score
    while True:
        yes_no = input('Save score (y/n): ').lower()
        if yes_no == 'y':
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div[1]/div/div[3]/button[1]').click()
            break
        elif yes_no == 'n':
            break
        else:
            print('Please enter either "y" or "n".')
