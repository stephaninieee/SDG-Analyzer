import requests
from bs4 import BeautifulSoup
import csv

csvfile = open('article.csv', 'w',encoding='UTF-8')
writer = csv.writer(csvfile, delimiter='\t')
writer.writerow(['tag', 'article'])

for page in range(1,20):
   link = "https://ncsd.ndc.gov.tw/fore/News?NewsPage="+str(page)+"&ActPage=1&Type=5"
   resp = requests.get(link)
   print(resp) #<Response [200]> 請求成功回200，請求失敗回404


   soup = BeautifulSoup(resp.text, 'html.parser')
   #整張HTML
   #print(soup)
   title_tag = soup.title
   print(title_tag)
   url = soup.find_all("a","card-title h5")
   tag = soup.find_all("div","color1234")

   #取得tag
   list=[]
   new_list=[]
   for t in tag:
      #print(t.text)
      list.append(t.text)
   for x in list:
      y=x.maketrans("\n", " ", "淨")
      new_list.append(x.translate(y))

   #取得文章內容   
   j=0
   for item in url:
      #print("標題：" + item.text)
      a = "https://ncsd.ndc.gov.tw" + item.get('href')
      article = requests.get(a)
      print(article)
      soup_s = BeautifulSoup(article.text, 'html.parser')
      context = soup_s.find_all("p")
      tmp=""
      for i in context:
         #print(i.text)
         tmp+=i.text
      writer.writerow([new_list[j],tmp])
      j+=1


# 輸出排版後的 HTML 程式碼
#print(soup.prettify())