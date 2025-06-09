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

def inference_gemma_3_1b_it(prompt, comment):
    payload = {
        "model": "google/gemma-3-1b-it",
        "messages": [{"role":"system","content":prompt},
                     {"role":"user","content":f"comment:\n\n「{comment}」"}],
        "max_tokens": 512,
        "temperature": 0,
        "top_p": 0.95,
        "stream": False
    }
    
    response = requests.post(invoke_url, headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content'].strip()

# Use a pipeline as a high-level helper
from transformers import pipeline

def inference_qwen3_0_6b(prompt, comment):
    pipe = pipeline("text-generation", model="Qwen/Qwen3-0.6B")
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"comment:\n\n「{comment}」"}
    ]
    response = pipe(messages, max_length=512, do_sample=False)
    print(response)
    return response[0]['generated_text']