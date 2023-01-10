from bs4 import BeautifulSoup


def getICSID(htmldoc):
    soup = BeautifulSoup(htmldoc, "html.parser")
    return (str(soup.find(id="ICSID").get("value")))
