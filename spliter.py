import pandas as pd
import os

# === 設定區 ===
input_file = 'youtube_multi_video_comments.csv'  # 原始CSV檔路徑
output_dir = 'output_csvs'  # 分割後CSV檔的輸出資料夾
key_column_index = 0  # 依據第幾欄分割，0代表第一欄
# ============

import re

def remove_html_tags(text):
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text

# 確保輸出資料夾存在
os.makedirs(output_dir, exist_ok=True)

# 讀取CSV
df = pd.read_csv(input_file)

# 取得欄位名稱（避免用 index 的方式造成混淆）
key_column_name = df.columns[key_column_index]

# 根據第一欄的值分組並儲存
for key, group in df.groupby(key_column_name):
    # 安全地處理檔名（避免非法字元）
    safe_key = str(key).replace('/', '_').replace('\\', '_')
    output_path = os.path.join(output_dir, f'{safe_key}.csv')
    # 移除 HTML 標籤
    group['text'] = group['text'].apply(remove_html_tags)
    group.to_csv(output_path, index=False)

print(f"已完成分割，檔案儲存在：{output_dir}")
