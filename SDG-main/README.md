# SDG Analyze

## 提取關鍵字

- 中文：
  - 先使用[CKIP Transformers](https://ckip.iis.sinica.edu.tw/service/transformers/)做斷詞
  ```python=
  from ckip_transformers.nlp import CkipWordSegmenter
  ws_driver = CkipWordSegmenter(level=3)
  swtext = ws_driver(text)
  ```
  - 將斷詞結果送入[KeyBERT](https://maartengr.github.io/KeyBERT/)，進行關鍵字萃取，取前 25 個
    - model：**distiluse-base-multilingual-cased-v1**
    - stop_words：**"./stoplist/中文分隔詞詞庫.txt"**
    - :::success
      ```python=
        extract_keywords(self,
             docs: Union[str, List[str]],
             candidates: List[str]=None,
             keyphrase_ngram_range: Tuple[int, int]=(1, 1),
             stop_words: Union[str, List[str]]='english',
             top_n: int=5,
             min_df: int=1,
             use_maxsum: bool=False,
             use_mmr: bool=False,
             diversity: float=0.5,
             nr_candidates: int=20,
             vectorizer: CountVectorizer=None,
             highlight: bool=False)
      ```
      **參數：**
      **docs**：要提取關鍵字/關鍵短語的文檔
      **candidates**：要使用的候選關鍵字/關鍵短語，而不是從文檔中提取它們
      **keyphrase_ngram_range**：提取的關鍵字/關鍵短語的長度（以字為單位）
      **stop_words**：要從文檔中刪除的停用詞
      **top_n**：返回前 n 個關鍵字/關鍵短語
      **min_df**：如果需要提取多個文檔的關鍵字，則一個單詞在所有文檔中的最小文檔頻率
      **use_maxsum**: 是否使用 Max Sum Similarity 來選擇 keywords/keyphrases
      **use_mmr**：是否使用最大邊際相關性（MMR）進行關鍵字/關鍵短語的選擇
      **diversity**：如果 use_mmr 設置為 True，結果的多樣性在 0 和 1 之間
      **nr_candidates**：如果 use_maxsum 設置為 True，要考慮的候選數
      **vectorizer**：從 scikit-learn 傳入你自己的 CountVectorizer
      **highlight**：是否列印文檔並突出顯示其關鍵字/關鍵短語。註意：如果傳遞了多個文檔，這將不起作用。
      :::
    - [教程](https://blog.csdn.net/chenhepg/article/details/118571671)
- 英文：
  - KeyBERT model：**paraphrase-mpnet-base-v2**

## SDG 分類

根據 **"./SDGs_keywords.xlsx"**，將得出來的關鍵字使用[SentenceTransformer](https://github.com/UKPLab/sentence-transformers)進行比對，得出各關鍵字相應的 SDG 分類

- 步驟：
  1. Load Model：
     ```python=
     from sentence_transformers import SentenceTransformer, util
     model = SentenceTransformer('paraphrase-mpnet-base-v2')    #英文
     # model = SentenceTransformer('distiluse-base-multilingual-cased-v2') #中文
     ```
  2. word embedding：
     ```pyhton=
     embeddings = model.encode(SDG)    #SDG分類
     ans_embed = model.encode(ans)     #輸入的關鍵字
     ```
  3. 計算相似度：用 cos_similarity
     ```python=
     cos_sim = util.pytorch_cos_sim(ans_embed, embeddings)
     ```
  4. 根據相似度進行排序，回傳相似度最高的 SDG 分類

## 網頁呈現

- 圖表：使用 Highcharts
  - [教程](https://www.runoob.com/highcharts/highcharts-tutorial.html)
- 文字編輯器：ckeditor`

## 程式碼

### python

#### keywords .py

- 英文：
  ![](https://i.imgur.com/kWHwOcb.png)

- 中文：
  ![](https://i.imgur.com/Jp8OsCX.png)
