from os import name
import pandas as pd
import json
import ast
from sentence_transformers import SentenceTransformer, util

df = pd.read_excel("SDGs_keywords.xlsx", header=1)
SDG_en = list(df['Key phrase'])
SDG_en = [str(i) for i in SDG_en]
SDG_zh = list(df['關鍵字'])
SDG_zh = [str(i) for i in SDG_zh]


def get_en_similar(text):
    model = SentenceTransformer('paraphrase-mpnet-base-v2')
    # ans = ast.literal_eval(text)
    ans = text.split(",")
    # Encode all sentences
    embeddings = model.encode(SDG_en)
    ans_embed = model.encode(ans)

    # Compute cosine similarity between all pairs
    cos_sim = util.pytorch_cos_sim(ans_embed, embeddings)

    # Add all pairs to a list with their cosine similarity score
    all_sentence_combinations = []
    for i in range(len(ans)):
        all_sentence_combinations.append([])
        for j in range(len(cos_sim[0])):
            all_sentence_combinations[i].append(
                [round(cos_sim[i][j].item(), 4), SDG_en[j]])

    # Sort list by the highest cosine similarity score
    for i in range(len(ans)):
        all_sentence_combinations[i] = sorted(
            all_sentence_combinations[i], key=lambda x: x[0], reverse=True)

    word_list = []
    key_word_list = []

    for i in range(len(ans)):
        word_list.append(ans[i])
        key_word_list.append(all_sentence_combinations[i][0][1])

    filter = df['Key phrase'].isin(key_word_list)
    out_df = pd.DataFrame(df.loc[filter])

    show_df = pd.DataFrame(columns=[
                           'Keywords', 'SDGKeyphrase', 'SDGzh', 'Similarity', 'Weight', 'SDG_NO'])

    for i in range(len(word_list)):
        Word = word_list[i]
        Key_phrase = all_sentence_combinations[i][0][1]
        Similarity = all_sentence_combinations[i][0][0]
        filter = out_df['Key phrase'] == Key_phrase
        Weight = out_df['Weight'][filter].values
        SDG_NO = out_df['SDG NO'][filter].values
        keywords_zh = out_df['關鍵字'][filter].values
        for i in range(len(Weight)):
            show_df = show_df.append({
                "Keywords": Word,
                "SDGKeyphrase": Key_phrase,
                'SDGzh': keywords_zh[i],
                "Similarity": Similarity,
                "Weight": float(Weight[i]),
                "SDG_NO": str(SDG_NO[i])}, ignore_index=True)

    word_df = show_df.sort_values(
        "Similarity", ascending=False).reset_index(drop=True)

    no_df = show_df.groupby("SDG_NO").sum()
    size_df = show_df.groupby("SDG_NO").size()
    no_df['Size'] = size_df

    return word_df, no_df.reset_index()


def get_zh_similar(text):
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    # ans = ast.literal_eval(text)
    ans = text.split(",")
    # Encode all sentences
    embeddings = model.encode(SDG_zh)
    ans_embed = model.encode(ans)

    # Compute cosine similarity between all pairs
    cos_sim = util.pytorch_cos_sim(ans_embed, embeddings)

    # Add all pairs to a list with their cosine similarity score
    all_sentence_combinations = []
    for i in range(len(ans)):
        all_sentence_combinations.append([])
        for j in range(len(cos_sim[0])):
            all_sentence_combinations[i].append(
                [round(cos_sim[i][j].item(), 4), SDG_zh[j]])

    # Sort list by the highest cosine similarity score
    for i in range(len(ans)):
        all_sentence_combinations[i] = sorted(
            all_sentence_combinations[i], key=lambda x: x[0], reverse=True)

    word_list = []
    key_word_list = []

    for i in range(len(ans)):
        word_list.append(ans[i])
        key_word_list.append(all_sentence_combinations[i][0][1])

    filter = df['關鍵字'].isin(key_word_list)
    out_df = pd.DataFrame(df.loc[filter])
    out_df.reset_index(inplace=True)

    show_df = pd.DataFrame(columns=[
                           'Keywords', 'SDGKeyphrase', 'SDGzh', 'Similarity', 'Weight', 'SDG_NO'])

    for i in range(len(word_list)):
        Word = word_list[i]
        Key_phrase = all_sentence_combinations[i][0][1]
        Similarity = all_sentence_combinations[i][0][0]
        filter = out_df['關鍵字'] == Key_phrase
        Weight = out_df['Weight'][filter].values
        SDG_NO = out_df['SDG NO'][filter].values
        keywords_zh = out_df['關鍵字'][filter].values
        for i in range(len(Weight)):
            show_df = show_df.append({
                "Keywords": Word,
                "SDGKeyphrase": Key_phrase,
                "SDGzh": keywords_zh[i],
                "Similarity": Similarity,
                "Weight": float(Weight[i]),
                "SDG_NO": str(SDG_NO[i])}, ignore_index=True)

    word_df = show_df.sort_values(
        "Similarity", ascending=False).reset_index(drop=True)

    no_df = show_df.groupby("SDG_NO").sum()
    size_df = show_df.groupby("SDG_NO").size()
    no_df['Size'] = size_df

    return word_df, no_df.reset_index()


def similarity(text, lang):
    if lang == "en":
        word_df, no_df = get_en_similar(text)
    elif(lang == "zh"):
        word_df, no_df = get_zh_similar(text)

    return word_df, no_df

# if __name__ == '__main__':
#     wordlist = "['creative business', 'creative industry', 'creative industries', 'overview creative', 'creative', 'types creative', 'policies creative', 'citizens aesthetics', 'living aesthetics', 'teaching goals', 'aesthetics living', 'culture economic','contemporary academic', 'business', 'living teaching', 'practical spirit', 'academic topic', 'aesthetics', 'prosperous contemporary', 'understanding concepts', 'qualities practical', 'teaching', 'industries explore', 'learners', 'course']"

#     word_df, no_df = get_similar(wordlist)
#     print(word_df)
#     print('##################################################')
#     print(no_df)
