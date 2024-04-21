import requests
from bs4 import BeautifulSoup
import csv

# SDG_list = ['no-poverty','zero-hunger','good-health-and-well-being','quality-education','gender-equality','clean-water-and-sanitation',]

csvfile = open('output.csv', 'w',encoding='UTF-8',newline='')
#open csv file
writer = csv.writer(csvfile)

# 寫入首列資料
writer.writerow(["SDG_NO","NAME","Title","Content","Link"])


root_response = requests.get(
    "https://2030.sdg.ncku.edu.tw/project/")

root_soup = BeautifulSoup(root_response.text, "html.parser")

SDG_list = []
for i in root_soup.find_all(class_="sdg_item"):
    SDG_list.append(i.select_one("a").get("href"))
# print(SDG_list)

for SDG_no,link in enumerate(SDG_list):
    print("doing SDG",SDG_no+1)
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    # print()
    SDG_name = link.split('/')[-1]
    Max_page = int(soup.find_all(class_ = "page-numbers")[-2].get_text()) if len(soup.find_all(class_ = "page-numbers"))>1 else 1
    # print(Max_page)
    all_article = []
    for page in range(Max_page):
        response = requests.get(f'{link}/page/{page+1}')
        soup = BeautifulSoup(response.text, "html.parser")
        all_article.extend(soup.find_all(class_="project_item"))
    for i in all_article:
        title = i.select_one("a").find(class_="title_en").get_text()
        link = i.select_one("a").get("href")
        response = requests.get(f'{link}/page/{page+1}')
        soup = BeautifulSoup(response.text, "html.parser")
        paragraph = soup.find(class_="article").find_all("p")
        text = ''
        for line in paragraph:
            text=text+line.get_text(strip=True)+'\n'
        # print(title)
        # print(link)
        # print()

        print(text)
        writer.writerow([SDG_no+1,SDG_name,title,text,link])
