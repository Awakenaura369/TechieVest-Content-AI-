import streamlit as st
from groq import Groq
import re

# --- UI & Styling ---
st.set_page_config(page_title="TechieVest Content AI PRO", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: #ffffff;
        border-radius: 10px 10px 0px 0px; gap: 1px; padding-left: 20px; padding-right: 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #1a73e8 !important; color: white !important; }
    .seo-card { padding: 15px; border-radius: 10px; background-color: #ffffff; border-left: 5px solid #1a73e8; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .score-text { font-size: 28px; font-weight: bold; color: #1a73e8; }
    </style>
    """, unsafe_allow_html=True)

# --- Logic Functions ---
def analyze_seo(text, keyword):
    score = 0
    checks = []
    
    # Word Count Check
    words = len(text.split())
    if words >= 1000: score += 40
    elif words >= 600: score += 20
    else: checks.append("❌ Article is too short for SEO (Under 600 words).")
    
    # Keyword Placement
    if keyword.lower() in text.lower():
        score += 30
        if f"##" in text and keyword.lower() in text.lower().split('##')[1].split('\n')[0]:
            score += 20
        else: checks.append(f"⚠️ Keyword '{keyword}' missing in H2 headings.")
    else:
        checks.append(f"❌ Primary Keyword not found in text.")

    # Structure Check
    if "###" in text: score += 10
    else: checks.append("⚠️ No H3 subheadings found. Use them to break down topics.")
    
    return score, checks

# --- Sidebar ---
with st.sidebar:
    st.title("🛡️ TechieVest PRO")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    st.markdown("---")
    st.info("Target: **Techievest.com**\nOwner: **Mouhcine Digital Systems**")
    st.write("v7.0 - Final Enterprise Edition")

# --- Main App Logic ---
if api_key:
    try:
        client = Groq(api_key=api_key)
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Writer & SEO", "🎯 Social Sniper", "🖼️ Visual Studio", "📊 Content Stats"])

        with tab1:
            col_in, col_set = st.columns([2, 1])
            with col_in:
                topic = st.text_input("Main Keyword / Topic:", placeholder="e.g., Best Fintech Stocks 2026")
                details = st.text_area("Specific Instructions:", placeholder="Focus on AI banking, crypto trends...")
            with col_set:
                model = st.selectbox("Engine:", ["llama-3.3-70b-versatile", "llama-3.1-405b-reasoning"])
                target_words = st.select_slider("Length:", options=[600, 1000, 1500, 2000], value=1000)

            if st.button("🚀 Generate Optimized Content"):
                with st.spinner("AI is building your authority article..."):
                    sys_prompt = f"You are a top-tier Fintech expert for Techievest.com. Write a unique, 2026-focused article about {topic}. Use Markdown (H2, H3). Include a FAQ."
                    user_prompt = f"Topic: {topic}\nInstructions: {details}\nWords: {target_words}. Add a list of 5 'Key Takeaways' and suggest 3 SEO Tags at the end."
                    
                    res = client.chat.completions.create(model=model, messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": user_prompt}
                    ], temperature=0.7)
                    
                    full_content = res.choices[0].message.content
                    st.session_state['article'] = full_content
                    st.session_state['topic'] = topic
                    
                    st.markdown("---")
                    st.markdown(full_content)
                    st.download_button("📩 Export for WordPress", full_content, file_name=f"{topic}.md")

        with tab2:
            st.header("🎯 Facebook Sniper Hooks")
            if 'article' in st.session_state:
                if st.button("Generate Viral Hooks"):
                    with st.spinner("Analyzing hooks..."):
                        hook_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[
                            {"role": "system", "content": "You are a viral marketing expert. Create 3 Facebook hooks (Story, FOMO, Question) with emojis for this article."},
                            {"role": "user", "content": st.session_state['article'][:1500]}
                        ])
                        st.success("Hooks Ready for Facebook Groups:")
                        st.write(hook_res.choices[0].message.content)
            else: st.warning("Generate an article first.")

        with tab3:
            st.header("🖼️ AI Image Designer")
            if 'topic' in st.session_state:
                if st.button("Generate Professional Image Prompt"):
                    img_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[
                        {"role": "system", "content": "Create a detailed 3D render image prompt for a blog thumbnail. Style: High-tech, blue/gold colors, Fintech theme."},
                        {"role": "user", "content": f"Topic: {st.session_state['topic']}"}
                    ])
                    st.code(img_res.choices[0].message.content, language="text")
                    st.info("Use this prompt in Gemini Nano Banana 2.")
            else: st.warning("Generate an article first.")

        with tab4:
            st.header("📊 Real-time SEO Audit")
            if 'article' in st.session_state:
                score, checks = analyze_seo(st.session_state['article'], st.session_state['topic'])
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"<div class='seo-card'><p>Optimization Score</p><p class='score-text'>{score}/100</p></div>", unsafe_allow_html=True)
                with col_b:
                    st.markdown("### SEO Checklist")
                    for check in checks: st.write(check)
                    if not checks: st.success("Everything looks perfect for ranking!")
            else: st.info("No content to analyze yet.")

    except Exception as e:
        st.error(f"API Error: {e}")
else:
    st.warning("Please enter your API key in the sidebar to start.")
