#!/usr/bin/env python3

import os
import sys
import csv
import logging
import random
import string
import subprocess

#---------------------------------------------#
# Author: Akash Nawin
#---------------------------------------------#

# Define the file paths for the logfile, and the password file
LOG_FILE = "/var/log/user_management.log"
PASSWORD_FILE = "/var/secure/user_passwords.csv"

# Ensure script is run with root privileges
if os.geteuid() != 0:
    print("Please run this script with root or sudo privileges.")
    sys.exit(1)

# Check if user list file path is provided as argument
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input_file>")
    sys.exit(1)

INPUT_FILE = sys.argv[1]

# Check if user list file exists
if not os.path.isfile(INPUT_FILE):
    print(f"User list file '{INPUT_FILE}' not found. Please check the path.")
    sys.exit(1)

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(message):
    logging.info(message)

# Create the log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'w').close()
    os.chmod(LOG_FILE, 0o600)
    log_message(f"Log file created: {LOG_FILE}")

# Create the password file if it doesn't exist
if not os.path.exists(PASSWORD_FILE):
    os.makedirs('/var/secure', exist_ok=True)
    open(PASSWORD_FILE, 'w').close()
    os.chmod(PASSWORD_FILE, 0o600)
    log_message(f"Password file created: {PASSWORD_FILE}")

# Function to generate a random password
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for i in range(length))

# Function to execute a shell command
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        log_message(f"Error executing command: {command}\\nError: {e.stderr.decode()}")
        sys.exit(1)

# Read the input file and process each user
with open(INPUT_FILE, 'r') as infile:
    reader = csv.reader(infile, delimiter=';')

    for row in reader:
        if len(row) == 0:
            continue

        username = row[0].strip()
        groups = row[1].strip() if len(row) > 1 else ""

        # Check if personal group exists, create it if not
        if run_command(f"getent group {username}") == "":
            run_command(f"groupadd {username}")
            log_message(f"Created personal group {username}")

        # Check if the user exists
        if run_command(f"id -u {username}") != "":
            log_message(f"User {username} already exists")
        else:
            # Create a new user with the personal group
            run_command(f"useradd -m -g {username} -s /bin/bash {username}")
            log_message(f"Created a new user {username}")

        # Process the groups if provided
        if groups:
            group_list = [g.strip() for g in groups.split(',')]
            for group in group_list:
                # Check if group exists, create it if not
                if run_command(f"getent group {group}") == "":
                    run_command(f"groupadd {group}")
                    log_message(f"Created group {group}")

                # Add user to the group
                run_command(f"usermod -aG {group} {username}")
                log_message(f"Added user {username} to group {group}")

        # Create and set the user password
        password = generate_password()
        run_command(f'echo "{username}:{password}" | chpasswd')

        # Save user and password to the password file
        with open(PASSWORD_FILE, 'a') as pwdfile:
            pwdfile.write(f"{username},{password}\\n")
        log_message(f"Password for {username} generated and saved")

log_message("User creation process completed successfully")
print("Users have been created and added to their groups successfully.")
