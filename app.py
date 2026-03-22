import streamlit as st
from groq import Groq
import re

# --- UI & Styling ---
st.set_page_config(page_title="TechieVest AI PRO v8", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #ffffff; border-radius: 5px; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #1a73e8 !important; color: white !important; }
    .seo-card { padding: 20px; border-radius: 12px; background-color: #ffffff; border-left: 6px solid #1a73e8; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .html-box { background-color: #282c34; color: #61afef; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; overflow-x: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- SEO Logic Function (Fixed Case Sensitivity) ---
def analyze_seo(text, keyword):
    score = 0
    checks = []
    text_lower = text.lower()
    kw_lower = keyword.lower()
    
    # 1. Word Count
    words = len(text.split())
    if words >= 1000: score += 40
    elif words >= 600: score += 20
    else: checks.append(f"❌ Short content ({words} words). Google prefers 1000+.")
    
    # 2. Keyword Check (Fixed)
    if kw_lower in text_lower:
        score += 30
        if kw_lower in text_lower[:1000]: score += 10 # Found in intro
        if "##" in text and kw_lower in text_lower: score += 10 # Found in headers
    else:
        checks.append(f"❌ Exact keyword '{keyword}' not detected. Use it naturally in text and H2.")

    # 3. Structure
    if "###" in text: score += 10
    else: checks.append("⚠️ Add H3 subheadings for better readability.")
    
    return score, checks

# --- HTML Converter for WordPress ---
def convert_to_wordpress_html(md_text):
    # تحويل العناوين
    html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', md_text, flags=re.M)
    html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.M)
    html = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html, flags=re.M)
    # تحويل القوائم
    html = re.sub(r'^\* (.*)$', r'<li>\1</li>', html, flags=re.M)
    html = re.sub(r'^- (.*)$', r'<li>\1</li>', html, flags=re.M)
    # تحويل Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    # إضافة فقرات (بسيطة)
    html = html.replace('\n\n', '</p><p>').replace('\n', '<br>')
    return f"<p>{html}</p>"

# --- Sidebar ---
with st.sidebar:
    st.title("🛡️ TechieVest v8.0")
    api_key = st.text_input("Groq API Key:", type="password")
    st.markdown("---")
    st.write("👤 Owner: **Mouhcine Digital Systems**")
    st.info("Mode: **WordPress Optimized**")

# --- Main App ---
if api_key:
    try:
        client = Groq(api_key=api_key)
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Writer", "💻 WordPress HTML", "🎯 Sniper", "📊 SEO Audit"])

        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                topic = st.text_input("Main Keyword:", placeholder="e.g., AI Banking Trends 2026")
                extra = st.text_area("Extra Instructions:", placeholder="Mention security, Morocco context, etc.")
            with col2:
                model = st.selectbox("Model:", ["llama-3.3-70b-versatile", "llama-3.1-405b-reasoning"])
                length = st.select_slider("Words:", options=[600, 1000, 1500, 2000], value=1000)

            if st.button("🚀 Generate Article"):
                with st.spinner("Generating Authority Content..."):
                    sys_p = f"You are a Senior Fintech Journalist for Techievest.com. Write a long-form article about {topic}. Use Markdown. Year: 2026."
                    usr_p = f"Write {length} words on {topic}. Instructions: {extra}. Ensure the keyword '{topic}' appears in the first paragraph and at least one H2 header."
                    
                    res = client.chat.completions.create(model=model, messages=[
                        {"role": "system", "content": sys_p}, {"role": "user", "content": usr_p}
                    ], temperature=0.7)
                    
                    content = res.choices[0].message.content
                    st.session_state['article'] = content
                    st.session_state['topic'] = topic
                    st.markdown(content)

        with tab2:
            st.header("💻 WordPress Ready HTML")
            if 'article' in st.session_state:
                wp_html = convert_to_wordpress_html(st.session_state['article'])
                st.info("Copy this code directly into the 'Text' or 'HTML' editor in WordPress.")
                st.code(wp_html, language="html")
                st.download_button("Download HTML File", wp_html, file_name=f"{st.session_state['topic']}.html")
            else: st.warning("Generate an article first.")

        with tab3:
            st.header("🎯 Facebook Sniper Hooks")
            if 'article' in st.session_state:
                if st.button("Get Viral Hooks"):
                    h_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[
                        {"role": "system", "content": "Viral marketer expert. 3 high-CTR hooks with emojis."},
                        {"role": "user", "content": st.session_state['article'][:1500]}
                    ])
                    st.success("Hooks Created:")
                    st.write(h_res.choices[0].message.content)
            else: st.warning("Generate an article first.")

        with tab4:
            st.header("📊 SEO Audit")
            if 'article' in st.session_state:
                score, checks = analyze_seo(st.session_state['article'], st.session_state['topic'])
                st.markdown(f"<div class='seo-card'><h3>Score: {score}/100</h3></div>", unsafe_allow_html=True)
                for c in checks: st.write(c)
                if not checks: st.success("SEO Perfect!")
            else: st.info("No content to analyze.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your API Key in the sidebar.")
