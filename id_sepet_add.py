import time
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
driver1 = webdriver.Chrome()
liste = []

with open("alinacak_ID.txt", "r") as dosya:
   for id1 in dosya:
        id1 = int(id1)
        liste.append(id1)
dosya.close()


def sepete_ekle(id):

    url = "https://store.steampowered.com/app/{}".format(id)
    driver1.get(url)
    try:
        driver1.find_element(By.CLASS_NAME, "btn_addtocart").click()
    except:
        driver1.find_element("xpath", "//*[@id='ageYear']/option[9]").click()
        driver1.find_element("xpath", "//*[@id='view_product_page_btn']").click()
        time.sleep(2)
        driver1.find_element(By.CLASS_NAME, "btn_addtocart").click()


def buy():
    driver1.find_element("xpath", "//*[@id='btn_purchase_self']").click()
    time.sleep(5)
    driver1.find_element("xpath",
                         "//*[@id='responsive_page_template_content']/div/div[2]/div/div/div/div[2]/div/form/div[1]/input").send_keys(
        config.steam_user)
    driver1.find_element("xpath",
                         "//*[@id='responsive_page_template_content']/div/div[2]/div/div/div/div[2]/div/form/div[2]/input").send_keys(
        config.steam_pass)
    driver1.find_element("xpath",
                         "//*[@id='responsive_page_template_content']/div/div[2]/div/div/div/div[2]/div/form/div[4]/button").click()
    print("onay bekleniyor")
    a = False
    a0 = 0
    while a == False:
        try:
            driver1.find_element("xpath", "//*[@id='accept_ssa']").click()
            a = True
        except:
            if a0 == 0:
                print("izin ver lan")
            time.sleep(2)
            a0 = a0+1

    driver1.find_element("xpath", "//*[@id='purchase_button_bottom_text']").click()
    print("satin alim basarili")
    driver1.close()


def start_main():
    for id0 in liste:
        sepete_ekle(id0)

    print("basari ile oyunlar sepete eklendi")

    if int(input("oyunlar satin almak icin 1 e basin\n")) == 1:
        buy()
    else:
        print("oyunlar sadece eklendi")

if len(liste) == 0:
    print("liste bos")
else:
    start_main()

driver1.close()