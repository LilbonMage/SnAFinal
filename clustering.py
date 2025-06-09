# 向量化留言
from sentence_transformers import SentenceTransformer

def embed_comments(list_of_comments):
    """
    將留言列表轉換為向量表示
    :param list_of_comments: 留言列表
    :return: 向量表示的留言列表
    """
    # model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    # model = SentenceTransformer("shibing624/text2vec-base-multilingual")
    model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
    embeddings = model.encode(list_of_comments, show_progress_bar=True)
    return embeddings

# 分群
import hdbscan

def cluster_comments(embeddings):
    """
    對留言向量進行分群
    :param embeddings: 向量表示的留言列表
    :return: 分群結果
    """
    # 使用 HDBSCAN 進行分群
    clusterer = hdbscan.HDBSCAN(min_cluster_size=10, metric='euclidean')
    labels = clusterer.fit_predict(embeddings)
    return labels

import os
import pandas as pd

# === 設定區 ===
input_folder = 'fetched_comments'       # CSV 檔案所在資料夾
output_dir = 'clustered_output'
os.makedirs(output_dir, exist_ok=True)
# ============

# 放所有處理後的結果
all_rows = []

# 處理每個CSV檔案
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        print(f"正在處理檔案：{filename}")
        try:
            df = pd.read_csv(filepath)
            comments = df['text'].tolist()
            embeds = embed_comments(comments)
            labels = cluster_comments(embeds)
            print(f"分群結果：{labels}")
            exit()
                
            if all_rows:
                output_file = filename + '_processed.csv'
                result_file = os.path.join(output_dir, output_file)
                output_df = pd.DataFrame(all_rows)
                output_df.to_csv(result_file, index=False)
                print(f"完成：已輸出至 {result_file}")
                break
            else:
                print("沒有可處理的資料。")
                
        except Exception as e:
            print(f"讀取 {filename} 失敗：{e}")