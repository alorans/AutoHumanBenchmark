from Typing import run_typing
from Sequence import run_sequence
from Aim import run_aim
from ReactionTime import run_reaction_time
from NumberMemory import run_number_memory
from ChimpTest import run_chimp_test
from VisualMemory import run_visual_memory
from VerbalMemory import run_verbal_memory
import Commands
import Import

if __name__ == '__main__':
    # initialize imports
    Import.import_req()

    # open web browser
    browser = Commands.new_browser()
    browser.get('https://humanbenchmark.com/dashboard')

    # logged in variable
    logged_in = False

    # list of commands
    commands = ('log in', 'log out', 'set login', 'get login', 'get average scores', 'new browser', 'help', 'exit')

    # list of tests
    tests = ('typing', 'sequence', 'aim', 'reaction time', 'number memory', 'chimp test', 'visual memory',
             'verbal memory')

    # ask user for command
    while True:
        command = input('>>> ')
        if command.lower() in commands:
            match command.lower():
                case 'log in':
                    logged_in = Commands.log_in(browser, logged_in)
                case 'log out':
                    logged_in = Commands.log_out(browser, logged_in)
                case 'set login':
                    Commands.set_login()
                case 'get login':
                    Commands.get_login()
                case 'get average scores':
                    Commands.get_average_scores(browser)
                case 'new browser':
                    browser = Commands.new_browser(browser)
                case 'help':
                    print('Commands:')
                    for command in commands:
                        print('- ' + command)
                    print('\nTests:')
                    for test in tests:
                        print('- ' + test)
                case 'exit':
                    break
        elif command.lower() in tests:
            match command.lower():
                case 'typing':
                    run_typing(browser)
                case 'sequence':
                    run_sequence(browser)
                case 'aim':
                    run_aim(browser)
                case 'reaction time':
                    run_reaction_time(browser)
                case 'number memory':
                    run_number_memory(browser)
                case 'chimp test':
                    run_chimp_test(browser)
                case 'visual memory':
                    run_visual_memory(browser)
                case 'verbal memory':
                    run_verbal_memory(browser)
        elif command == '':
            pass
        else:
            print('Invalid input. Please try again.')
        if browser.current_url != 'https://humanbenchmark.com/dashboard':
            browser.get('https://humanbenchmark.com/dashboard')
    browser.quit()
