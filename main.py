from bs4 import BeautifulSoup
from dateutil.rrule import *
from dateutil.rrule import rrule
from datetime import datetime
import re
import os
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


with open("info.json", "r") as f:
    userInfo = json.load(f)

selectedCourses = []

userid = userInfo["userid"]

password = userInfo["password"]

PATH = userInfo["ChromeDriverPath"]

service = Service(PATH)

os.chdir("output")

now = datetime.now()

dateNow = datetime.today().date()

filename = now.strftime("%Y-%m-%d_%H-%M-%S")

op = webdriver.ChromeOptions()
# uncomment this if you want chrome to be hidden.
op.add_argument('--headless')
op.add_argument('--service')
op.add_argument('--hide-scrollbars')
op.add_argument('--disable-gpu')
op.add_argument('--log-level=3')
driver = webdriver.Chrome(options=op)
driver.implicitly_wait(10)


driver.get("https://student.uwo.ca/")

useridField = driver.find_element(By.ID, "userid")
passwordField = driver.find_element(By.ID, "pwd")

useridField.send_keys(userid)
passwordField.send_keys(password)

submitButton = driver.find_element(By.CLASS_NAME, "ps-button")
submitButton.click()

print("\nPlease complete your 2FA.\n")

while (True):

    try:
        passedYet = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "win0divLPNAVSELECT")))
        break
    except:
        print("2FA failed, trying again.\n")
        driver.refresh()

print("2FA complete.\n")

driver.find_element(
    By.ID, "win0divPTNUI_LAND_REC_GROUPLET$2").click()

driver.find_element(
    By.ID, "win0divPTNUI_LAND_REC_GROUPLET$1").click()

time.sleep(5)

driver.find_element(
    By.ID, "DERIVED_SSR_FL_SSR_VW_CLSCHD_OPT_LBL").click()

time.sleep(5)

endDateEndTimeData = driver.page_source

time.sleep(5)

driver.find_element(
    By.ID, "DERIVED_SSR_FL_SSR_VW_CLSCHD_OPT$81$_LBL").click()

time.sleep(5)


checkDates = driver.page_source

soup = BeautifulSoup(endDateEndTimeData, "html.parser")
[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
visible_text = soup.getText()

text = str(visible_text)

text = str(text).replace(
    """Class\nStart/End Dates\nDays and Times\nRoom""", "")

responseTextEnd = open("responsetextend.txt", "w")
responseTextEnd.write(text)
responseTextEnd.close()


soup = BeautifulSoup(checkDates, "html.parser")
[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
visible_text = soup.getText()

textCheckCourses = str(visible_text)

responseCheckCourses = open("responseCheckCourses.txt", "w")
responseCheckCourses.write(textCheckCourses)
responseCheckCourses.close()

indicesOfTimes = [m.start()
                  for m in re.finditer("Time", textCheckCourses)]

indicesofEndOfTimes = []

for i in range(len(indicesOfTimes)):
    indicesofEndOfTimes.append(
        textCheckCourses[indicesOfTimes[i]::].find("\n")+indicesOfTimes[i])

indicesOfSubjects = []
indicesOfEndofSubjects = []
subjects = []

for i in range(len(indicesofEndOfTimes)):
    indicesOfSubjects.append(indicesofEndOfTimes[i]+3)

    indicesOfEndofSubjects.append(
        (textCheckCourses[indicesOfSubjects[i]::].find("\n"))+indicesOfSubjects[i])

    subjects.append(
        textCheckCourses[indicesOfSubjects[i]:indicesOfEndofSubjects[i]])


for i in range(len(subjects)):
    subjects[i] = (str(subjects[i].split(" ")[0]) + " " +
                   str(subjects[i].split(" ")[1])).strip()

daysScheduledIndices = [m.start()
                        for m in re.finditer("DaysSchedule", text)]

for i in range(len(daysScheduledIndices)):
    substring = text[daysScheduledIndices[i]:daysScheduledIndices[i]+35]
    text = text.replace(substring, "")

coursesStartIndices = [m.start()
                       for m in re.finditer("Component Details", text)]

coursesDeatils = []


for i in range(len(coursesStartIndices)):

    if i == len(coursesStartIndices)-1:
        coursesDeatils.append(text[coursesStartIndices[i]::])
    else:
        coursesDeatils.append(
            text[coursesStartIndices[i]:coursesStartIndices[i+1]:])


countOne = 0
OneIndices = []
titles = []
titlesOneArray = []


for i in range(len(coursesDeatils)):
    titlesForI = []
    titleIndices = [m.start()
                    for m in re.finditer("Section ", coursesDeatils[i])]
    lengthOfTitle = len("Section 001 LEC 2146")

    for j in range(len(titleIndices)):
        titlesForI.append(str(coursesDeatils[i])[
            titleIndices[j]:titleIndices[j]+lengthOfTitle])
        titlesOneArray.append(str(coursesDeatils[i])[
            titleIndices[j]:titleIndices[j]+lengthOfTitle])
    titles.append(titlesForI)


dateStartEndIndices = [m.start()
                       for m in re.finditer("Start/End Dates2", text)]
lengthOfBeginningOfdateStartEnd = len("Start/End Dates")
lengthOfDateStartEnd = len("2022/09/08 - 2022/12/08")

dateStartEnd = []


for i in range(len(dateStartEndIndices)):
    dateStartEnd.append(str(text)[
                        dateStartEndIndices[i]+lengthOfBeginningOfdateStartEnd:dateStartEndIndices[i]+lengthOfBeginningOfdateStartEnd+lengthOfDateStartEnd:])


daysIndices = [m.start()
               for m in re.finditer("DaysDays: ", text)]
lengthofBeginningOfdays = len("DaysDays: ")

timesIndices = [m.start()
                for m in re.finditer("TimesTimes: ", text)]
lengthofBeginningOfTimes = len("TimesTimes: ")
lengthofTimes = len("1:30PM to 2:30PM")

days = []
times = []
newLineIndicesTimes = []

for i in range(len(daysIndices)):
    days.append(str(text)[daysIndices[i] +
                lengthofBeginningOfdays:timesIndices[i]-1])


for i in range(len(timesIndices)):
    substring = text[timesIndices[i]::]
    newLineIndicesTimes.append(substring.find("\n")+timesIndices[i])
    times.append(str(text)[
                 timesIndices[i]+lengthofBeginningOfTimes:newLineIndicesTimes[i]])


roomIndices = [m.start()
               for m in re.finditer("Room", text)]
newLineIndicesroom = []
rooms = []
lengthRooms = len("Room")

for i in range(len(roomIndices)):
    substring = text[roomIndices[i]::]
    newLineIndicesroom.append(substring.find("\n")+roomIndices[i])

    rooms.append(str(text)[roomIndices[i]+lengthRooms:newLineIndicesroom[i]])


courseName = []
courseNameIndices = [m.start()
                     for m in re.finditer("Class Details", text)]
courseNameBeginning = len("Class Details - ")
newLineIndicesCourseName = []


for i in range(len(courseNameIndices)):
    substring = text[courseNameIndices[i]::]
    newLineIndicesCourseName.append(substring.find("\n")+courseNameIndices[i])
    courseName.append(
        text[courseNameIndices[i]+courseNameBeginning:newLineIndicesCourseName[i]])


howManyEachCourse = []


for i in range(len(courseNameIndices)):
    thisCourse = 0
    for j in range(len(daysIndices)):
        if i != len(courseNameIndices)-1:
            if daysIndices[j] > courseNameIndices[i] and daysIndices[j] < courseNameIndices[i+1]:
                thisCourse += 1
        else:
            if daysIndices[j] > courseNameIndices[i]:
                thisCourse += 1
    howManyEachCourse.append(thisCourse)

titleIndicesInText = [m.start()
                      for m in re.finditer("Section ", text)]

howManyEachComponent = []

for i in range(len(titleIndicesInText)):
    thisCourse = 0
    for j in range(len(daysIndices)):
        if i != len(titleIndicesInText)-1:
            if daysIndices[j] > titleIndicesInText[i] and daysIndices[j] < titleIndicesInText[i+1]:
                thisCourse += 1
        else:
            if daysIndices[j] > titleIndicesInText[i]:
                thisCourse += 1
    howManyEachComponent.append(thisCourse)

dateStart = []
dateEnd = []

for i in range(len(dateStartEnd)):
    temp = dateStartEnd[i].split(" - ")
    dateStart.append(temp[0])
    dateEnd.append(temp[1])

for i in range(len(times)):
    times[i] = times[i].replace("0P", "0 P")
    times[i] = times[i].replace("0A", "0 A")


timeStart = []
timeEnd = []

for i in range(len(times)):
    temp = times[i].split(" to ")
    timeStart.append(temp[0])
    timeEnd.append(temp[1])


html = open(filename+".csv", "a")

html.write("Subject,Start Time,End Time,Start Date,End Date,Location\n")


def datesBetweenTwoDates(startDate, endDate, weekDay):

    if weekDay == "Sunday":
        dayOfWeek = SU
    elif weekDay == "Monday":
        dayOfWeek = MO
    elif weekDay == "Tuesday":
        dayOfWeek = TU
    elif weekDay == "Wednesday":
        dayOfWeek = WE
    elif weekDay == "Thursday":
        dayOfWeek = TH
    elif weekDay == "Friday":
        dayOfWeek = FR
    elif weekDay == "Saturday":
        dayOfWeek = SA

    dates = []
    startDateSplit = startDate.split("/")
    endDateSplit = endDate.split("/")

    dateOne = datetime(int(startDateSplit[0]), int(
        startDateSplit[1]), int(startDateSplit[2]))
    dateTwo = datetime(int(endDateSplit[0]), int(
        endDateSplit[1]), int(endDateSplit[2]))

    for dt in rrule(WEEKLY, byweekday=dayOfWeek, dtstart=dateOne, until=dateTwo):
        dates.append(dt.strftime("%Y-%m-%d"))

    return dates


whereWeAre = 0

index = 0


for i in range(len(courseName)):
    for j in range(len(titles[i])):
        for k in range(howManyEachComponent[whereWeAre]):
            for weekDays in days[index].split(" "):
                for dates in datesBetweenTwoDates(dateStart[index], dateEnd[index], weekDays):
                    if dateNow <= datetime(int(str(dateEnd[index]).split("/")[0]), int(str(dateEnd[index]).split("/")[1]), int(str(dateEnd[index]).split("/")[2])).date():
                        if courseName[i] in subjects:
                            html.write(str(courseName[i]) + " " + str(titles[i][j].split(" ")[2])+"," +
                                       str(timeStart[index]) + "," +
                                       str(timeEnd[index]) + "," +
                                       str(dates) + "," +
                                       str(dates)+"," +
                                       str(rooms[index]) + "," +
                                       "\n")
                if len(weekDays) > 1 and weekDays != days[index].split(" ")[len(days[index].split(" "))-1]:
                    pass
                else:
                    index += 1
        whereWeAre += 1

print("Output CSV file has been saved in /output/"+str(filename)+".csv")

input("Press any button to exit.")
