import os
from dotenv import load_dotenv
load_dotenv()
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers.utils import logging

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

def inference_qwen3_0_6b(prompt, comment):
    model_id = "Qwen/Qwen3-0.6B"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
    logging.set_verbosity_error()  # Suppress warnings
    chat_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    prompt = tokenizer.apply_chat_template(
        [{"role": "system", "content": prompt},{"role": "user", "content": comment}],
        tokenize=False,
        add_generation_prompt=True
    )
    output = chat_pipe(prompt, max_new_tokens=2048, do_sample=False)
    return output[0]['generated_text'].strip().split('\n')[-1].strip()