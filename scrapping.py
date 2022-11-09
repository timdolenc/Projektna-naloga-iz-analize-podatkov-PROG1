"""Program ob zagonu pobere frontpage in tabe"""

import os
import re


#SELENIUM##########################################
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
DRIVER_PATH = '/path/to/chromedriver'
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
####################################################

# LINKI#############################################
directory_frontpages = "/Users/timdolenc/Desktop/PROGRAMIRANJE/programiranje-1/PROJEKT_ANALIZA_PODATKOV/frontpages"
directory_tabs = "/Users/timdolenc/Desktop/PROGRAMIRANJE/programiranje-1/PROJEKT_ANALIZA_PODATKOV/tabs"
####################################################



def download_url_to_string_selenium(url):
    driver.get(url)
    vsebina = driver.page_source
    return vsebina

def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename) #združiš direktorij z imenom datoteke da nerabiš posebi lepit
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
        print(f"{filename} shranjena")
    return None


def save_page(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    vsebina = download_url_to_string_selenium(page)
    save_string_to_file(vsebina, directory, filename)

def save_frontpages_and_tabs(od_strani, do_strani): #tukaj sem bil v dilemi ali naj naredim dve različni funkciji, eno da shrani frontpage in drugo da shrani tabse (iz shranjenih datotek frontpagov), ampak sem se odločil... prav tako sem
    """Shrani vsebino prvih 'do_strani' strani v datoteke z imenom 
    'frontpage_i' za i-to stran, na vsaki strani je 50 tabov"""

    for stran_št in range(od_strani, do_strani + 1):
        url_frontpage = f"https://www.ultimate-guitar.com/explore?order=hitstotal_desc&page={stran_št}&type[]=Chords"
        ime_datoteke_frontpage = f"frontpage_{50*stran_št+1}-{50*stran_št+50}.html"

        vsebina = download_url_to_string_selenium(url_frontpage) #tu funkcijo shrani stran v datoteko razbijem na dva dela, saj potrebujem vsebino 
        save_string_to_file(vsebina, directory_frontpages, ime_datoteke_frontpage)

        vzorec_url_taba = r'<a class="aPPf7 HT3w5 lBssT" href="(?P<url_taba>.+?)">(?P<naslov>.+?)<'
        for pojavitev in re.finditer(vzorec_url_taba, vsebina):
            pesem = pojavitev.groupdict()
            naslov = pesem["naslov"]
            url_taba = pesem["url_taba"]
            ime_datoteke_tab = f"{naslov}.html"
            save_page(url_taba, directory_tabs, ime_datoteke_tab)


if __name__ == '__main__': 
    save_frontpages_and_tabs(41, 200)


