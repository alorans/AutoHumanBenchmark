import time
from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# create run function
def run_reaction_time(browser):
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
        if browser.current_url == 'https://humanbenchmark.com/tests/reactiontime':
            browser.get('https://humanbenchmark.com/dashboard')
        browser.get('https://humanbenchmark.com/tests/reactiontime')
    except WebDriverException:
        print('Failed to load website')
        browser.quit()

    # create an explicit wait function for a max of 10 seconds
    wait = WebDriverWait(browser, 10)

    # wait for load function
    def wait_for_load(xpath):
        while True:
            try:
                return wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
            except TimeoutException:
                pass

    # wait for load
    wait_for_load('//*[@id="root"]/div/div[4]/div[1]')

    # loop through first 4 clicks
    print('Step 1 of 5', end='', flush=True)
    screen = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]')
    screen.click()
    average_latency = 0
    for click_counter in range(4):
        # click on target
        while True:
            screen_class = screen.get_attribute('class').split(' ', 1)[0]
            if screen_class == 'view-go':
                print("\r" + " " * 50 + "\r", end='', flush=True)
                print(f'\rStep {click_counter + 2} of 5', end='', flush=True)
                break
        screen.click()
        average_latency += int(wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div/div/h1/div').text[:-3])
        screen.click()
    average_latency /= 4000

    # do final click
    while True:
        screen_class = screen.get_attribute('class').split(' ', 1)[0]
        if screen_class == 'view-go':
            break
    if 5 * target_time > 4 * average_latency + 0.025:
        time.sleep(5 * target_time - 4 * average_latency - 0.025)
    screen.click()

    # print reaction time
    print('\nResult: {}'.format(wait_for_load('//*[@id="root"]/div/div[4]/div[1]/div/div/div[2]/h1').text))

    # save score
    while True:
        yes_no = input('Save score (y/n): ').lower()
        if yes_no == 'y':
            browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div[3]/button[1]').click()
            break
        elif yes_no == 'n':
            browser.get('https://humanbenchmark.com/dashboard')
            break
        else:
            print('Please enter either "y" or "n".')
