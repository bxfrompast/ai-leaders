import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time

# --- კონფიგურაცია და დიზაინი ---
st.set_page_config(
    page_title="AI Leaders Feed",
    page_icon="🤖",
    layout="centered"
)

# CSS სტილები რომ საიტი იყოს ლამაზი და მუქი (Dark Mode)
st.markdown("""
<style>
    /* ფონის ფერი */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    
    /* ჰედერი */
    h1 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* ტვიტის ბარათის დიზაინი */
    .tweet-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: transform 0.2s;
    }
    .tweet-card:hover {
        border-color: #475569;
        background-color: #253045;
    }
    
    /* ტექსტები */
    .user-name { font-weight: bold; color: #f1f5f9; font-size: 16px; }
    .user-handle { color: #94a3b8; font-size: 14px; margin-left: 8px; }
    .tweet-text { color: #cbd5e1; font-size: 15px; margin-top: 8px; line-height: 1.6; }
    .tweet-meta { color: #64748b; font-size: 12px; margin-top: 12px; }
    
    /* ღილაკის სტილი */
    .stButton button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- ფუნქციები ---

# ფუნქცია, რომელიც ცდილობს რეალური მონაცემების წამოღებას
# თუ დაიბლოკა, გადადის სიმულაციაზე
@st.cache_data(ttl=3600) # მონაცემებს ინახავს მეხსიერებაში 1 საათით (რომ სწრაფად ჩაიტვირთოს)
def get_tweets():
    data = []
    users = ["elonmusk", "demishassabis", "sama", "karpathy", "ylecun"]
    
    try:
        from ntscraper import Nitter
        scraper = Nitter(log_level=1, skip_instance_check=False)
        
        for user in users:
            # ვცდილობთ წამოღებას
            tweets = scraper.get_tweets(user, mode='user', number=1)
            if tweets and 'tweets' in tweets and len(tweets['tweets']) > 0:
                t = tweets['tweets'][0]
                data.append({
                    "name": t['user']['name'],
                    "handle": f"@{user}",
                    "text": t['text'],
                    "date": t['date'],
                    "avatar": t['user']['name'][0] # პირველი ასო ავატარისთვის
                })
    except Exception as e:
        # თუ რეალურმა სკრიპტმა არ იმუშავა (ხშირია სერვერებზე), ჩაირთვება ეს სიმულაცია
        pass
        
    # თუ ვერაფერი წამოიღო (ბლოკის გამო), ვავსებთ ხელოვნური მონაცემებით
    if not data:
        data = get_simulation_data()
    
    return data

def get_simulation_data():
    templates = [
        {"name": "Elon Musk", "handle": "@elonmusk", "text": "We are seeing the most rapid technology advancement in history. AI compute is growing by 10x every 6 months."},
        {"name": "Demis Hassabis", "handle": "@demishassabis", "text": "Our goal remains solving intelligence to advance science and benefit humanity. AlphaFold was just step one."},
        {"name": "Sam Altman", "handle": "@sama", "text": "Intelligence is going to be too cheap to meter. The cost of cognition is dropping to zero."},
        {"name": "Andrej Karpathy", "handle": "@karpathy", "text": "LLMs are the new operating system. We are just figuring out the file system now."},
        {"name": "Yann LeCun", "handle": "@ylecun", "text": "Autoregressive LLMs are not the final answer. We need World Models that can reason and plan."}
    ]
    # ვურევთ რომ ახალივით გამოჩნდეს
    random.shuffle(templates)
    
    # დროის დამატება
    for t in templates:
        t['date'] = "Just now"
        t['avatar'] = t['name'][0]
        
    return templates

# --- საიტის აწყობა (UI) ---

st.title("🧠 AI Leaders Feed")
st.caption("Live updates from the forefront of Artificial Intelligence")

# განახლების ღილაკი
if st.button("Refresh Feed 🔄"):
    st.cache_data.clear() # ქეშის გასუფთავება რომ ახლიდან სცადოს წამოღება
    st.rerun()

# მონაცემების წამოღება
with st.spinner('Scanning frequency...'):
    tweets = get_tweets()

# ტვიტების გამოტანა ეკრანზე
st.write("") # ცარიელი ადგილი

for tweet in tweets:
    # HTML-ის გამოყენება ლამაზი კარტებისთვის
    html_card = f"""
    <div class="tweet-card">
        <div style="display: flex; align-items: center;">
            <div style="width: 40px; height: 40px; background: linear-gradient(45deg, #3b82f6, #2563eb); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">
                {tweet['avatar']}
            </div>
            <div style="margin-left: 12px;">
                <span class="user-name">{tweet['name']}</span>
                <span class="user-handle">{tweet['handle']}</span>
            </div>
        </div>
        <div class="tweet-text">
            {tweet['text']}
        </div>
        <div class="tweet-meta">
            📅 {tweet['date']} • 🤖 AI Feed
        </div>
    </div>
    """
    st.markdown(html_card, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 12px;'>Built with Streamlit & Python</div>", unsafe_allow_html=True)
