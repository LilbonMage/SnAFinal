import pandas as pd
import jieba
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn_extra.cluster import KMedoids
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from collections import Counter

# ========= 1. 讀取資料 ===============
df = pd.read_csv('youtube_multi_video_comments.csv')
df = df.dropna(subset=['text'])

# ========= 2. 中文清洗與斷詞 ===============
def clean_and_cut(text):
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', str(text))
    words = jieba.cut(text)
    return ' '.join(words)

df['cleaned_text'] = df['text'].apply(clean_and_cut)

# ========= 3. 向量化（TF-IDF） ===============
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df['cleaned_text'])

# ========= 4. 分群（K-Medoids） ===============
k = 4  # 想分幾群就改這裡
medoids = KMedoids(n_clusters=k, metric='cosine', random_state=42)
df['cluster'] = medoids.fit_predict(X)

# ========= 5. 分群關鍵詞統計 ===============
print("📌 各群 Top 10 關鍵詞（K-Medoids）：\n")
for i in range(k):
    cluster_texts = df[df['cluster'] == i]['cleaned_text']
    words = ' '.join(cluster_texts).split()
    top_words = Counter(words).most_common(10)
    print(f'🔹 Cluster {i}: {top_words}')

# ========= 6. 降維 + 視覺化 ===============
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X.toarray())

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster'], cmap='tab10', alpha=0.7)
plt.title('留言內容分群視覺化（K-Medoids + PCA）')
plt.xlabel('PCA-1')
plt.ylabel('PCA-2')
plt.grid(True)
plt.show()
