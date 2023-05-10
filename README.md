# Western Timetable Exporter

~~**IMPORTANT NOTE:** This program is now available as a web application at https://western-schedule-exporter.web.app/. You can access all of its features and export your course timetable directly from the website without the need to install any packages or run any Python code.~~

The Western Timetable Exporter is a Python program that exports your course timetable from Western University's student center to a CSV file. The CSV file can be imported into Google Calendar or other calendar apps, allowing you to easily view your course schedule on the go.

## Requirements

- Python 3.6 or later
- BeautifulSoup 4
- dateutil
- requests
- selenium
- ChromeDriver

## Installation

1. Download or clone the repository.
2. Navigate to the project directory.
3. Install the required packages using pip:

```
pip install -r requirements.txt
```
4. Install ChromeDriver for your installed Google Chrome version.
5. Change the "PATH" varaible to where your ChromeDriver.exe is.

## Usage

1. Run the program:

```
python main.py
```

2. Enter your Western University username and password when prompted.
3. Complete your 2FA.
4. The program will export your course timetable to a CSV file in the `output` directory.
5. Import the CSV file into your calendar app.

## Limitations

- The program only works for Western University students.
- The program only exports course information (title, start time, end time, location). It does not export other events such as exams or assignments.
