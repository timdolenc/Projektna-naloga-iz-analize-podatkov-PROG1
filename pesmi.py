import os
import re
import csv

# LINKI#############################################
directory = "/Users/timdolenc/Desktop/PROGRAMIRANJE/programiranje-1/PROJEKT_ANALIZA_PODATKOV"
directory_frontpages = "/Users/timdolenc/Desktop/PROGRAMIRANJE/programiranje-1/PROJEKT_ANALIZA_PODATKOV/frontpages"
directory_tabs = "/Users/timdolenc/Desktop/PROGRAMIRANJE/programiranje-1/PROJEKT_ANALIZA_PODATKOV/tabs"
####################################################

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz."""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding="utf8") as f:
        vsebina = f.read()
    return vsebina

def kliki_to_int(str):
    """pretvori št. klikov v ustrezno obliko"""
    return int("".join(str.split(",")))

vzorec_osnovnih_podatkov = re.compile(
    r'<h1 class="dUjZr">(?P<naslov>.+?) Chords</h1>.*?'
    r'<a class="aPPf7 fcGj5" href=".*?">(?P<izvajalec>.+?)</a>',
    flags=re.DOTALL
)

vzorec_kliki = re.compile(
    r'<div class="_apVM">(?P<kliki>.*?) views',
    flags=re.DOTALL
)

vzorec_težavnosti = re.compile(
    r'<td class="IcoWj"><span>(?P<tezavnost>.*?)</span></td>',
    flags=re.DOTALL
)

vzorec_akorda = re.compile(
    r'<header class="Ufuqr"><span class="">(?P<akord>.*?)</span></header>',
    flags=re.DOTALL
)

def izloči_podatke_iz_tab(vsebina):
    match = re.search(vzorec_osnovnih_podatkov, vsebina)
    slovar = match.groupdict()
    match_težavnost = re.search(vzorec_težavnosti, vsebina)
    if not match_težavnost:
        print(f"Tab: {slovar['naslov']} - {slovar['izvajalec']} je neustrezen, zato je izločen.") #nekateri tabi niso na voljo zaradi avtorskih pravic
        return None

    slovar["kliki"] = kliki_to_int(re.search(vzorec_kliki, vsebina).group("kliki"))
    slovar["tezavnost"] = match_težavnost.group("tezavnost")
    

    akordi = [akord.group(1) for akord in re.finditer(vzorec_akorda, vsebina)]
    slovar["akordi"] = akordi
    return slovar
    
def izloči_podatke_iz_tab_datoteke(directory, filename):
    vsebina = read_file_to_string(directory, filename)
    return izloči_podatke_iz_tab(vsebina)
    

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def izloči_podatke_iz_vseh_tab_datotek(n=5000):
    sez = []
    neustrezni = 0
    for i, tab_datoteka in enumerate(listdir_nohidden(directory_tabs)):
        tab_slovar = izloči_podatke_iz_tab_datoteke(directory_tabs, tab_datoteka)
        if tab_slovar == None:
            neustrezni += 1
        else:
            sez.append(tab_slovar)
        if i == n-1:
            break
    return sez, neustrezni

def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return     
        
slovar, neustrezni = izloči_podatke_iz_vseh_tab_datotek(100)
fieldnames = ["naslov", "izvajalec","kliki","tezavnost", "akordi"]

write_csv(fieldnames, slovar, directory, "tabs.csv")

print(slovar)
print(len(slovar))
print(neustrezni)










        








