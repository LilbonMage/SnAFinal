from llm import inference_gemma_3_1b_it, inference_qwen3_0_6b
from prompts import sentiment_prompt, stance_prompt, attack_prompt

# Only respond with one of the two labels above. Do not provide any explanation, reasoning, or additional commentary. Return only the label as a single word.

def analyze_comment(comment):
    sentiment = inference_qwen3_0_6b(sentiment_prompt, comment)
    stance = inference_qwen3_0_6b(stance_prompt, comment)
    attack = inference_qwen3_0_6b(attack_prompt, comment)
    
    return {
        "sentiment": sentiment,
        "stance": stance,
        "attack": attack
    }

# 主程式：處理所有留言

import os
import pandas as pd

# === 設定區 ===
input_folder = 'fetched_comments'       # CSV 檔案所在資料夾
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
            i = 0
            df = pd.read_csv(filepath)
            for index, row in df.iterrows():
                i += 1
                if i == 6:
                    print("測試：只處理前5筆資料")
                    break
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