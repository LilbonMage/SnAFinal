from llm import inference_gemma_3_1b_it, inference_qwen3_0_6b
from prompts import sentiment_prompt, stance_prompt, attack_prompt
import os

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
import sys
import pandas as pd

# === 設定區 ===
input_folder = 'fetched_comments'
output_dir = 'analyzed_output_2048'
# ============

# 放所有處理後的結果
all_rows = []
i = 0  # 用於跳過檔案
# 處理每個CSV檔案
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        filepath = os.path.join(input_folder, filename)
        try:
            df = pd.read_csv(filepath)
            rows = len(df)
            for index, row in df.iterrows():
                sys.stdout.write(f"\r正在處理檔案：{filename}, {index + 1}/{rows}")
                sys.stdout.flush()

                # === 在這裡自訂你的處理邏輯 ===
                # print(f"處理留言：{row['text']}")
                processed_row = row.to_dict()
                results = analyze_comment(processed_row['text'])
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
            else:
                print("沒有可處理的資料。")
                
        except Exception as e:
            print(f"讀取 {filename} 失敗：{e}")