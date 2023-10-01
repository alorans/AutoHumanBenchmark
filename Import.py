import importlib
import subprocess


def import_req():
    def pip_install(package):
        try:
            result = subprocess.Popen(['pip', 'install', '--upgrade', package], stdout=subprocess.PIPE)
            output = result.communicate()[0].decode('utf-8').split('\r\n')
            for statement in output:
                if not statement.startswith('Requirement already satisfied: '):
                    print(statement)
            print(f"{package.capitalize()} and its dependencies have been successfully checked for upgrades.")
        except subprocess.CalledProcessError as e:
            print(f"Experienced pip error upgrading {package}: {e}")

    requirements = {
        'selenium': 'selenium',
        'webdriver-manager': 'webdriver_manager'
    }

    for module in requirements:
        pip_install(module)
        importlib.import_module(requirements[module])
