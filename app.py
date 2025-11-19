import streamlit as st
import json
import random
from datetime import datetime
import time
import os

# --- კონფიგურაცია და დიზაინი ---
st.set_page_config(
    page_title="Global AI News Feed",
    page_icon="📰",
    layout="centered"
)

# CSS სტილები
st.markdown("""
<style>
    /* ფონის ფერი */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    h1 { color: #f8fafc !important; font-family: 'Inter', sans-serif; }
    
    /* სიახლის ბარათის დიზაინი */
    .news-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .news-card:hover {
        border-color: #475569;
        background-color: #253045;
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
    }
    
    /* ტექსტები */
    .news-title { font-weight: 600; color: #3b82f6; font-size: 18px; margin-bottom: 8px; }
    .news-summary { color: #cbd5e1; font-size: 15px; line-height: 1.6; }
    .news-source { color: #64748b; font-size: 12px; margin-top: 12px; }
    .update-time { color: #64748b; font-size: 12px; margin-top: 20px; text-align: center;}

</style>
""", unsafe_allow_html=True)

# --- ფუნქცია ---
def load_news_data():
    """კითხულობს მონაცემებს news.json ფაილიდან, რომელსაც ქმნის GitHub Action"""
    try:
        with open('news.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('news', []), data.get('timestamp', 'უცნობი დრო')
    except FileNotFoundError:
        return [], 'ფაილი ვერ მოიძებნა (ჯერ არ განახლებულა)'
    except json.JSONDecodeError:
        return [], 'მონაცემები დაზიანებულია'
    except Exception as e:
        return [], f'შეცდომა: {e}'

# --- საიტის აწყობა (UI) ---

st.title("📰 Global AI News Aggregator")
st.caption("უახლესი სიახლეები, ავტომატურად განახლებული GitHub Actions-ის მიერ.")

news_items, timestamp = load_news_data()

if not news_items:
    st.info("უახლესი მონაცემები ჯერ არ არის ხელმისაწვდომი. გთხოვთ, ხელით გაუშვათ GitHub Action.")
    
for item in news_items:
    html_card = f"""
    <div class="news-card">
        <div class="news-title">{item.get('title', 'No Title')}</div>
        <div class="news-summary">{item.get('summary', 'No summary provided.')}</div>
        <div class="news-source">Source: {item.get('source', 'Unknown')}</div>
    </div>
    """
    st.markdown(html_card, unsafe_allow_html=True)

st.markdown(f"<div class='update-time'>ბოლოს განახლდა: {timestamp}</div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 12px;'>Powered by Gemini API and Streamlit</div>", unsafe_allow_html=True)

