import requests
from tabulate import tabulate
from termcolor import colored
from datetime import datetime, timedelta
import pytz
import configparser
import os
import requests
from packaging import version
import shutil
import subprocess
import sys
import tempfile

# Define config_file path globally
config_file = os.path.join(os.environ['APPDATA'], 'Edval Timetable', 'config.ini')

if not os.path.exists(os.path.dirname(config_file)):
    os.makedirs(os.path.dirname(config_file))

os.system('cls' if os.name == 'nt' else 'clear')

def install_libraries():
    print("Installing dependencies...")
    os.system('pip install requests tabulate termcolor pytz configparser')
    os.system('cls')
    print("Dependencies Installed!")

config = configparser.ConfigParser()

# Removed the re-definition of config_file
if not os.path.exists(config_file):
    config['Setup'] = {'LibrariesInstalled': 'False'}
    with open(config_file, 'w') as f:
        config.write(f)

config.read(config_file)

if config['Setup'].getboolean('LibrariesInstalled') == False:
    install_libraries()
    config['Setup']['LibrariesInstalled'] = 'True'
    with open(config_file, 'w') as f:
        config.write(f)
    os.system('cls' if os.name == 'nt' else 'clear')

def get_webcode():

    def validate_webcode(webcode):
        # Function to validate the webcode using the login API
        login_data = {"webCode": webcode, "rememberMe": False}
        login_response = requests.post(
            "https://my.edval.education/api/auth/login",
            json=login_data
        )
        return login_response.status_code == 200  # Returns True if status code is 200 (OK)

    if not os.path.exists(config_file) or not config.has_section('Credentials'):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            webcode = input('Enter your Edval webcode: ')
            if validate_webcode(webcode):  # Removed the re.match condition
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid webcode. Please enter a valid webcode.")  # Updated error message
        config['Credentials'] = {'webCode': webcode}
        with open(config_file, 'w') as f:  # Use config_file variable here
            config.write(f)
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        config.read(config_file)  # Use config_file variable here
        webcode = config['Credentials']['webCode']

        # Validate the stored webcode, prompt for new if invalid
        if not validate_webcode(webcode):
            print("Stored webcode is invalid, please enter a new webcode.")
            return get_webcode()  # Recursion to prompt for a new webcode

    return webcode

def print_timetable(day_offset=0):
    try:
        webcode = get_webcode()  # Get the webcode from the config file or user input

        # Login and get tokens
        login_data = {"webCode": webcode, "rememberMe": False}  # Use the webcode here
        login_response = requests.post(
            "https://my.edval.education/api/auth/login",
            json=login_data
        )
        login_response.raise_for_status()  # Check for errors
        tokens = login_response.json()

        # Get the current date
        tz = pytz.timezone('Australia/Sydney')  # Set the timezone to AEDT
        now = datetime.now(tz)  # Use the timezone when getting the current date
        
        # Calculate the date to query based on the day_offset
        target_date = now + timedelta(days=day_offset)
        weekday = target_date.weekday()

        # Adjust for weekends
        if weekday == 5:  # Saturday
            target_date += timedelta(days=2)  # Skip to Monday
        elif weekday == 6:  # Sunday
            target_date += timedelta(days=1)  # Skip to Monday

        # Adjust day_offset based on the new target_date
        day_offset = (target_date - now).days

        formatted_date = target_date.strftime('%Y-%m-%d')

        current_time = now.time()  # Get the current time

        # Now use the formattedDate in your axios get request URL
        fetchTT_response = requests.get(
            f"https://my.edval.education/api/v1/timetable?date={formatted_date}&resourceIds%5B%5D=S!442681597&viewType=day&timetableType=resourceTimetable&usual=false",
            headers={
                "Cookie": f"token={tokens['token']}; refreshToken={tokens['refreshToken']};",
                "Authorization": f"Bearer {tokens['token']}"
            }
        )
        fetchTT_response.raise_for_status()  # Check for errors
        fetchTT_data = fetchTT_response.json()

        def hex_to_rgb(value):
            value = value.lstrip('#')
            length = len(value)
            return tuple(
                int(value[i:i + length // 3], 16) for i in range(0, length, length // 3)
            )

        def add_breaks(table_data, day_name):
            def calculate_break_time(period_before_end, period_after_start):
                return period_before_end + " - " + period_after_start

            if "thu" in day_name:
                recess_time = calculate_break_time(
                    table_data[2][1].split(" - ")[1],
                    table_data[3][1].split(" - ")[0]
                )
                lunch_time = calculate_break_time(
                    table_data[4][1].split(" - ")[1],
                    table_data[5][1].split(" - ")[0]
                )
                table_data.insert(3, ["Recess", recess_time, ""])
                table_data.insert(6, ["Lunch", lunch_time, ""])
            else:
                recess_time = calculate_break_time(
                    table_data[3][1].split(" - ")[1],
                    table_data[4][1].split(" - ")[0]
                )
                lunch_time = calculate_break_time(
                    table_data[5][1].split(" - ")[1],
                    table_data[6][1].split(" - ")[0]
                )
                table_data.insert(4, ["Recess", recess_time, ""])
                table_data.insert(7, ["Lunch", lunch_time, ""])

        table_data = []
        timetable = fetchTT_data['data'][0]
        day_name = timetable['dayName'].lower()
        table_data.append([timetable['dayName'], "", ""])

        skipped_first_assembly = False
        for timetable_object in timetable['timetables']:
            for item in timetable_object['items']:
                if (
                    (item['classSubject'] == "Assembly" and "thu" in day_name and skipped_first_assembly) or
                    (item['classSubject'] not in ["Assembly", "TAFE Course", "Scripture"] and
                    not ("thu" in day_name and "Home Room" in item['classSubject']))
                ):
                    rgb = hex_to_rgb(item['colorHex'])
                    color = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
                    reset_color = "\033[0m"
                    activity = f"{color}{item['activity']} - {item['classSubject']}{reset_color}"
                    # Convert epoch milliseconds to seconds
                    epoch_seconds_from = item['from'] / 1000
                    epoch_seconds_to = item['to'] / 1000

                    # Convert epoch seconds to datetime objects
                    # Use the timezone when converting epoch seconds to datetime objects
                    dt_from = datetime.fromtimestamp(epoch_seconds_from, tz)
                    dt_to = datetime.fromtimestamp(epoch_seconds_to, tz)
                    time_from = dt_from.strftime('%I:%M %p')
                    time_to = dt_to.strftime('%I:%M %p')

                    # Check if the current time is within this period
                    is_current_period = dt_from.time() <= current_time <= dt_to.time()

                    # Highlight the current period in bold
                    bold_start = "\033[1m• " if is_current_period else ""
                    bold_end = "\033[0m" if is_current_period else ""

                    teacher_name = item.get('teacherName', '')
                    room_code = item.get('roomCode', '')
                    table_data.append([
                        f"{bold_start}{activity}{bold_end}",
                        f"{bold_start}{time_from} - {time_to}{bold_end}",
                        f"{bold_start}{teacher_name} - {room_code}{bold_end}" if teacher_name and room_code else (teacher_name or room_code)
                    ])
                elif item['classSubject'] == "Assembly" and not skipped_first_assembly:
                    skipped_first_assembly = True

        add_breaks(table_data, day_name)  # Call the function to add breaks

        table_output = tabulate(table_data, headers='firstrow', tablefmt='fancy_grid')
        print(table_output)
        # At the end of the print_timetable function, before the except block:
        return day_offset
    
    except requests.RequestException as e:
        print(f"Error: {e}")

def prompt_user_action():
    print("\nOptions:")
    print("[Enter] to exit.")
    print("'change' to change your Edval webcode.")
    print("'today' to view today's timetable.")
    print("'next' to view the next day's timetable.")
    print("'prev' to view the previous day's timetable.")
    user_input = input("What would you like to do? ")
    return user_input.lower().strip()

def perform_action(action, current_offset):
    if action == 'change':
        if os.path.exists(config_file):
            os.remove(config_file)
        return 0, True  # Reset to today's timetable, change webcode
    elif action == 'today':
        return 0, False  # Reset to today's timetable, do not change webcode
    elif action == 'next':
        # If the current day is Friday, add 3 to skip the weekend
        if (datetime.now() + timedelta(days=current_offset)).weekday() == 4:
            return current_offset + 3, False
        return current_offset + 1, False  # Increment offset by 1, do not change webcode
    elif action == 'prev':
        # If the current day is Monday, subtract 3 to go back to Friday
        if (datetime.now() + timedelta(days=current_offset)).weekday() == 0:
            return current_offset - 3, False
        # If the current day is Sunday, subtract 2 to go back to Friday
        elif (datetime.now() + timedelta(days=current_offset)).weekday() == 6:
            return current_offset - 2, False
        return current_offset - 1, False  # Decrement offset by 1, do not change webcode
    return current_offset, False  # No action, retain current offset, do not change webcode

def get_latest_release_info():
    # URL of the latest release in GitHub API
    url = "https://api.github.com/repos/Skittlq/edval-timetable/releases/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()
        latest_release = response.json()
        return latest_release
    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
        return None

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename

def apply_update(download_url):
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(f"Downloading update from {download_url}")
        downloaded_file_path = download_file(download_url, os.path.join(tmpdirname, 'timetable.exe'))
        current_executable_path = sys.executable
        
        print("Applying update...")
        # Replace the old executable with the new one
        shutil.copyfile(downloaded_file_path, current_executable_path)
        
        # Restart the application
        print("Restarting application...")
        subprocess.Popen([current_executable_path] + sys.argv[1:])
        sys.exit()

def check_for_updates(current_version):
    latest_release = get_latest_release_info()
    if latest_release:
        latest_version_tag = latest_release['tag_name']
        latest_version = version.parse(latest_version_tag)
        if latest_version > version.parse(current_version):
            print(f"New version available: {latest_version}")
            download_url = ""
            for asset in latest_release['assets']:
                if asset['name'] == "timetable.exe":
                    download_url = asset['browser_download_url']
                    break
            if download_url:
                apply_update(download_url)
            else:
                print("No executable found for the update.")
        else:
            print("You have the latest version.")

if __name__ == '__main__':
    CURRENT_VERSION = "1.2.1"  # Replace with the current version of your app
    check_for_updates(CURRENT_VERSION)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Edval Timetable ", CURRENT_VERSION)
    day_offset = 0  # Start with today's timetable
    change_webcode = False
    while True:
        # Save the returned day_offset from print_timetable to a variable
        new_day_offset = print_timetable(day_offset)
        action = prompt_user_action()
        if action == '':
            break  # Exit the program
        # Update day_offset based on the action, while keeping track of the change_webcode flag
        day_offset, change_webcode = perform_action(action, new_day_offset)
        if change_webcode:
            # User chose to change webcode, re-prompt for it
            get_webcode()
            day_offset = 0  # Reset to today's timetable after changing webcode
        os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Program exited.")