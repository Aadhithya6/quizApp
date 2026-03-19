import json
import os
import requests
import time
from django.conf import settings

def generate_quiz(topic: str, difficulty: str, num_questions: int = 5) -> list:
    """
    Calls NVIDIA LLM API using requests to generate quiz questions in JSON format.
    Includes retry logic (3 times) for invalid JSON or API failures.
    """
    api_key = os.getenv('NVIDIA_API_KEY')
    api_url = os.getenv('NVIDIA_API_URL')
    model_name = os.getenv('NVIDIA_MODEL', 'meta/llama-3.1-405b-instruct')

    if not api_key or not api_url:
        raise ValueError("NVIDIA_API_KEY or NVIDIA_API_URL not configured in environment.")

    prompt = f"""
    Generate {num_questions} {difficulty} level quiz questions on "{topic}".

    Return ONLY valid JSON in this format:
    [
      {{
        "question": "string",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "explanation": "string",
        "type": "SINGLE"
      }}
    ]

    Rules:
    - No markdown
    - No explanation outside JSON
    - Always valid JSON
    - Exactly 4 options
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a professional quiz generator that outputs strict JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            content = data['choices'][0]['message']['content'].strip()
            
            # Basic cleanup if AI adds markdown code blocks
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            questions_data = json.loads(content)
            
            if isinstance(questions_data, list) and len(questions_data) > 0:
                return questions_data
                
        except (requests.RequestException, json.JSONDecodeError, KeyError, Exception) as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == retries - 1:
                raise e
            time.sleep(1) # Small delay before retry
            
    return []
