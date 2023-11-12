# Edval Timetable Fetcher

## Description
Edval Timetable is a Python application designed to seamlessly retrieve your daily timetable from Edval using your unique Edval webcode. Simplify your school day planning with an easy-to-use interface and convenient commands.

## Features
- **Display Timetable in Table Format:** Your timetable is neatly displayed in a readable table format, making it easy to view your daily schedule at a glance.
- **Navigation Commands:**
  - `next`: Move forward to view the timetable for the next day.
  - `prev`: Go back to view the timetable for the previous day.
  - `today`: Quickly jump to the current date's timetable.
  - `change`: Change your Edval webcode as needed.
- **Automatic Library Installation:** The app automatically installs all required libraries upon first launch, ensuring a smooth setup process.
- **Configuration File:** Your Edval webcode is securely stored in a `config.ini` file located in `AppData/Roaming/Edval Timetable`, ensuring easy access and management.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Skittlq/edval-timetable.git
   ```
2. Navigate to the cloned directory and run the application. On first launch, it will automatically install necessary Python libraries.

## Usage
Run the application and enter your Edval webcode when prompted. Use the navigation commands (`next`, `prev`, `today`, `change`) to interact with your timetable.

## Note on Compatibility
Please note that this application is developed and tested exclusively for Windows operating systems. While it may work on other systems, such functionality is not guaranteed, and support for issues arising on non-Windows platforms may be limited.

## License
This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).
