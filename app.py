import streamlit as st
from groq import Groq
import re

# --- UI & Styling ---
st.set_page_config(page_title="TechieVest Revenue Engine v9", layout="wide", page_icon="💸")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #ffffff; border-radius: 5px; padding: 10px 20px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #2e7d32 !important; color: white !important; }
    .cta-box { padding: 15px; border-radius: 10px; background-color: #fff3e0; border-left: 5px solid #ff9800; margin-bottom: 10px; }
    .html-code { background-color: #1e1e1e; color: #dcdcdc; padding: 10px; border-radius: 5px; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- Logic: SEO & WP HTML ---
def analyze_seo(text, keyword):
    text_l, kw_l = text.lower(), keyword.lower()
    score = 0
    checks = []
    words = len(text.split())
    if words >= 1000: score += 50
    if kw_l in text_l: score += 30
    if "##" in text: score += 20
    return score

def to_wp_html(md):
    html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', md, flags=re.M)
    html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.M)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    return html.replace('\n\n', '</p><p>').replace('\n', '<br>')

# --- Main App ---
with st.sidebar:
    st.title("🛡️ TechieVest v9.0")
    api_key = st.text_input("Groq API Key:", type="password")
    st.write("---")
    st.write("👤 Owner: **Mouhcine Digital Systems**")
    st.success("Target: High-CPM Adsterra/Affiliate")

if api_key:
    client = Groq(api_key=api_key)
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Writer", "💻 WP HTML", "💰 Monetization", "🎯 Sniper"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            topic = st.text_input("Keyword:", placeholder="e.g., Best Trading Apps 2026")
        with col2:
            model = st.selectbox("Model:", ["llama-3.3-70b-versatile", "llama-3.1-405b-reasoning"])
        
        if st.button("🚀 Generate Article"):
            with st.spinner("Writing for profit..."):
                res = client.chat.completions.create(model=model, messages=[
                    {"role": "system", "content": "Fintech Expert Writer. Use Markdown."},
                    {"role": "user", "content": f"Write a 1200-word SEO article about {topic}. Focus on high-value terms."}
                ])
                st.session_state['art'] = res.choices[0].message.content
                st.session_state['kw'] = topic
                st.markdown(st.session_state['art'])

    with tab2:
        if 'art' in st.session_state:
            st.code(to_wp_html(st.session_state['art']), language="html")
        else: st.info("Generate content first.")

    with tab3:
        st.header("💸 Smart CTA & Ad Placements")
        if 'art' in st.session_state:
            if st.button("Generate High-CTR CTAs"):
                with st.spinner("Analyzing content for profit hooks..."):
                    cta_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[
                        {"role": "system", "content": "Marketing Psychology Expert. Create 3 types of CTAs: 1. Native Link for Adsterra Direct Link, 2. High-converting Button Text, 3. Urgent Banner Text."},
                        {"role": "user", "content": f"Topic: {st.session_state['kw']}"}
                    ])
                    st.markdown(f"<div class='cta-box'>{cta_res.choices[0].message.content}</div>", unsafe_allow_html=True)
                    st.info("💡 Hint: Place these near your most engaging paragraphs for max profit.")
        else: st.warning("Need an article to analyze!")

    with tab4:
        st.write("Facebook Sniper active for traffic...")
        # (Sniper logic as before)
else:
    st.warning("Enter API Key.")
