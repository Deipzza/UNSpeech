import requests
from bs4 import BeautifulSoup

def get_academic_calendar(student):
    URL = "https://minas.medellin.unal.edu.co/tramitesestudiantiles/calendarios/calendario-academico-sede-medellin.html"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    links = soup.find_all("li")

    for link in links:
        try:
            anchor = link.find("a").text
            if (("CALENDARIO ACADÉMICO 2023-1S" in anchor) and (f"{student.upper()}" in anchor)):
                URL = link.find("div").find("a")["href"]
                r = requests.get(URL)
                soup = BeautifulSoup(r.content, 'html5lib')
                scrapTable = True

                if ("MODIFICACIÓN" in anchor):
                    scrapTable = False
                    modif = soup.find_all("span")

                    for span in modif:
                        if ("calendario del periodo académico 2023-1S" in span.text):
                            scrapTable = True
                            break

                if (scrapTable):
                    table = soup.find_all("table",attrs ={"class":"MsoNormalTable"})
                    content = table[0].find("tbody")

                    result = ""

                    for row in content.find_all("tr"):
                        print("hola2")
                        cells=row.findAll("td")

                        if len(cells)>2:
                            act=cells[0].find("p").text
                            date=cells[1].find("p").text
                            result+=f"{act} --- {date} \n"
                    return result
                
        except:
            pass

def get_request_calendar(student):
    URL = "https://registroymatricula.medellin.unal.edu.co"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    URL=soup.find("img",attrs ={"alt":f"Banner calendario acadmico {student}"}).parent["href"]
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    table = soup.find_all("table",attrs ={"class":"MsoNormalTable"})
    content = table[1].find("tbody")

    result = ""
    for row in content.find_all("tr"):
        cells=row.findAll("td")
        if len(cells)>3:
            number=cells[0].find("p").text
            act=cells[1].find("p").text            
            date=cells[2].find("p").text        
            if len(date) < 3:
                result+=f"{number}. {act}\n"
            else:
                result+=f"{number}. {act} --- {date}\n"
    return result