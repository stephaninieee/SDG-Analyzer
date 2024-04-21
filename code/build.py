from ckip_transformers.nlp import CkipWordSegmenter
from sentence_transformers import SentenceTransformer
import torch
import os

ws_driver = CkipWordSegmenter(level=1)
ch_st_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
en_st_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

if not os.path.isdir('./model'):
    os.mkdir('./model')
torch.save(ws_driver, './model/ws_driver.pkl')
torch.save(ch_st_model, './model/ch_st_model.pkl')
torch.save(en_st_model, './model/en_st_model.pkl')
print("Done")
