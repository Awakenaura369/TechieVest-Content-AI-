import streamlit as st
from groq import Groq

# --- Settings & UI ---
st.set_page_config(page_title="TechieVest Content AI 2026", layout="wide", page_icon="💰")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1a73e8; color: white; font-weight: bold; }
    .stDownloadButton>button { width: 100%; border-radius: 5px; background-color: #34a853; color: white; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🚀 TechieVest Content Engine v4.0")
st.caption("Professional Automation for Mouhcine Digital Systems")

# Sidebar
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    st.info("Using Llama 3.3 & 3.1 for Maximum Reasoning.")
    st.markdown("---")
    st.write("Target: **Techievest.com**")

if api_key:
    try:
        client = Groq(api_key=api_key)
        
        tab1, tab2, tab3 = st.tabs(["📝 Article Writer", "🎯 Facebook Sniper", "🖼️ Image Prompter"])

        # --- Tab 1: SEO Article Generator ---
        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                keyword = st.text_input("Topic / Keyword:", placeholder="e.g., Best Crypto Wallets 2026")
                points = st.text_area("Key Points (Optional):", placeholder="Mention security, AI integration, etc.")
            with col2:
                model = st.selectbox("Engine:", ["llama-3.3-70b-versatile", "llama-3.1-405b-reasoning"])
                length = st.select_slider("Words:", options=[600, 1000, 1500, 2000], value=1000)

            if st.button("Generate Mega Article"):
                with st.spinner("AI is crafting your masterpiece..."):
                    sys_prompt = f"You are a professional Fintech journalist for Techievest.com. Write a unique, SEO-optimized article about {keyword}. Focus on 2026 data. Use Markdown (H2, H3, lists). Tone: Professional & Authoritative."
                    user_prompt = f"Write {length} words about {keyword}. Specific points: {points}. Formatting: Bold key terms, include a FAQ section at the end."
                    
                    chat = client.chat.completions.create(model=model, messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": user_prompt}
                    ], temperature=0.7)
                    
                    full_text = chat.choices[0].message.content
                    st.session_state['article'] = full_text
                    st.session_state['topic'] = keyword
                    st.markdown(full_text)
                    st.download_button("📩 Download Article", full_text, file_name=f"{keyword}.md")

        # --- Tab 2: Facebook Sniper ---
        with tab2:
            st.header("🎯 Viral Social Media Hooks")
            content_to_hook = st.text_area("Source Text:", value=st.session_state.get('article', ''), height=200)
            if st.button("Generate Sniper Hooks"):
                if content_to_hook:
                    with st.spinner("Analyzing hooks..."):
                        hook_chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[
                            {"role": "system", "content": "You are a viral marketing expert. Create 3 high-CTR Facebook hooks (Controversial, Question-based, and List-based) with emojis."},
                            {"role": "user", "content": f"Create hooks for this: {content_to_hook[:1500]}"}
                        ])
                        st.success("Your Hooks are ready:")
                        st.write(hook_chat.choices[0].message.content)
                else: st.warning("Please generate an article first.")

        # --- Tab 3: Image Prompter ---
        with tab3:
            st.header("🖼️ AI Image Prompt Generator")
            if st.button("Create Image Prompt"):
                if st.session_state.get('article'):
                    with st.spinner("Designing visual prompt..."):
                        img_chat = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[
                            {"role": "system", "content": "Create a highly detailed English prompt for an AI image generator (like Gemini or Midjourney). Focus on a professional, 3D render, high-tech fintech style related to the topic."},
                            {"role": "user", "content": f"Topic: {st.session_state.get('topic')}"}
                        ])
                        st.code(img_chat.choices[0].message.content, language="text")
                        st.info("Copy this prompt into your Image Generator to get a perfect thumbnail.")
                else: st.warning("Please generate an article first.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter your API Key in the sidebar.")
