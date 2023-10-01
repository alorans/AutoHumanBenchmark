import time
import copy
import math
from selenium.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# create run function
def run_visual_memory(browser):
    # ask user for target score
    while True:
        target_score = input('Target score: ')
        try:
            target_score = int(target_score)
            if target_score > 0:
                break
            print('Invalid input. Please try again.')
        except ValueError:
            print('Invalid input. Please try again.')

    try:
        if browser.current_url == 'https://humanbenchmark.com/tests/memory':
            browser.get('https://humanbenchmark.com/dashboard')
        browser.get('https://humanbenchmark.com/tests/memory')
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

    # create a grid object
    grid = browser.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div')

    # create a wait for grid update function
    def wait_grid_update():
        prev_grid_html = copy.copy(grid.get_attribute('outerHTML'))
        grid_html_ = copy.copy(grid.get_attribute('outerHTML'))
        while grid_html_ == prev_grid_html:
            grid_html_ = copy.copy(grid.get_attribute('outerHTML'))
            time.sleep(0.05)
        return grid_html_

    # remember active squares
    print("\r" + " " * 50 + "\r", end='', flush=True)
    print(f'Score: 1 of {target_score}', end='', flush=True)
    for score in range(target_score):
        grid_html = wait_grid_update()
        # make active squares list
        active_squares = []
        # extract active squares from html
        square_class_list = grid_html.split('class')[2:]
        grid_size = int(math.sqrt(len(square_class_list)))
        i = 0
        # add the active squares to the list in row, column format
        for square_class in square_class_list:
            if square_class[2] == 'a':
                active_squares.append((i // grid_size + 1, i % grid_size + 1))
            i += 1
        wait_grid_update()
        time.sleep(0.05)
        # click on the active squares
        for pos in active_squares:
            square = browser.find_element(
                By.XPATH, f'//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div/div[{pos[0]}]/div[{pos[1]}]')
            square.click()
        time.sleep(1)
        print("\r" + " " * 50 + "\r", end='', flush=True)
        print(f'\rScore: {score + 2} of {target_score}', end='', flush=True)

    # get 3 wrong
    print("\r" + " " * 50 + "\r", end='', flush=True)
    print('\rEnding game...', end='', flush=True)
    for wrong in range(3):
        grid_html = wait_grid_update()
        # make active squares list
        active_squares = []
        # extract active squares from html
        square_class_list = grid_html.split('class')[2:]
        grid_size = int(math.sqrt(len(square_class_list)))
        i = 0
        # add the active squares to the list in row, column format
        for square_class in square_class_list:
            if square_class[2] == 'a':
                active_squares.append((i // grid_size + 1, i % grid_size + 1))
            i += 1
        wait_grid_update()
        time.sleep(0.05)
        wrong_squares = 0
        for row in range(grid_size):
            for column in range(grid_size):
                if (row + 1, column + 1) not in active_squares:
                    square = browser.find_element(
                        By.XPATH,
                        f'//*[@id="root"]/div/div[4]/div[1]/div/div/div/div[2]/div/div[{row + 1}]/div[{column + 1}]')
                    square.click()
                    wrong_squares += 1
                if wrong_squares == 3:
                    break
            if wrong_squares == 3:
                break
        time.sleep(1)
    print('\rGame ended.')

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
