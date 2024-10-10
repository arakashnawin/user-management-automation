# User Management Script

## Overview

This project is a Python-based user management script that automates the creation of Linux system users and their associated groups. It generates secure passwords for each user and logs the process while securely storing generated passwords. The script is particularly useful in scenarios where administrators need to quickly onboard multiple users with specific group assignments on Linux servers.

## Why This Project?

Managing users manually, especially in environments with numerous users and groups, can be time-consuming and error-prone. This project aims to simplify and automate the user management process, reducing the administrative workload. By leveraging Python and shell commands, the script ensures consistency and efficiency in user creation and management.

## How This Project Helps

- **Automation:** Automates user creation and group assignment, saving time and minimizing errors.
- **Security:** Ensures secure password generation and stores passwords in a restricted file with proper permissions.
- **Logging:** Logs all activities for auditing and troubleshooting purposes, making it easy to track user management operations.
- **Scalability:** Handles multiple users and groups efficiently, making it ideal for environments with a growing number of users.

## Features

- **Root Privileges:** Ensures the script runs with the necessary privileges for managing system users.
- **User and Group Management:** Creates personal groups for users, assigns them to additional groups, and verifies the existence of groups before creation.
- **Password Generation and Storage:** Generates random, secure passwords for each user and stores them securely in a password file.
- **Logging:** Records actions, including errors and successful operations, to a designated log file.

## Usage

1. **Run the Script as Root**: This script requires root privileges to execute. Run it with `sudo` or as the root user.

2. **Provide an Input File**: The script takes a CSV input file with a list of users and optional group assignments.
   - Example CSV Format:
     ```csv
     username1;group1,group2
     username2;group3
     ```

3. **Command**:
   ```bash
   sudo ./user_management_script.py /path/to/input_file.csv
   ```

4. **Logging and Output**:
   - Logs are saved to `/var/log/user_management.log`.
   - Passwords are securely stored in `/var/secure/user_passwords.csv`.

## Dependencies

- Python 3.x
- Linux system with user and group management utilities

## Security Considerations

- **Log and Password Files**: Ensure that the log file (`/var/log/user_management.log`) and the password file (`/var/secure/user_passwords.csv`) have restricted permissions (600) to prevent unauthorized access.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

