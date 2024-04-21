# -*- coding:utf-8 -*-
import heapq
import re
import pandas as pd
from keybert import KeyBERT
from ckip_transformers.nlp import CkipWordSegmenter
from os import name
from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch


df = pd.read_excel("SDGs_keywords.xlsx", header=1)
SDG_no = list(df['SDG NO'])
SDG_no = [int(str(i).split(' ')[1]) for i in SDG_no]
SDG_weight = list(df['Weight'])
SDG_weight = [float(i) for i in SDG_weight]
SDG_en = list(df['Key phrase'])
SDG_en = [str(i) for i in SDG_en]
SDG_zh = list(df['關鍵字'])
SDG_zh = [str(i) for i in SDG_zh]
SDG_categories = ['消除貧窮', '終結飢餓', '健康與福祉',
                  '優質教育', '性別平權', '潔淨水資源', '可負擔能源', '良好工作與經濟成長',  '工業化、創新及基礎建設', '消弭不平等', '永續城鄉', '責任消費與生產循環', '氣候變遷對策', '海洋生態', '陸域生態', '公平、正義與和平']

# ws_driver = torch.load('./model/ws_driver.pkl')
# ch_kw_model = torch.load('./model/ch_kw_model.pkl')
# en_kw_model = torch.load('./model/en_kw_model.pkl')
# ch_st_model = torch.load('./model/ch_st_model.pkl')
# en_st_model = torch.load('./model/en_st_model.pkl')


def get_similarity(text, lang):
    if lang == "en":
        SDG = get_en_similar(text)
    elif(lang == "zh"):
        SDG = get_zh_similar(text)
    return SDG


def get_en_similar(all_kw_list):
    # en_st_model = SentenceTransformer('paraphrase-mpnet-base-v2')
    en_st_model = torch.load('./model/en_st_model.pkl')
    # Encode all sentences
    embeddings = en_st_model.encode(SDG_en)
    paragraphSDG = [0]*16

    tmp_embedding = en_st_model.encode(
        [i[0] for i in all_kw_list])
    sim = util.pytorch_cos_sim(tmp_embedding, embeddings)
    sim = sim.detach().numpy()
    for j, i in enumerate(sim):
        max_pos = np.argmax(i)

        # 不考慮關鍵字權重
        paragraphSDG[SDG_no[max_pos] -
                     1] += SDG_weight[max_pos]+10 if(i[max_pos] > 0.7) else 0

        # 考慮關鍵字權重
        # paragraphSDG[SDG_no[max_pos]-1] += all_kw_list[j][1] * \
        #     (SDG_weight[max_pos]+10) if(i[max_pos] > 0.7) else 0

        # print(all_kw_list[j], SDG_en[max_pos], round(i[max_pos], 6))

    return paragraphSDG


def get_zh_similar(all_kw_list):
    # ch_st_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    ch_st_model = torch.load('./model/ch_st_model.pkl')

    # Encode all sentences
    embeddings = ch_st_model.encode(SDG_zh)
    paragraphSDG = [0]*16

    tmp_embedding = ch_st_model.encode([i[0] for i in all_kw_list])
    sim = util.pytorch_cos_sim(tmp_embedding, embeddings)
    sim = sim.detach().numpy()
    for j, i in enumerate(sim):
        max_pos = np.argmax(i)

        # 不考慮關鍵字權重
        paragraphSDG[SDG_no[max_pos] -
                     1] += SDG_weight[max_pos] if(i[max_pos] > 0.7) else 0

        # 考慮關鍵字權重
        # paragraphSDG[SDG_no[max_pos]-1] += all_kw_list[j][1] * \
        #     (SDG_weight[max_pos]+10) if(i[max_pos] > 0.7) else 0

        # print(all_kw_list[j], SDG_zh[max_pos], round(i[max_pos], 6))

    return paragraphSDG


def get_en_keywords(text):
    # en_kw_model = KeyBERT('paraphrase-mpnet-base-v2')
    en_kw_model = torch.load('./model/en_kw_model.pkl')
    text = [i.strip() for i in text.split('.')]
    text = [i for i in text if len(i) > 0]
    all_kw_list = []
    for d in text:
        all_kw_list.extend(en_kw_model.extract_keywords(
            d, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=len(d)//50+1))
    # df = pd.DataFrame(keywords, columns=['Keyword', 'Rate'])
    all_kw_list = [i for i in all_kw_list if len(i) > 0]
    return all_kw_list


def get_zh_keywords(text):
    # ws_driver = CkipWordSegmenter(level=1)
    # ch_kw_model = KeyBERT('distiluse-base-multilingual-cased-v2')
    ws_driver = torch.load('./model/ws_driver.pkl')
    ch_kw_model = torch.load('./model/ch_kw_model.pkl')
    stoplist_path = r"中文分隔詞詞庫.txt"
    with open(stoplist_path, 'rb') as fp:
        tmp = fp.read().decode('utf-8')
    stoplist = tmp.splitlines()

    all_kw_list = []
    ws = ws_driver(re.split('。|\n', text))
    ws = [w for w in ws if len(w) > 0]
    data = [' '.join(i) for i in ws]
    all_kw_list = []
    for d in data:
        all_kw_list.extend(ch_kw_model.extract_keywords(
            d, keyphrase_ngram_range=(1, 1), stop_words=stoplist, top_n=len(d)//30+1))

    all_kw_list = [i for i in all_kw_list if len(i) > 0]
    return all_kw_list


def get_keywords(text, lang='en'):
    if(lang == 'en'):
        all_kw_list = get_en_keywords(text)
    elif(lang == 'zh'):
        all_kw_list = get_zh_keywords(text)
    return all_kw_list


if __name__ == "__main__":
    text = """為促進畜產資源合作及永續經營，台糖公司於今(16)日上午假台糖總管理處舉辦與農委會畜試所合作備忘錄(MOU)簽署儀式，儀式由台糖總經理王國禧主持，並與農委會畜試所所長黃振芳在雙方成員共同見證下，正式簽署合作備忘錄。未來台糖與畜試所將攜手於飼料、肉品加工及智慧農業的技術交流上深化合作，秉持「畜產等於續產」理念，共同為臺灣畜牧業國際競爭力及永續發展增添助力與新量能。

台糖表示，台糖與畜試所資源互補性高，雙方簽訂MOU不僅達到互惠之加乘效果，更是促進畜產業轉型升級的大利多。台糖擁有垂直整合飼料、養殖、

肉品加工的經驗及場域優勢，結合畜試所充沛的研發與技術能量，共同組成研究團隊，聚焦「飼料配方」(精準營養、減廢飼料及在地化替代飼料)、「肉品加工」(外銷目標與屠體評級)，以及「智慧農業」(農機與自動化系統)等項目，盼能胼手新創畜產、聯合締造農發，為畜牧產業轉型迎來新契機。

台糖指出，養豬一直是公司的核心事業，畜牧永續發展更是願景目標。近年公司將「循環經濟」與「新農業」落實到養豬事業已展現成果，去年全球畜殖業第一座BSI認證的「台糖東海豐農業循環園區」正式啟用，轄下豬場現代化改建工程也正如火如荼進行中。台糖率先建立標竿典範，也盼更多專業夥伴一起加入，加速國內畜殖產業的轉型升級，今與畜試所攜手合作，互惠共享畜產資源及技術外，未來創新研發成果也有助於提升整體競爭力。

台糖補充，本次MOU合作範圍除飼料、肉品、智慧農業項目外，也擴及經驗與技術交流、學術資料交流、教育推廣、資源互惠，以及畜產學術推展等六大範疇，有助於未來雙方共同爭取政府研究計畫及產學合作計畫，並共享智慧財產研發成果，為臺灣畜產業的創新加值及永續經營驅動更高量能、拓展更遠鵬程。"""

    LANG = 'zh'

    all_kw_list = get_keywords(text, LANG)
    print("------------KEYWORDS EXTRACT------------")
    df = pd.DataFrame(all_kw_list, columns=['Keyword', 'Rate'])
    print(df)
    paragraphSDG = get_similarity(all_kw_list, LANG)
    print("------------GET SIMILARITY------------")
    max_SDG_index_list = list(map(
        paragraphSDG.index, heapq.nlargest(16, paragraphSDG)))

    for i in max_SDG_index_list:
        if paragraphSDG[i] == 0:
            break
        print(
            f"SDG: {i+1:1d}{'('+SDG_categories[i]+')':10}   weight = {paragraphSDG[i]:.4f}")
    print("done")
