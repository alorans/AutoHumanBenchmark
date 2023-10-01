########################################################################################################################
AutoHumanBenchmark

A simple Python command line to automate tests on humanbenchmark.com using Selenium.


########################################################################################################################
Installation


To install, run:

    git clone https://github.com/alorans/AutoHumanBenchmark.git
    cd AutoHumanBenchmark
    python Install.py

Or simply download the repository and save it in an empty folder, then run 'Install.py'.


To start the program, run:

    python HumanBenchmark.py


NOTE: On some systems, 'python3' is used instead of 'python' to execute python files.


On startup, the program
- installs & updates its PIP dependencies.
- opens a new Google Chrome window, after prompting the user to select visible or headless (invisible) mode.


Requirements:

- Google Chrome (latest version recommended)
- ChromeDriver (latest version recommended) **
- Selenium (>= 4.0.0) **
- Webdriver-manager (>= 4.0.0) **

** requirements are automatically maintained.


########################################################################################################################
Commands

General:

- Set login: Sets the username and password in 'login.txt'.
- Get login: Prints the username and password from 'login.txt'.
- Log in: Uses the login information in 'login.txt' to log in to Human Benchmark.
- Log out: Logs out from Human Benchmark.

- Get average scores: Prints the averages scores on all Human Benchmark tests for the current account. (Can be guest
account)
- New browser: Closes the current browser window and opens a new one, after prompting the user to select visible or
headless (invisible) mode.

- Help: Prints a list of commands.
- Exit: Closes the browser window and exits the program.

Tests:

- Typing: Runs the Typing test, after prompting the user for a target WPM.
- Sequence: Runs the Sequence Memory test, after prompting the user for a target score.
- Aim: Runs the Aim Trainer test, after prompting the user for a target time per target.
- Reaction time: Runs the Reaction Time test, after prompting the user for a target reaction time.
- Number memory: Runs the Number Memory test, after prompting the user for a target score.
- Chimp test: Runs the Chimp Test, after prompting the user for a target score.
- Visual memory: Runs the Visual Memory test, after prompting the user for a target score.
- Verbal memory: Runs the Verbal Memory test, after prompting the user for a target score.