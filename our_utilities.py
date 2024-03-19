# our_utilities.py
import os, re, subprocess
from dotenv import find_dotenv, load_dotenv


def load_env_with_substitutions():
    
    # First do a normal load of the .env file
    load_dotenv(find_dotenv('local-secrets.env'), override=True)
    load_dotenv(find_dotenv('.env'), override=True)

    # Then go through again and perform command substitutions
    # TODO : Add the possibility of multiple files found !!
    with open(find_dotenv('.env'), 'r') as file:
        for line in file:
            # Ignore comments
            if line.startswith('#'):
                continue

            # Check if the line matches the pattern: alphanumeric characters, equals sign, any characters except '#'
            match = re.match(r'^([a-zA-Z0-9_]+)=([^#]*)(#.*)?$', line.strip())
            if match:
                key, value, _ = match.groups()

                # Check if the value contains a command substitution
                match = re.search(r'\$\((.*)\)', value)
                if match:
                    # Execute the command and get the output
                    command = match.group(1)
                    output = subprocess.check_output(command, shell=True, env=os.environ).decode().strip()

                    # Set the environment variable with the output of the command
                    os.environ[key] = output