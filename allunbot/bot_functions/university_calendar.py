import requests
from bs4 import BeautifulSoup

def get_academic_calendar(student):
    URL = "https://minas.medellin.unal.edu.co/tramitesestudiantiles/calendarios/calendario-academico-sede-medellin.html"
    page_request = requests.get(URL)
    soup = BeautifulSoup(page_request.content, 'html5lib')
    collapses = soup.find_all("li")
    result = "Lo siento. No he podido encontrar esa información."

    for collapse in collapses:
        try:
            anchor = collapse.find("a").text
            if (("CALENDARIO ACADÉMICO 2023-1S" in anchor) and (f"{student.upper()}" in anchor)):
                URL = collapse.find("div").find("a")["href"]
                page_request = requests.get(URL)
                soup = BeautifulSoup(page_request.content, 'html5lib')
                scrapTable = True

                if ("MODIFICACIÓN" in anchor):
                    scrapTable = False
                    modif = soup.find_all("span")

                    for span in modif:
                        if ("calendario del periodo académico 2023-1S" in span.text):
                            scrapTable = True
                            break

                if (scrapTable):
                    table = soup.find_all("table", attrs = {"class": "MsoNormalTable"})
                    result = process_table(table[0], [0, 1])
                    return result
        except:
            pass

    return result

def get_request_calendar(student):
    URL = "https://minas.medellin.unal.edu.co/tramitesestudiantiles/calendarios/calendario-academico-sede-medellin.html"
    page_request = requests.get(URL)
    soup = BeautifulSoup(page_request.content, 'html5lib')
    collapses = soup.find_all("li")
    result = "Lo sentimos. No hemos podido encontrar esa información."

    for collapse in collapses:
        try:
            anchor = collapse.find("a").text
            if (("CALENDARIO ACADÉMICO 2023-1S" in anchor) and (f"{student.upper()}" in anchor) and "MODIFICACIÓN" not in anchor):
                URL = collapse.find("div").find("a")["href"]
                page_request = requests.get(URL)
                soup = BeautifulSoup(page_request.content, 'html5lib')
                table = soup.find_all("table", attrs = {"class": "MsoNormalTable"})
                result = process_table(table[1],[1,2])
                return result
        except:
            pass

    return result

def process_table(table, positions):
    
    content = table.find("tbody")
    result = ""
    count = 0

    for row in content.find_all("tr"):
        cells = row.findAll("td")

        if len(cells) > 2:
            activity = cells[positions[0]].find("p").text
            date = cells[positions[1]].find("p").text
            if (count == 0):
                result += f"No. | {activity} | {date}.\n\n"
            else:
                result += f"{count} | {activity} | {date}.\n\n"

            count += 1

    return result