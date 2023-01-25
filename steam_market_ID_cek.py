# marifetname

import time
import config
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True

ID_sayisi = input("taranacak oyun sayisi=")
dongu_sayisi = input("dongu sayisi")
txtsorgu=input("txt icin 0\nexcel icin 1\n")
driver1 = webdriver.Chrome(options=options)
driver1.get("https://store.steampowered.com/")
# from webdriver_manager.chrome import ChromeDriverManager


sessionid = config.sessionid
steamLoginSecure = config.steamLoginSecure

driver1.add_cookie({'domain': 'store.steampowered.com', 'httpOnly': False, 'name': 'sessionid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': sessionid})
driver1.add_cookie({'domain': 'store.steampowered.com', 'expiry': 1708441729, 'httpOnly': True, 'name': 'steamLoginSecure', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': steamLoginSecure})

# options.add_argument('--headless')
# driver1 = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver1.get(
    'https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=10&category1=998&category2=29&filter=topsellers&ndl=1')
# driver1.refresh()



liste = []
listea = []
listeson = []
ID_sayisi = int(ID_sayisi)
dongu_sayisi = int(dongu_sayisi)

def listeye_yazdirson():
    wp_source2 = driver1.page_source
    soup2 = BeautifulSoup(wp_source2, 'html.parser')
    st1 = soup2.find("div", attrs={"id": "search_resultsRows"})
    tags = st1.find_all("a")
    for id in tags:
        id1 = id["data-ds-appid"]
        Kut_kontrol = id.find("div", attrs={"class": "ds_flag ds_owned_flag"})
        if Kut_kontrol == None:
            listeson.append(id1)
    print(len(listeson))

def downsorgu():
    for i in range(dongu_sayisi):
        driver1.execute_script("window.scrollBy(0,1000)", "")
        time.sleep(1)
    wp_source2 = driver1.page_source
    soup2 = BeautifulSoup(wp_source2, 'html.parser')
    st1 = soup2.find("div", attrs={"id": "search_resultsRows"})
    tags = st1.find_all("a")
    for id in tags:
        id1 = id["data-ds-appid"]
        Kut_kontrol = id.find("div", attrs={"class": "ds_flag ds_owned_flag"})
        if Kut_kontrol == None:
            liste.append(id1)
        else:
            pass
    listea = list(set(liste))
    print("toplam_ID==", len(listea))
    if len(listea) <= ID_sayisi:
        print("basa donuyor")
        downsorgu()
    else:
        listeye_yazdirson()

        if txtsorgu == 1:
            df = pd.read_excel("C:/Users/kadir/Desktop/STEAM_ID.xlsx")
            df["id"] = listeson
            df.to_excel("C:/Users/kadir/Desktop/STEAM_ID.xlsx", index=False)
        else:
            with open('ilk_IDs.txt', 'w') as f:
                for item in listeson:
                    f.write("%s\n" % item)
                print("yazdirildi")

#
downsorgu()
def txt_duzelt():


    dosya=open("ilk_IDs.txt", "r")
    dosya2=open("denedd2.txt","w")
    for id_K in dosya:
        id_K=id_K.replace(",","\n")
        dosya2.write(str(id_K) + "\n")
    dosya.close()
    dosya2.close()

    with open('denedd2.txt') as inputfile, open('ilk_IDs.txt', 'w') as outputfile:
        for line in inputfile:
            if not line.strip():
                continue
            outputfile.write(line)
    print("dosya duzeltildi")

txt_duzelt()
driver1.close()
import steam_kart_fiyat_cekme
