import requests
import json
from datetime import datetime
import os

# Gemini API-ის კონფიგურაცია
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
OUTPUT_FILE = "news.json"

# API Key-ს ვიღებთ GitHub Secrets-დან, ან ცარიელია
API_KEY = os.environ.get("GEMINI_API_KEY", "")

# --- JSON სქემა Gemini-ისთვის ---
json_schema = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "title": {"type": "STRING", "description": "A concise title for the news item."},
            "summary": {"type": "STRING", "description": "A short, 2-3 sentence summary of the news item."},
            "source": {"type": "STRING", "description": "The title of the primary source or publication (e.g., TechCrunch, OpenAI Blog)."}
        },
        "required": ["title", "summary", "source"]
    }
}

def fetch_and_save_news():
    print("Starting news generation via Gemini API...")

    if not API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        # თუ გასაღები არაა, ვქმნით სიმულაციის ფაილს
        create_simulation_file("API Key not set")
        return

    # ეს არის System Instruction - ეუბნება მოდელს რა როლი უნდა შეასრულოს
    system_prompt = "You are a world-class AI news aggregator. Your task is to find the 5 most important and recent news items regarding Artificial Intelligence (AI) and present them in a structured JSON format. The summaries must be in English. Use the Google Search tool for grounding."
    
    # ეს არის User Prompt - რა დავალება უნდა შეასრულოს
    user_query = "Find and summarize the 5 most critical global AI news stories from the last 24 hours. Focus on major releases, policy changes, or breakthrough research."
    
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "tools": [{"google_search": {}}],
        "config": {
            "responseMimeType": "application/json",
            "responseSchema": json_schema
        },
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }
    
    # API გამოძახება
    try:
        response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=payload, timeout=60)
        response.raise_for_status() # HTTP შეცდომების დამუშავება

        result = response.json()
        
        # მონაცემების ამოღება
        json_string = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '{}')
        
        try:
            news_list = json.loads(json_string)
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON response from Gemini.")
            create_simulation_file("JSON parsing error")
            return

        final_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S (GMT)"),
            "news": news_list
        }
        
        # მონაცემების შენახვა news.json-ში
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully saved {len(news_list)} news items to {OUTPUT_FILE}")

    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error during API call: {e}")
        create_simulation_file(f"Network error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        create_simulation_file(f"Unexpected error: {e}")


def create_simulation_file(error_reason):
    """ქმნის ბექაფ ფაილს თუ API-მ არ იმუშავა"""
    print(f"Creating fallback simulation file. Reason: {error_reason}")
    templates = [
        {"title": "Fallback: Cannot fetch real-time news", "summary": f"The Gemini API call failed due to: {error_reason}. The feed will update on the next successful run.", "source": "System Error"},
        {"title": "Static: AI Policy Takes Center Stage", "summary": "Placeholder summary indicating an API connection issue. Please check the GitHub Actions logs.", "source": "AI Almanac"},
    ]
    
    final_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S (GMT)"),
        "news": templates
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    fetch_and_save_news()
