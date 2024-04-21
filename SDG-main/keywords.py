# This Python file uses the following encoding: utf-8
import pandas as pd
from keybert import KeyBERT
from ckip_transformers.nlp import CkipWordSegmenter


def get_en_keywords(text):
    kw_model = KeyBERT('paraphrase-mpnet-base-v2')
    keywords = kw_model.extract_keywords(
        text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=25)
    df = pd.DataFrame(keywords, columns=['Keyword', 'Rate'])
    return df


def get_zh_keywords(text):
    ws_driver = CkipWordSegmenter(level=3)
    kw_model = KeyBERT('distiluse-base-multilingual-cased-v1')
    stoplist_path = "./stoplist/中文分隔詞詞庫.txt"
    with open(stoplist_path, 'rb') as fp:
        tmp = fp.read().decode('utf-8')
    stoplist = tmp.splitlines()

    tmp_text = [str(text)]
    swtext = ws_driver(tmp_text)
    for i in swtext:
        print(i)
    data = ' '. join(swtext[0])
    print("len:::",len(swtext))
    print("datais:::::", data)
    keywords = kw_model.extract_keywords(
        data, keyphrase_ngram_range=(1, 1), stop_words=stoplist, top_n=25)
    df = pd.DataFrame(keywords, columns=['Keyword', 'Rate'])
    return df


def get_keywords(text, lang):
    if(lang == 'en'):
        df = get_en_keywords(text)
        return df
    elif(lang == 'zh'):
        df = get_zh_keywords(text)
        return df


if __name__ == "__main__":
    text = "1 導論：教學⽬標、課程 介紹與上課基本要求 劉阿榮（2014）〈⽂創Ԣ業與通識教育〉載劉阿榮、洪泉湖主 編：《⽂化、創意與教育》，台北：師⼤書苑，⾴1-18 2 ⽂創Ԣ業與公民美學的意 涵及相關概念 李天鐸（2012）《⽂化創意Ԣ業讀本》，台北遠流，⾴19-35 3 ⽂創Ԣ業的發展與演變： 從負⾯到中性，再到正 向意義 林炎旦主編（2011）《⽂化創意Ԣ業：理論與實務》台北：師⼤ 書苑，第2章 4 ⽂創Ԣ業的全球視野：歐 美、東亞主要國家地區 的概況 李天鐸（2012）《⽂化創意Ԣ業讀本》，台北遠流，⾴19-35陳 德富（2016）《⽂化創意Ԣ業經營與⾏銷管理》，台北揚智，⾴ 60-120 3/4 5 我國「⽂創Ԣ業政策與法 規」介紹 學⽣就「⽂化Ԣ業發展法」（⽂化部）及「Ԣ業創新條例」（經濟部） 寫800字⼼得報告 6 「⽂化Ԣ業園區」簡介與⽐ 較：華⼭/松菸/北京七 九⼋ 上網蒐集資料或實地參訪並作⼩組報告 7 傳統⽂化Ԣ業：陶瓷、崑 曲及其他 上網蒐集資料或實地參訪並作⼩組報告 8 流⾏⽂化Ԣ業：動漫、影 視⽂創Ԣ業 上網蒐集資料或實地參訪並作⼩組報告 9 期中考試週 10 專題演講題⽬及講員待確定 11 藝術遇上經濟：⽂創Ԣ業 的⾏銷與管理 陳德富（2016）《⽂化創意Ԣ業經營與⾏銷管理》，台北揚智， ⾴386-412 12 創意、設計與消費典藏 （東⽅⽂物舉例） 上網蒐集資料或拍賣典藏專刊⼩組報告 13 創意、設計與消費典藏 （西洋⽂物舉例） 上網蒐集資料或拍賣典藏專刊⼩組報告 14 從社區營造到⽣活美學陳其南（2004）〈公民美學運動在台灣〉《書⾹遠傳》第15期。 15 美學想像與在地美學的 建⽴ 陳懷恩（2011）〈台灣社會的美學想像與在地美學的建⽴〉 《成⼤研發快訊》20卷第1期 16 ⽂化意識與⽣活美學劉阿榮（2012）〈⽂化意識與⽣活美學：差異或趨同〉，台北 商⿍數位出版，⾴1-23 17 調整進度與課程統整 18 期末考試週"

    df = get_keywords(text, "zh")
    print(df)
