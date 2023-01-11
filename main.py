from bs4 import BeautifulSoup
from dateutil.rrule import *
from dateutil.rrule import rrule
from datetime import datetime
import re
import requests
import os
import time


def getICSID(htmldoc):
    soup = BeautifulSoup(htmldoc, "html.parser")
    return (str(soup.find(id="ICSID").get("value")))


os.chdir("output")

now = datetime.now()

dateNow = datetime.today().date()

filename = now.strftime("%Y-%m-%d_%H-%M-%S")


loginURL = "https://student.uwo.ca/psp/heprdweb/?&cmd=login&languageCd=ENG"
get1URL = "https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID:PTPPNAVCOL&scname=ADMN_MANAGE_MY_CLASSES&PTPPB_GROUPLET_ID=WSA_MANAGE_CLASSES&CRefName=ADMN_NAVCOLL_5"
get2URL = "https://student.uwo.ca/psc/heprdweb_newwin/EMPLOYEE/SA/c/PTGP_MENU.PTGP_GROUPLETS_FL.GBL?PTGP_TYPE=NavigationCollectionDataSource&PAGE=PTGP_GPLT_NV_FL&AGComp=N&TEMPLATE_ID=PTPPNAVCOL&scname=ADMN_MANAGE_MY_CLASSES&ICDoModal=1&ICGrouplet=1&ICAction=GROUPLET_CONTENTS$hmodal&ICLoc=1&nWidth=286&nHeight=17"
get3URL = "https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_COMPONENT_FL.GBL?Page=SSR_VW_CLASS_FL&NavColl=true&ICAJAX=1&ICAGTarget=start&ICPanelControlStyle=pst_side1-fixed pst_panel-mode"

userid = input("Enter your userid:\n")
password = input("Enter your password:\n")

formData = {
    "httpPort2": "",
    "timezoneOffset": 300,
    "ptmode": "f",
    "ptlangcd": "ENG",
    "ptinstalledlang": "ENG",
    "userid": userid,
    "pwd": password
}

dataURL = "https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_COMPONENT_FL.GBL?PAGE=SSR_VW_CLASS_FL"

postURL = "https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_COMPONENT_FL.GBL"

s = requests.Session()

try:
    print("Logging in...")
    response = s.post(loginURL, data=formData)
    print("\nGetting schedule...")
    icsidResponse = s.get(get1URL)
    iscid = getICSID(icsidResponse.text)
    s.get(get2URL)
    s.get(get3URL)

    postFormData = {
        "ICAction": "DERIVED_SSR_FL_SSR_VW_CLSCHD_OPT",
        "ICModelCancel": "0",
        "ICXPos": "0",
        "ICYPos": "0",
        "ResponsetoDiffFrame": "-1",
        "TargetFrameName": "None",
        "FacetPath": "None",
        "ICFocus": "",
        "ICSaveWarningFilter": "0",
        "ICChanged": "0",
        "ICSkipPending": "0",
        "ICAutoSave": "0",
        "ICResubmit": "0",
        "ICSID": str(iscid),
        "ICAGTarget": "true",
        "ICActionPrompt": "false",
        "ICBcDomData": "C~UnknownValue~EMPLOYEE~SA~NUI_FRAMEWORK.PT_LANDINGPAGE.GBL~PT_LANDINGPAGE~Student Homepage~UnknownValue~UnknownValue~https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL?~UnknownValue*C~UnknownValue~EMPLOYEE~SA~PT_FLDASHBOARD.PT_FLDASHBOARD.GBL~PT_LANDINGPAGE~Academics~UnknownValue~UnknownValue~https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/PT_FLDASHBOARD.PT_FLDASHBOARD.GBL?DB=WSA_ACADEMICS&lp=SA.EMPLOYEE.WSA_ACADEMICS~UnknownValue*C~UnknownValue~EMPLOYEE~SA~PT_FLDASHBOARD.PT_FLDASHBOARD.GBL~PT_LANDINGPAGE~Academics~UnknownValue~UnknownValue~https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/PT_FLDASHBOARD.PT_FLDASHBOARD.GBL?DB=WSA_ACADEMICS&lp=SA.EMPLOYEE.WSA_ACADEMICS~UnknownValue*C~UnknownValue~EMPLOYEE~SA~NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL~PT_AGSTARTPAGE_NUI~Course Registration~UnknownValue~UnknownValue~https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID%3aPTPPNAVCOL&scname=ADMN_MANAGE_MY_CLASSES&PTPPB_GROUPLET_ID=WSA_MANAGE_CLASSES&CRefName=ADMN_NAVCOLL_5&ptgpid=ADMN_S202205301002261020844141~UnknownValue",
        "ICDNDSrc": "",
        "ICPanelHelpUrl": "http://www.registrar.uwo.ca/general-information/how_to_guides/index.html",
        "ICPanelName": "",
        "ICPanelControlStyle": "pst_side1-fixed pst_panel-mode pst_side2-hidden",
        "ICFind": "",
        "ICAddCount": "",
        "ICAppClsData": "",
        "win0hdrdivPT_SYSACT_HELP": "",
        "DERIVED_SSR_FL_SSR_VW_CLSCHD_OPT": "L"
    }

    checkCoursesFormData = {
        "ICAction": "DERIVED_SSR_FL_SSR_VW_CLSCHD_OPT$81$",
        "ICModelCancel": "0",
        "ICXPos": "0",
        "ICYPos": "0",
        "ResponsetoDiffFrame": "-1",
        "TargetFrameName": "None",
        "FacetPath": "None",
        "ICFocus": "",
        "ICSaveWarningFilter": "0",
        "ICChanged": "0",
        "ICSkipPending": "0",
        "ICAutoSave": "0",
        "ICResubmit": "0",
        "ICSID": str(iscid),
        "ICAGTarget": "true",
        "ICActionPrompt": "false",
        "ICBcDomData": "C~UnknownValue~EMPLOYEE~SA~NUI_FRAMEWORK.PT_LANDINGPAGE.GBL~PT_LANDINGPAGE~Student Homepage~UnknownValue~UnknownValue~https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL?~UnknownValue*C~UnknownValue~EMPLOYEE~SA~PT_FLDASHBOARD.PT_FLDASHBOARD.GBL~PT_LANDINGPAGE~Academics~UnknownValue~UnknownValue~https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/PT_FLDASHBOARD.PT_FLDASHBOARD.GBL?DB=WSA_ACADEMICS~UnknownValue*C~UnknownValue~EMPLOYEE~SA~NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL~PT_AGSTARTPAGE_NUI~Course Registration~UnknownValue~UnknownValue~https://student.uwo.ca/psc/heprdweb/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID%3aPTPPNAVCOL&scname=ADMN_MANAGE_MY_CLASSES&PTPPB_GROUPLET_ID=WSA_MANAGE_CLASSES&CRefName=ADMN_NAVCOLL_5&ptgpid=ADMN_S202205301002261020844141~UnknownValue",
        "ICDNDSrc": "",
        "ICPanelHelpUrl": "http://www.registrar.uwo.ca/general-information/how_to_guides/index.html",
        "ICPanelName": "",
        "ICPanelControlStyle": "pst_side1-fixed pst_panel-mode pst_side2-hidden",
        "ICFind": "",
        "ICAddCount": "",
        "ICAppClsData": "",
        "win0hdrdivPT_SYSACT_HELP": "",
        "DERIVED_SSR_FL_SSR_VW_CLSCHD_OPT$81$": "D"
    }

    endDateEndTimeData = str(s.post(postURL, data=postFormData).text)
    checkDates = str(s.post(postURL, data=checkCoursesFormData).text)

except Exception as e:
    print("Something went wrong\n")
    print(e)
    input("Press any button to quit.")
    quit()


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


# checkCoursesIndices = [m.start()
#                        for m in re.finditer("Class Details - ", textCheckCourses)]
# newLineIndicesCheckCourses = []

# checkCourses = []

# for i in range(len(checkCoursesIndices)):
#     newLineIndicesCheckCourses.append(
#         textCheckCourses[textCheckCourses[i]::].find("\n"))

#     checkCourses.append(
#         textCheckCourses[textCheckCourses[i]: newLineIndicesCheckCourses[i]])

# checkCourses = list(set(checkCourses))

# print(checkCourses)


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


# for i in range(len(courseName)):
#     courseName[i] = str(courseName[i].split(" ")[
#         0]) + " " + str(courseName[i].split(" ")[1]) + " " + str(courseName[i].split(" ")[4])

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
