# Edval Timetable

## Description

Edval Timetable is a Python application designed to seamlessly retrieve your daily timetable from Edval using your unique Edval webcode. Simplify your school day planning with an easy-to-use interface and convenient keyboard navigation.

## Features

- **Display Timetable in Table Format:** Your timetable is neatly displayed in a readable table format, making it easy to view your daily schedule at a glance.
- **Keyboard Navigation:**
  - `[RIGHT ARROW]`: Move forward to view the timetable for the next day.
  - `[LEFT ARROW]`: Go back to view the timetable for the previous day.
  - `[UP ARROW]`: Quickly jump to the current date's timetable.
  - `[DELETE]`: Change your Edval webcode as needed.
  - `[ENTER]` / `[ESC]`: Exit the application.
- **Automatic Library Installation:** The app automatically installs all required libraries upon first launch, ensuring a smooth setup process.
- **Configuration File:** Your Edval webcode is securely stored in a `config.ini` file located in `AppData/Roaming/Edval Timetable`, ensuring easy access and management.
- **Clear Input Handling:** The application ignores unintended key presses, allowing for a focused and streamlined user experience.

## Installation

1. [Download](https://github.com/Skittlq/edval-timetable/releases/latest) and run the installer from the repositories releases section.

## Usage

Run the application and enter your Edval webcode when prompted. Use the arrow keys to navigate through your timetable and other specified keys to interact with the application:

- `[RIGHT ARROW]`: Next day
- `[LEFT ARROW]`: Previous day
- `[UP ARROW]`: Current day
- `[DELETE]`: Change webcode
- `[ENTER]` / `[ESC]`: Exit

The interface will only respond to these specific key presses, ensuring that your interaction is intentional and error-free.

## Note on Compatibility

Please note that this application is developed and tested on Unix-like and Windows operating systems. While it may work on other systems, such functionality is not guaranteed, and support for issues arising on non-supported platforms may be limited.

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).
