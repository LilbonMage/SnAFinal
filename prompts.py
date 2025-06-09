# 分析留言
## 分析情緒與強度
sentiment_prompt = f"""
You are an expert sentiment analyst. Evaluate the sentiment of the following comment and classify it as either Positive, Negative, or Neutral. Additionally, rate the emotional intensity on a scale from 0 to 10, where 0 means neutral or calm, and 10 means extremely emotional or intense.

Respond strictly in the following format:
Sentiment / Intensity
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

Only respond with one of the two labels: Malicious or Not Malicious. Do not include any explanations, comments, or extra text.
"""