import os
from dotenv import load_dotenv
load_dotenv()
import requests

# LLM 設定
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False

headers = {
  "Authorization": "Bearer " + os.getenv("NVIDIA_API_KEY"),
  "Accept": "text/event-stream" if stream else "application/json"
}

def inference(prompt, comment):
    payload = {
        "model": "google/gemma-3-27b-it",
        "messages": [{"role":"system","content":prompt}, {"role":"user","content":f"comment:\n\n「{comment}」"}],
        "max_tokens": 512,
        "temperature": 0,
        "top_p": 0.95,
        "stream": False
    }
    
    response = requests.post(invoke_url, headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content'].strip()


# 分析留言
## 分析情緒與強度
sentiment_prompt = f"""
You are an expert sentiment analyst. Evaluate the sentiment of the following comment and classify it as either Positive, Negative, or Neutral. Additionally, rate the emotional intensity on a scale from 0 to 10, where 0 means neutral or calm, and 10 means extremely emotional or intense.

Respond strictly in the following format:
[Sentiment / Intensity]
Do not include any explanations, comments, or extra text.
"""

## 分析立場，支持行人/中立/支持駕駛
stance_prompt = f"""
You are a stance classification expert specializing in social commentary analysis.

Your task is to analyze a given YouTube comment related to a video about pedestrian rights. Based on the content, classify the stance into one of the following four categories:

- Supportive
- Neutral
- Irrelevant
- Opposed

Only respond with one of the four category labels above. Do not include any explanations, justifications, punctuation, or additional text of any kind. Respond with a **single word only**.
"""
## 分析留言是否是攻擊、謾罵
attack_prompt = f"""
You are a content moderation expert specializing in detecting personal verbal attacks and hate speech.

Classify the following comment as either:

- Malicious: The comment contains deliberate personal insults, hate speech, or abusive language directed at individuals or groups.
- Not Malicious: The comment includes neutral, critical, or emotional language that does not target individuals or groups with hate or abuse.

Examples:
1. "You're a worthless idiot." → Malicious
2. "This platform's policy is so frustrating." → Not Malicious

Only respond with one of the two labels: Malicious or Not Malicious.
"""

# Only respond with one of the two labels above. Do not provide any explanation, reasoning, or additional commentary. Return only the label as a single word.

def analyze_comment(comment):
    sentiment = inference(sentiment_prompt, comment)
    stance = inference(stance_prompt, comment)
    attack = inference(attack_prompt, comment)
    
    return {
        "sentiment": sentiment,
        "stance": stance,
        "attack": attack
    }

# 主程式：處理所有留言

import os
import pandas as pd

# === 設定區 ===
input_folder = 'output_csvs'       # CSV 檔案所在資料夾
output_dir = 'analyzed_output'
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
            for index, row in df.iterrows():
                # === 在這裡自訂你的處理邏輯 ===
                processed_row = row.to_dict()
                results = analyze_comment(row['text'])
                processed_row['sentiment'] = results['sentiment']
                processed_row['stance'] = results['stance']
                processed_row['attack'] = results['attack']
                # ===================================
                
                all_rows.append(processed_row)
                
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