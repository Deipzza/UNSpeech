import requests
from bs4 import BeautifulSoup



def get_calendar(student):
    
    URL = "https://registroymatricula.medellin.unal.edu.co"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    URL=soup.find("img",attrs ={"alt":f"Banner calendario acadmico {student}"}).parent["href"]
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    table = soup.find_all("table",attrs ={"class":"MsoNormalTable"})
    content = table[0].find("tbody")

    result = ""
    for row in content.find_all("tr"):
        cells=row.findAll("td")
        if len(cells)>2:
            act=cells[0].find("p").text
            date=cells[1].find("p").text
            result+=f"{act} --- {date} \n"
    return result