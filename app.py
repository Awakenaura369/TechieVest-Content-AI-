import streamlit as st
from groq import Groq

# --- Settings & UI Configuration ---
st.set_page_config(page_title="TechieVest Content AI 2026", layout="wide", page_icon="💰")

# Custom CSS for Professional Look (Corrected parameter name)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.5em; 
        background-color: #1a73e8; 
        color: white; 
        font-weight: bold;
        border: none;
    }
    .stDownloadButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background-color: #34a853; 
        color: white; 
    }
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 TechieVest Content Engine v4.0")
st.caption("Advanced AI Automation for Techievest.com | Powered by Groq LPU™")

# Sidebar for API Key and Info
with st.sidebar:
    st.header("🔑 Authentication")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    st.markdown("---")
    st.write("👤 Owner: **Mouhcine Digital Systems**")
    st.info("This tool uses Llama 3.3 and 3.1 models for the highest reasoning quality in 2026.")

if api_key:
    try:
        client = Groq(api_key=api_key)
        
        # Tabs for different features
        tab1, tab2, tab3 = st.tabs(["📝 Article Writer", "🎯 Facebook Sniper", "🖼️ Image Prompter"])

        # --- Tab 1: SEO Article Generator ---
        with tab1:
            st.subheader("Generate High-Authority SEO Content")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                keyword = st.text_input("Topic / Main Keyword:", placeholder="e.g., Best Fintech Apps for Beginners 2026")
                points = st.text_area("Specific Points to cover:", placeholder="Mention security, AI integration, low fees, etc.", height=100)
            
            with col2:
                model_engine = st.selectbox("Select Model:", ["llama-3.3-70b-versatile", "llama-3.1-405b-reasoning"])
                article_length = st.select_slider("Target Word Count:", options=[600, 1000, 1500, 2000], value=1000)

            if st.button("🚀 Generate Mega Article"):
                if keyword:
                    with st.spinner("AI is crafting your professional article..."):
                        system_msg = f"You are a professional Fintech journalist writing for Techievest.com. Write a unique, human-like article about {keyword}. Focus on 2026 data. Use Markdown (H2, H3, lists). Tone: Professional & Trustworthy."
                        user_msg = f"Write {article_length} words about {keyword}. Key points to include: {points}. Formatting: Bold important financial terms, include a 'Verdict' section at the end."
                        
                        try:
                            completion = client.chat.completions.create(
                                model=model_engine,
                                messages=[
                                    {"role": "system", "content": system_msg},
                                    {"role": "user", "content": user_msg}
                                ],
                                temperature=0.7
                            )
                            article_text = completion.choices[0].message.content
                            
                            # Store in session state for other tabs
                            st.session_state['article_output'] = article_text
                            st.session_state['article_topic'] = keyword
                            
                            st.markdown("---")
                            st.markdown(article_text)
                            st.download_button("📩 Download Markdown (.md)", article_text, file_name=f"{keyword.replace(' ', '_')}.md")
                        except Exception as e:
                            st.error(f"Groq API Error: {e}")
                else:
                    st.warning("Please enter a topic first.")

        # --- Tab 2: Facebook Sniper ---
        with tab2:
            st.header("🎯 Viral Social Media Hooks")
            st.write("Generate high-CTR hooks for Facebook Groups and Ads.")
            
            # Use generated article or custom text
            context = st.text_area("Context for Hooks:", value=st.session_state.get('article_output', ''), height=200)
            
            if st.button("🎯 Generate Sniper Hooks"):
                if context:
                    with st.spinner("Analyzing content for viral hooks..."):
                        hook_sys = "You are a master of Digital Marketing. Create 3 viral Facebook hooks: 1 Controversial, 1 Question-based, and 1 FOMO-based. Use emojis and keep it high-energy."
                        hook_comp = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": hook_sys},
                                {"role": "user", "content": f"Article context: {context[:1500]}"}
                            ]
                        )
                        st.success("Hooks Generated Successfully:")
                        st.write(hook_comp.choices[0].message.content)
                else:
                    st.warning("No context found. Please generate an article or paste text here.")

        # --- Tab 3: Image Prompter ---
        with tab3:
            st.header("🖼️ AI Image Prompt Designer")
            st.write("Get the perfect prompt for Gemini or Midjourney.")
            
            if st.button("🎨 Create Visual Prompt"):
                current_topic = st.session_state.get('article_topic')
                if current_topic:
                    with st.spinner("Designing professional prompt..."):
                        img_sys = "You are a creative director. Design a highly detailed image prompt for a fintech blog post thumbnail. Style: 3D Isometric, high-tech, professional, neon-accents."
                        img_comp = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": img_sys},
                                {"role": "user", "content": f"Create a prompt for: {current_topic}"}
                            ]
                        )
                        st.code(img_comp.choices[0].message.content, language="text")
                        st.info("Copy the text above and use it in your AI image generator.")
                else:
                    st.warning("Generate an article first to get a tailored prompt.")

    except Exception as e:
        st.error(f"Connection Error: {e}")
else:
    st.warning("👈 Please enter your Groq API Key in the sidebar to activate the machine.")
