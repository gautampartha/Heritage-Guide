from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import streamlit.components.v1 as components

from modules.chatbot import get_ai_response, get_demo_response
from modules.quiz import get_quiz_questions
from modules.recognition import get_all_monument_names, get_demo_result, get_monument_details, identify_monument
from modules.sustainability import get_demo_sustainability_tips, get_sustainability_tips

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Sanskriti AI", page_icon="🏛️", layout="wide")

# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "monument_result" not in st.session_state:
    st.session_state["monument_result"] = None
if "monument_details" not in st.session_state:
    st.session_state["monument_details"] = None
if "quiz_questions" not in st.session_state:
    st.session_state["quiz_questions"] = None
if "current_question_index" not in st.session_state:
    st.session_state["current_question_index"] = 0
if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = []
if "quiz_started" not in st.session_state:
    st.session_state["quiz_started"] = False
if "quiz_completed" not in st.session_state:
    st.session_state["quiz_completed"] = False

# -----------------------------------------------------------------------------
# Custom CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --gold: #C9A84C;
  --gold-light: #E8C97A;
  --gold-dim: rgba(201, 168, 76, 0.12);
  --bg-primary: #1A1A2E;
  --bg-secondary: #1F1F35;
  --bg-card: #242438;
  --bg-card-hover: #2A2A42;
  --border: rgba(201, 168, 76, 0.25);
  --border-strong: rgba(201, 168, 76, 0.55);
  --text-primary: #F0EAD6;
  --text-secondary: #B8A98A;
  --text-muted: #7A6E5C;
  --accent-red: #C44B4B;
  --accent-teal: #4B9B8E;
  --success: #4B8E6E;
  --radius: 12px;
  --radius-lg: 20px;
}

*, *::before, *::after { box-sizing: border-box; }

.stApp {
  background: linear-gradient(160deg, #1A1A2E 0%, #16213E 50%, #1A1A2E 100%) !important;
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-primary) !important;
}

.stApp::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
  opacity: 0.4;
}

.main .block-container {
  padding: 2rem 3rem 4rem 3rem !important;
  max-width: 1200px !important;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0F0F20 0%, #13132A 100%) !important;
  border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div { padding: 2rem 1.2rem !important; }

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: 'Cormorant Garamond', serif !important;
  color: var(--gold) !important;
  letter-spacing: 0.05em !important;
}

[data-testid="stSidebar"] .stRadio > label {
  color: var(--text-secondary) !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
}

[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.92rem !important;
  color: var(--text-primary) !important;
  letter-spacing: 0.02em !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  border-radius: 8px !important;
  padding: 0.5rem 0.8rem !important;
  margin: 2px 0 !important;
  transition: all 0.2s ease !important;
  border: 1px solid transparent !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: var(--gold-dim) !important;
  border-color: var(--border) !important;
}

[data-testid="stSidebar"] .stCaption {
  color: var(--text-muted) !important;
  font-size: 0.75rem !important;
}

[data-testid="stSidebar"] hr {
  border-color: var(--border) !important;
  margin: 1rem 0 !important;
}

h1 {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 3rem !important;
  font-weight: 600 !important;
  color: var(--gold) !important;
  letter-spacing: -0.01em !important;
  line-height: 1.1 !important;
  margin-bottom: 0.5rem !important;
}

h2 {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 2rem !important;
  font-weight: 500 !important;
  color: var(--text-primary) !important;
  letter-spacing: 0.01em !important;
}

h3 {
  font-family: 'DM Sans', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  color: var(--gold-light) !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}

p, .stMarkdown p {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-secondary) !important;
  line-height: 1.7 !important;
  font-size: 0.95rem !important;
}

.stAlert {
  border-radius: var(--radius) !important;
  border: 1px solid !important;
  backdrop-filter: blur(10px) !important;
}

div[class*="stInfo"] {
  background: rgba(75, 155, 142, 0.08) !important;
  border-color: rgba(75, 155, 142, 0.3) !important;
  color: #7ECDC0 !important;
}

div[class*="stSuccess"] {
  background: rgba(75, 142, 110, 0.08) !important;
  border-color: rgba(75, 142, 110, 0.3) !important;
  color: #7ECDA0 !important;
}

div[class*="stWarning"] {
  background: rgba(201, 168, 76, 0.08) !important;
  border-color: rgba(201, 168, 76, 0.3) !important;
  color: var(--gold-light) !important;
}

div[class*="stError"] {
  background: rgba(196, 75, 75, 0.08) !important;
  border-color: rgba(196, 75, 75, 0.3) !important;
  color: #E08080 !important;
}

.stButton > button {
  background: linear-gradient(135deg, var(--gold) 0%, #A07830 100%) !important;
  color: #0A0A0F !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  padding: 0.6rem 1.4rem !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 20px rgba(201, 168, 76, 0.25) !important;
}

.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(201, 168, 76, 0.4) !important;
  background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 100%) !important;
}

.stButton > button:active { transform: translateY(0px) !important; }

.stFormSubmitButton > button {
  background: linear-gradient(135deg, var(--accent-teal) 0%, #2D6B61 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  font-size: 0.88rem !important;
  padding: 0.6rem 1.4rem !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 20px rgba(75, 155, 142, 0.25) !important;
}

.stFormSubmitButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(75, 155, 142, 0.4) !important;
}

[data-testid="stFileUploader"] {
  background: var(--bg-card) !important;
  border: 2px dashed var(--border-strong) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.5rem !important;
  transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: var(--gold) !important;
  background: var(--gold-dim) !important;
}

[data-testid="stFileUploader"] label {
  color: var(--text-secondary) !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1.2rem 1.5rem !important;
  transition: all 0.3s ease !important;
}

[data-testid="stMetric"]:hover {
  border-color: var(--gold) !important;
  background: var(--bg-card-hover) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(201, 168, 76, 0.1) !important;
}

[data-testid="stMetricLabel"] {
  color: var(--text-muted) !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 2rem !important;
  color: var(--gold) !important;
  font-weight: 600 !important;
}

[data-testid="stMetricDelta"] {
  color: var(--text-muted) !important;
  font-size: 0.78rem !important;
}

.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border-radius: 10px !important;
  padding: 4px !important;
  gap: 4px !important;
  border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-muted) !important;
  border-radius: 8px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.03em !important;
  border: none !important;
  padding: 0.5rem 1rem !important;
  transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
  background: var(--gold-dim) !important;
  color: var(--gold) !important;
  border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"]:hover { color: var(--text-primary) !important; }

.stTabs [data-baseweb="tab-panel"] {
  background: var(--bg-card) !important;
  border-radius: 0 0 var(--radius) var(--radius) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
  padding: 1.5rem !important;
  animation: fadeSlideUp 0.4s ease forwards;
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

[data-testid="stChatMessage"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1rem 1.2rem !important;
  margin: 0.5rem 0 !important;
}

.stChatInput textarea {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
}

.stChatInput textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 2px var(--gold-dim) !important;
}

.stRadio div[role="radiogroup"] label {
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.92rem !important;
}

.stProgress > div > div {
  background: linear-gradient(90deg, var(--gold) 0%, var(--gold-light) 100%) !important;
  border-radius: 999px !important;
}

.stProgress > div {
  background: var(--bg-card) !important;
  border-radius: 999px !important;
  border: 1px solid var(--border) !important;
}

.streamlit-expanderHeader {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 500 !important;
  transition: all 0.2s ease !important;
}

.streamlit-expanderHeader:hover {
  border-color: var(--gold) !important;
  color: var(--gold) !important;
}

.streamlit-expanderContent {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
  border-radius: 0 0 var(--radius) var(--radius) !important;
}

hr {
  border-color: var(--border) !important;
  margin: 2rem 0 !important;
}

[data-testid="stImage"] img {
  border-radius: var(--radius-lg) !important;
  border: 1px solid var(--border) !important;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5) !important;
}

.stSpinner > div { border-top-color: var(--gold) !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

.stCaption, [data-testid="stCaptionContainer"] {
  color: var(--text-muted) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.04em !important;
}

footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }
header[data-testid="stHeader"] {
  background: rgba(20, 20, 40, 0.85) !important;
  backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid var(--border) !important;
}

.heritage-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  transition: all 0.3s ease;
  height: 100%;
}

.heritage-card:hover {
  border-color: var(--gold);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(201, 168, 76, 0.12);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Demo mode — always ON
# -----------------------------------------------------------------------------
demo_mode = True

# -----------------------------------------------------------------------------
# Sidebar navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
<div style="padding: 0.5rem 0 1.5rem 0;">
  <div style="font-family:'Cormorant Garamond',serif; font-size:1.6rem; font-weight:600; color:#C9A84C; letter-spacing:0.05em;">
    🏛️ Sanskriti
  </div>
  <div style="font-family:'DM Mono',monospace; font-size:0.65rem; color:#7A6E5C; letter-spacing:0.2em; text-transform:uppercase; margin-top:2px;">
    AI Heritage Guide
  </div>
</div>
""", unsafe_allow_html=True)
    st.markdown("---")

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "🏠 Home"

    page_options = [
        "🏠 Home",
        "🔍 Monument Recognition",
        "🤖 AI Chatbot",
        "🌿 Sustainability",
        "🧠 Quiz",
    ]
    current_page = st.session_state.get("selected_page", "🏠 Home")
    try:
        default_index = page_options.index(current_page)
    except ValueError:
        default_index = 0

    selected_page = st.radio(
        "Navigate",
        options=page_options,
        index=default_index,
        key="nav_radio",
        label_visibility="collapsed",
    )
    st.session_state["selected_page"] = selected_page

    st.markdown("---")
    st.sidebar.markdown("### 🎬 Demo Flow")
    st.sidebar.markdown("""
1. 📸 Upload monument image
2. 🔍 View AI recognition
3. 📖 Explore history tabs
4. 🤖 Chat with AI guide
5. 🌿 Check sustainability
6. 🧠 Take the quiz
""")
    st.sidebar.divider()
    st.sidebar.caption("Sanskriti AI © 2025")

# -----------------------------------------------------------------------------
# Home page
# -----------------------------------------------------------------------------
if selected_page == "🏠 Home":

    # Cinematic hero with Taj Mahal image
    st.markdown("""
<div style="
  position: relative;
  width: 100%;
  height: 420px;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 2rem;
  border: 1px solid rgba(201,168,76,0.3);
">
  <img
    src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Taj_Mahal%2C_Agra%2C_India_edit3.jpg/1280px-Taj_Mahal%2C_Agra%2C_India_edit3.jpg"
    style="width:100%; height:100%; object-fit:cover; display:block;"
  />
  <div style="
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, rgba(10,10,20,0.92) 0%, rgba(10,10,20,0.5) 60%, rgba(10,10,20,0.15) 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 3rem;
  ">
    <div style="
      display: inline-block;
      background: rgba(201,168,76,0.15);
      border: 1px solid rgba(201,168,76,0.5);
      color: #C9A84C;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      padding: 0.3rem 0.9rem;
      border-radius: 999px;
      font-family: DM Mono, monospace;
      margin-bottom: 1.2rem;
      width: fit-content;
    ">&#10022; AI-Powered Heritage Guide</div>
    <div style="
      font-family: Cormorant Garamond, serif;
      font-size: 3.2rem;
      color: #F0EAD6;
      font-weight: 600;
      line-height: 1.1;
      margin-bottom: 1rem;
    ">Discover India's<br><span style="color:#C9A84C;">Living Heritage</span></div>
    <p style="
      font-size: 1rem;
      color: #B8A98A;
      max-width: 480px;
      line-height: 1.7;
      font-family: DM Sans, sans-serif;
      margin: 0;
    ">Upload a monument photograph and let AI guide you through 5,000 years of history, culture, and architecture.</p>
  </div>
</div>
""", unsafe_allow_html=True)

    # Metrics
    st.markdown("")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🏛️ Monuments Covered", "5+", "Growing database")
    with m2:
        st.metric("🤖 AI Powered", "Vision AI", "Smart recognition")
    with m3:
        st.metric("🌍 SDG Aligned", "SDG 11 & 17", "Responsible Tourism")
    with m4:
        st.metric("⚡ Response Time", "< 2 sec", "Real-time AI")

    st.markdown("")

    # Feature cards
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            '<div class="heritage-card"><strong>🔍 Smart Recognition</strong><br><br>'
            'Upload any monument photo for instant AI identification</div>',
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            '<div class="heritage-card"><strong>🤖 Heritage Chatbot</strong><br><br>'
            'Ask anything about history, architecture, culture</div>',
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            '<div class="heritage-card"><strong>🌿 Sustainability Guide</strong><br><br>'
            'SDG-aligned responsible tourism tips</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(
        '<div class="heritage-card"><strong>🧠 Knowledge Quiz</strong><br><br>'
        'Test your heritage knowledge with AI-generated MCQs</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    with st.expander("🚀 How to use Sanskriti AI"):
        st.markdown("""
**Step 1:** Go to Monument Recognition and upload a monument photo

**Step 2:** View detailed history, architecture, and facts

**Step 3:** Chat with AI Heritage Chatbot about the monument

**Step 4:** Get Sustainability tips and take the Knowledge Quiz
""")

    st.divider()
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("**🛠️ Tech Stack**")
        st.caption("Python + Streamlit")
        st.caption("AI / Computer Vision")
        st.caption("Pillow + JSON")
    with a2:
        st.markdown("**🎯 Problem Solved**")
        st.caption("Lack of accessible heritage education")
        st.caption("Promoting responsible tourism")
        st.caption("AI-powered cultural preservation")
    with a3:
        st.markdown("**🌍 Impact**")
        st.caption("500M+ annual heritage visitors")
        st.caption("SDG 11 & 17 aligned")
        st.caption("Preserving 5000 years of culture")

# -----------------------------------------------------------------------------
# Monument Recognition page
# -----------------------------------------------------------------------------
elif selected_page == "🔍 Monument Recognition":
    st.markdown("## Monument Recognition")

    image_to_show = st.session_state.get("uploaded_image")
    file_uploader_here = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        key="recognition_uploader",
    )
    if file_uploader_here is not None:
        st.session_state.uploaded_image = file_uploader_here
        image_to_show = file_uploader_here

    if image_to_show is not None:
        image_bytes = image_to_show.read()
        image_to_show.seek(0)

        with st.spinner("🔍 Analyzing monument with AI..."):
            st.session_state["monument_result"] = get_demo_result()

        result = st.session_state.get("monument_result")

        if result is not None and result.get("monument_name") != "Unknown":
            st.toast("✅ Monument identified!", icon="🏛️")

        col_img, col_result = st.columns(2)
        with col_img:
            st.image(image_to_show, caption="Uploaded Monument", use_container_width=True)
        with col_result:
            if result is not None:
                if result.get("monument_name") == "Unknown":
                    st.warning("⚠️ Could not identify monument. Try a clearer image.")
                else:
                    st.success("✅ Monument Identified!")
                st.markdown(f"**🏛️ Monument:** {result.get('monument_name', '—')}")
                st.markdown(f"**📍 Location:** {result.get('location', '—')}")
                st.markdown(f"**📊 Confidence:** {result.get('confidence', '—')}")
                st.markdown(f"**📝** {result.get('brief_description', '—')}")

        # Detailed information — loads immediately after upload
        result = st.session_state.get("monument_result")
        if result is not None and result.get("monument_name") != "Unknown":
            monument_name = result.get("monument_name")
            monument_details = get_monument_details(monument_name)
            st.session_state["monument_details"] = monument_details

            if monument_details is not None:
                st.markdown("---")
                st.markdown("### 📚 Detailed Information")

                tab1, tab2, tab3, tab4 = st.tabs(
                    ["📖 History", "🏛️ Architecture", "📊 Key Facts", "🎯 Visitor Info"]
                )

                with tab1:
                    st.markdown(f"**Built By:** {monument_details.get('built_by', '—')}")
                    st.markdown(f"**Year Built:** {monument_details.get('year_built', '—')}")
                    st.markdown(f"**Location:** {monument_details.get('location', '—')}")
                    st.markdown(f"**Type:** {monument_details.get('type', '—')}")
                    st.markdown("")
                    st.markdown("**Cultural Importance:**")
                    st.info(monument_details.get("cultural_importance", "—"))
                    if monument_details.get("unesco"):
                        st.success("🏆 UNESCO World Heritage Site")
                    if monument_details.get("seven_wonders"):
                        st.success("✨ One of the Seven Wonders of the World")

                with tab2:
                    st.info(monument_details.get("architecture", "—"))

                with tab3:
                    key_facts = monument_details.get("key_facts", [])
                    for fact in key_facts:
                        st.markdown(f"✅ {fact}")
                    st.markdown("")
                    fun_fact = monument_details.get("fun_fact", "")
                    if fun_fact:
                        st.warning(f"💡 Fun Fact: {fun_fact}")

                with tab4:
                    st.markdown(f"**Best Time to Visit:** {monument_details.get('best_time_to_visit', '—')}")
                    st.markdown(f"**Entry Fee:** {monument_details.get('entry_fee', '—')}")
                    st.markdown("")
                    st.info("Please follow sustainable tourism guidelines → Visit the Sustainability tab for tips!")

                # Auto-scroll to detailed info after upload
                components.html(
                    "<script>setTimeout(function(){ window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'}); }, 400);</script>",
                    height=0,
                )
            else:
                st.markdown("---")
                st.info("📚 Detailed information for this monument is being added. Try with a Taj Mahal image!")
    else:
        st.info("📸 Upload a monument image to begin recognition")
        if st.session_state.get("monument_result") is not None:
            del st.session_state["monument_result"]
        if st.session_state.get("monument_details") is not None:
            del st.session_state["monument_details"]

# -----------------------------------------------------------------------------
# AI Chatbot page
# -----------------------------------------------------------------------------
elif selected_page == "🤖 AI Chatbot":
    st.markdown("## 🤖 AI Heritage Chatbot")

    monument_result = st.session_state.get("monument_result")
    if monument_result is None or monument_result.get("monument_name", "Unknown") == "Unknown":
        monument_name = "Taj Mahal"
        st.info("🏛️ Chatting about: **Taj Mahal** — Upload an image in Monument Recognition to switch monuments.")
    else:
        monument_name = monument_result.get("monument_name", "Taj Mahal")
        st.success(f"🏛️ Chatting about: {monument_name}")

    # Display chat history
    for message in st.session_state["chat_history"]:
        role = message.get("role", "")
        content = message.get("content", "")
        if role == "user":
            with st.chat_message("user"):
                st.write(content)
        elif role == "assistant":
            with st.chat_message("assistant"):
                st.write(content)

    # Chat input
    user_input = st.chat_input(f"Ask anything about {monument_name}...")

    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        with st.spinner("🤔 Thinking..."):
            try:
                response = get_demo_response(user_input, monument_name)
            except Exception as e:
                response = f"I'd be happy to tell you about {monument_name}. Please ask me anything about its history, architecture, or culture!"

        st.session_state["chat_history"].append({"role": "assistant", "content": response})
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state["chat_history"] = []
        st.rerun()

# -----------------------------------------------------------------------------
# Sustainability page
# -----------------------------------------------------------------------------
elif selected_page == "🌿 Sustainability":
    st.markdown("## Sustainable & Responsible Tourism")

    monument_result = st.session_state.get("monument_result")
    if monument_result is None or monument_result.get("monument_name", "Unknown") == "Unknown":
        monument_name = "Taj Mahal"
    else:
        monument_name = monument_result.get("monument_name", "Taj Mahal")

    st.success(f"🌿 Sustainability tips for: {monument_name}")

    monument_details = st.session_state.get("monument_details")
    if "sustainability_tips" not in st.session_state or st.session_state.get("last_monument") != monument_name:
        with st.spinner("🌱 Loading sustainability tips..."):
            tips = get_demo_sustainability_tips(monument_name)
            st.session_state["sustainability_tips"] = tips
            st.session_state["last_monument"] = monument_name
            st.toast("Sustainability tips ready!", icon="🌿")

    tips = st.session_state.get("sustainability_tips", get_demo_sustainability_tips(monument_name))

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown('<div class="heritage-card">', unsafe_allow_html=True)
        st.markdown("### 🌱 Environmental Tips")
        for tip in tips.get("environmental_tips", []):
            st.markdown(f"• {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown('<div class="heritage-card">', unsafe_allow_html=True)
        st.markdown("### 🏛️ Cultural Respect")
        for tip in tips.get("cultural_tips", []):
            st.markdown(f"• {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

    with s3:
        st.markdown('<div class="heritage-card">', unsafe_allow_html=True)
        st.markdown("### 📸 Responsible Photography")
        for tip in tips.get("photography_tips", []):
            st.markdown(f"• {tip}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    conservation_message = tips.get("conservation_message", "")
    if conservation_message:
        st.info(f"💚 {conservation_message}")

# -----------------------------------------------------------------------------
# Quiz page
# -----------------------------------------------------------------------------
elif selected_page == "🧠 Quiz":
    st.markdown("## 🧠 Heritage Knowledge Quiz")

    monument_result = st.session_state.get("monument_result")
    if monument_result is None or monument_result.get("monument_name", "Unknown") == "Unknown":
        monument_name = "Taj Mahal"
    else:
        monument_name = monument_result.get("monument_name", "Taj Mahal")

    if st.session_state.get("quiz_questions") is None or st.session_state.get("last_quiz_monument") != monument_name:
        quiz_questions = get_quiz_questions(monument_name)
        if quiz_questions:
            st.session_state["quiz_questions"] = quiz_questions
            st.session_state["last_quiz_monument"] = monument_name
            st.session_state["quiz_started"] = False
            st.session_state["quiz_completed"] = False
            st.session_state["current_question_index"] = 0
            st.session_state["quiz_answers"] = []
        else:
            st.info(f"📚 Quiz questions for {monument_name} are being added. Try with a Taj Mahal image!")
            st.stop()

    quiz_questions = st.session_state.get("quiz_questions", [])
    current_index = st.session_state.get("current_question_index", 0)
    quiz_started = st.session_state.get("quiz_started", False)
    quiz_completed = st.session_state.get("quiz_completed", False)
    quiz_answers = st.session_state.get("quiz_answers", [])

    st.success(f"🏛️ Quiz about: {monument_name}")

    if not quiz_started and not quiz_completed:
        st.markdown(f"**Test your knowledge about {monument_name}!**")
        st.markdown(f"This quiz has {len(quiz_questions)} questions.")
        if st.button("🚀 Start Quiz", type="primary"):
            st.session_state["quiz_started"] = True
            st.session_state["current_question_index"] = 0
            st.session_state["quiz_answers"] = []
            st.rerun()

    elif quiz_started and not quiz_completed:
        if current_index < len(quiz_questions):
            question_data = quiz_questions[current_index]
            question = question_data.get("question", "")
            options = question_data.get("options", [])
            answer = question_data.get("answer", "")

            st.markdown("---")
            st.markdown(f"### Question {current_index + 1} of {len(quiz_questions)}")
            st.markdown(f"**{question}**")

            selected_option = st.radio(
                "Select your answer:",
                options=options,
                key=f"quiz_option_{current_index}",
                label_visibility="collapsed",
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("✅ Submit Answer", type="primary"):
                    is_correct = selected_option == answer
                    quiz_answers.append({
                        "question": question,
                        "selected": selected_option,
                        "correct": answer,
                        "is_correct": is_correct,
                        "explanation": question_data.get("explanation", ""),
                    })
                    st.session_state["quiz_answers"] = quiz_answers
                    if current_index + 1 < len(quiz_questions):
                        st.session_state["current_question_index"] = current_index + 1
                    else:
                        st.session_state["quiz_completed"] = True
                        correct_count = sum(1 for ans in quiz_answers if ans.get("is_correct", False))
                        st.toast(f"Quiz complete! Score: {correct_count}/{len(quiz_questions)}", icon="🧠")
                    st.rerun()
            with col2:
                if current_index > 0:
                    if st.button("⬅️ Previous"):
                        st.session_state["current_question_index"] = current_index - 1
                        st.rerun()

    elif quiz_completed:
        st.markdown("---")
        st.markdown("### 🎉 Quiz Completed!")

        correct_count = sum(1 for ans in quiz_answers if ans.get("is_correct", False))
        total_questions = len(quiz_answers)
        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0

        st.markdown(f"**Your Score: {correct_count}/{total_questions} ({score_percentage:.0f}%)**")

        if score_percentage == 100:
            st.success("🌟 Perfect score! You're a heritage expert!")
            st.snow()
        elif score_percentage >= 80:
            st.success("🎯 Excellent! Great knowledge of Indian heritage!")
        elif score_percentage >= 60:
            st.info("👍 Good job! Keep learning about India's monuments!")
        else:
            st.warning("📚 Keep studying! Visit the monument details to learn more!")

        st.markdown("---")
        st.markdown("### 📋 Review Your Answers:")
        for idx, ans in enumerate(quiz_answers):
            with st.expander(f"Question {idx + 1}: {ans.get('question', '')}"):
                if ans.get("is_correct", False):
                    st.success(f"✅ Correct! You selected: {ans.get('selected', '')}")
                else:
                    st.error(f"❌ Incorrect. You selected: {ans.get('selected', '')}")
                    st.info(f"✅ Correct answer: {ans.get('correct', '')}")
                st.markdown(f"**Explanation:** {ans.get('explanation', '')}")

        if st.button("🔄 Retake Quiz"):
            st.session_state["quiz_started"] = False
            st.session_state["quiz_completed"] = False
            st.session_state["current_question_index"] = 0
            st.session_state["quiz_answers"] = []
            st.rerun()

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("""
<div style="
  margin-top: 4rem;
  padding: 1.5rem 0;
  border-top: 1px solid rgba(201,168,76,0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
">
  <span style="font-family:'DM Mono',monospace; font-size:0.72rem; color:#5C5445; letter-spacing:0.08em;">
    SANSKRITI AI &copy; 2025
  </span>
  <span style="font-family:'DM Mono',monospace; font-size:0.72rem; color:#5C5445; letter-spacing:0.08em;">
    BUILT WITH &hearts; FOR INDIA'S HERITAGE
  </span>
</div>
""", unsafe_allow_html=True)