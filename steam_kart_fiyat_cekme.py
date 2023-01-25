import time
import config
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from requests.cookies import RequestsCookieJar
sessionid=config.sessionid
steamLoginSecure=config.steamLoginSecure
listealinacak=[]
cookies_dict ={
    "steamLoginSecure":steamLoginSecure,
    "sessionid":sessionid,
}

cookies = RequestsCookieJar()
cookies.update(cookies_dict)
response = requests.get("https://steamcommunity.com/id/Airr_Hub/gamecards/730?curator_clanid=4777282&utm_source=SteamDB", cookies=cookies)
soup = BeautifulSoup(response.content, "html.parser")
listeson=[]
def oyunfiyat(x2):
    x2 = str(x2)
    api_key = "4DE135D9940885940F16FD17C9A19D41"
    app_id = x2
    url = f"http://store.steampowered.com/api/appdetails?appids={app_id}&cc=tr&l=tr&v=1&key={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        price = data[app_id]["data"]["price_overview"]["final"]
        fiyat = float(price)
        O_fiyat = fiyat / 100
        O_fiyat = str(O_fiyat)
        O_fiyats = O_fiyat.replace(".", ",")
    except:
        print("fiyati yok")
        return 0
        pass
    return O_fiyats


def increment_if_odd(number):
    if number % 2 == 1:
        number += 1
        # print("toplam_kart",number,"dusucek kart",number / 2)
    return number / 2


def sorgulama(x):
        x1 = str(x)
        url = "https://steamcommunity.com/id/Airr_Hub/gamecards/" + x1
        istek = requests.get(url, cookies=cookies)
        html_content = istek.content
        soup = BeautifulSoup(html_content, "lxml")
        bads = soup.find("div", attrs={"class": "badges_sheet"})
        if bads == None:
            a=1
        else:
            return "/NOF"
        try:
            links1 = soup.find("div", attrs={"class": "badge_cards_to_collect"})
            links2 = links1.find("div", attrs={"class": "gamecards_inventorylink"})
            link = links2.find('a')['href']
            response = requests.get(link, cookies=cookies)
            soup2 = BeautifulSoup(response.content, 'lxml')
            kart_E = soup2("input", attrs={"class": "market_dialog_input market_multi_price"})
            liste = []
            for kart in kart_E:
                value = kart["value"]
                value1 = value[:-3]
                value1 = value1.replace(",", ".")
                a2 = float(value1)
                liste.append(a2)
            kart_fiyat = min(liste) * int(increment_if_odd(len(liste)))
            askart = "{:.2f}".format(kart_fiyat)
            askart = str(askart)
            return askart.replace(".", ",")
        except:
            print("K-bilgi-yok")
            time.sleep(1)
            sorgulama(x)

g= 0
def start_main():

    print("kart hesaplama basliyor")
    start_time = datetime.now()
    df = pd.read_excel("C:/Users/kadir/Desktop/STEAM_ID.xlsx")
    def fonksiyon(id):
        global g
        g = g + 1
        x_str = str(id)
        sonuc0 = sorgulama(x_str)
        sonuc1=oyunfiyat(x_str)

        asd0 = str(sonuc0)
        asd1= str(sonuc1)
        return asd1+"/"+asd0

    # df['Oyun'] = df["id"].apply(oyunfiyat)
    df["oyun_F"] = df["id"].apply(fonksiyon)
    df.to_excel("C:/Users/kadir/Desktop/STEAM_ID.xlsx", index=False)
    end_time = datetime.now()
    sure = end_time-start_time

    print("top_saniye", int(sure.total_seconds()))
    print("islenen_veri", g)
    print(int(sure.total_seconds())/g, "saniyede_bir_ID")
    # os.os.system("shutdown /s /t 1")

def teklisorgu(x):
    oyun = oyunfiyat(x)
    oyun = str(oyun)
    oyun = oyun.replace(",", ".")
    oyun = float(oyun)
    kart = sorgulama(x)
    kart = str(kart)
    kart = kart.replace(",", ".")
    # if kart=="/NOF":
    #     return "kartbilgisiyok",x
    try:
        kart = float(kart)
    except:
        return "kartbilgisiyok",x
    sonuc0 = kart-oyun
    if sonuc0 >= 0.3:
        print(x,sonuc0)
        listealinacak.append(x)
        return round(sonuc0)
    else:
        a=1
start_time=datetime.now()
print(start_time)
with open("ilk_IDs.txt", "r") as dosya:
   for id1 in dosya:
        id1 = int(id1)
#print(id1)
        teklisorgu(id1)
dosya.close()


fin_time=datetime.now()
dosya = open("alinacak_ID.txt", "w")
for i in listealinacak:

        dosya.write(str(i)+"\n")
dosya.close()
print(len(listealinacak),"yazdirildi")

print(listealinacak,fin_time-start_time)
import id_sepet_add