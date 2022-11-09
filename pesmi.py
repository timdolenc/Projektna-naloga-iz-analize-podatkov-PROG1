import os
import re

# LINKI#############################################
directory_frontpages = "/Users/timdolenc/Desktop/PROGRAMIRANJE/programiranje-1/PROJEKT_ANALIZA_PODATKOV/frontpages"
directory_tabs = "/Users/timdolenc/Desktop/PROGRAMIRANJE/programiranje-1/PROJEKT_ANALIZA_PODATKOV/tabs"
####################################################

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz."""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding="utf8") as f:
        vsebina = f.read()
    return vsebina

vzorec_osnovnih_podatkov = re.compile(
    r'<h1 class="dUjZr">(?P<naslov>.+?) Chords</h1>.*?'
    r'<a class="aPPf7 fcGj5" href=".*?">(?P<izvajalec>.+?)</a>.*?'
    r'<div class="_apVM">(?P<kliki>.*?) views',
    #r'<td class="IcoWj"><span>(?P<tezavnost>.*?)</span></td>',
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
    #akordi = [akord.group(1) for akord in re.finditer(vzorec_akorda, vsebina)]
    #slovar["akordi"]
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
    for i, tab_datoteka in enumerate(listdir_nohidden(directory_tabs)):
        tab_slovar = izloči_podatke_iz_tab_datoteke(directory_tabs, tab_datoteka)
        sez.append(tab_slovar)
        if i == n-1:
            break
    return sez

        
        
slovar = izloči_podatke_iz_vseh_tab_datotek()

print(slovar)
print(len(slovar))

print(None in slovar)










        








