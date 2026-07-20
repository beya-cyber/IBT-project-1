import streamlit as st
import time
import hashlib
import random
from datetime import datetime

# ==========================================
# 0. CONFIGURATION & ENTERPRISE STYLING LAYER
# ==========================================
st.set_page_config(page_title="LUCY CORE V2", page_icon="🇪🇹", layout="wide", initial_sidebar_state="expanded")

# Telegram Dark Mode + TikTok Immersive Media Layout Styling Map
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #182533; color: #f5f5f5; }

    /* Telegram Left Sidebar Chat List */
    .tg-chat-item {
        display: flex;
        align-items: center;
        padding: 10px 12px;
        border-radius: 10px;
        margin-bottom: 4px;
    }
    .tg-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: #2b5278;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1.1rem;
        color: white;
        margin-right: 12px;
    }
    .tg-chat-info { flex: 1; min-width: 0; }
    .tg-chat-title-row { display: flex; justify-content: space-between; align-items: center; }
    .tg-chat-name { font-weight: 500; font-size: 0.95rem; color: #fff; }
    .tg-chat-time { font-size: 0.75rem; color: #7f91a4; }
    .tg-chat-preview { font-size: 0.85rem; color: #7f91a4; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px; }
    .tg-badge { background: #4e82b4; color: white; border-radius: 10px; padding: 2px 7px; font-size: 0.75rem; font-weight: 600; }

    /* Telegram Chat Window Header */
    .tg-header {
        background: #17212b;
        padding: 10px 20px;
        border-bottom: 1px solid #101921;
        margin-top: -10px;
        margin-bottom: 15px;
    }
    .tg-header-title { font-weight: 500; font-size: 1.05rem; color: #fff; }
    .tg-header-subtitle { font-size: 0.8rem; color: #527596; }

    /* Telegram Chat Bubbles Container */
    .tg-chat-box {
        background-color: #0e1621;
        border-radius: 12px;
        padding: 20px;
        height: 480px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 8px;
        border: 1px solid #101921;
    }
    .tg-bubble {
        padding: 8px 14px;
        border-radius: 12px;
        font-size: 0.92rem;
        max-width: 65%;
        line-height: 1.4;
        position: relative;
        color: #f5f5f5;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .tg-bubble-in { background: #182533; align-self: flex-start; border-top-left-radius: 4px; }
    .tg-bubble-out { background: #2b5278; align-self: flex-end; border-top-right-radius: 4px; }
    .tg-bubble-meta { font-size: 0.68rem; color: #7f91a4; text-align: right; margin-top: 4px; float: right; margin-left: 15px; }

    /* ==========================================
       TIKTOK IMMERSIVE INTERFACE SYSTEM DESIGN
       ========================================== */
    .tiktok-wrapper {
        max-width: 420px;
        margin: 0 auto 30px auto;
        background: #000000;
        border-radius: 16px;
        overflow: hidden;
        position: relative;
        border: 4px solid #202b36;
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }
    .tiktok-video-container {
        position: relative;
        width: 100%;
        background: #000;
    }
    /* Lower overlay targeting description details */
    .tiktok-meta-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 30px 80px 20px 16px;
        background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.4) 60%, rgba(0,0,0,0) 100%);
        z-index: 10;
        pointer-events: none;
    }
    .tiktok-author {
        font-weight: 700;
        font-size: 1.05rem;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .tiktok-description {
        font-size: 0.9rem;
        color: #e5e7eb;
        line-height: 1.3;
        margin-bottom: 8px;
    }
    .tiktok-music {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.8rem;
        color: #a1a1aa;
    }
    /* Floating action dock columns logic configuration */
    .tiktok-action-dock {
        position: absolute;
        bottom: 40px;
        right: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 18px;
        z-index: 20;
    }
    .tiktok-avatar-container {
        position: relative;
        margin-bottom: 10px;
    }
    .tiktok-avatar-img {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        border: 2px solid #ffffff;
        background: #fe2c55;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1rem;
    }
    .tiktok-avatar-plus {
        position: absolute;
        bottom: -5px;
        left: 50%;
        transform: translateX(-50%);
        background: #fe2c55;
        color: white;
        border-radius: 50%;
        width: 18px;
        height: 18px;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    .tiktok-metric-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #ffffff;
        margin-top: -2px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. CORE PERSISTENT STATE ARCHITECTURE
# ==========================================
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.chat_db = [
        {"id": 1, "room": "Tech Ethiopia 🇪🇹", "type": "Group", "sender": "Behailu (Beya)",
         "msg": "ሰላም ለሁሉም! ይህ የሉሲ አዲስ የመገናኛ ዘዴ ነው:: 🙌", "time": "20:30"},
        {"id": 2, "room": "Lucy Announcements 📢", "type": "Channel", "sender": "Lucy System Node",
         "msg": "Welcome to Lucy Core. Optimized for local languages and secure global diaspora connections.",
         "time": "20:32"}
    ]
    st.session_state.posts_db = [
        {"id": 101, "author": "BeyaTech", "title": "Building production systems with Streamlit & OOP 🐍", "likes": 1240,
         "shares": 345, "video": "https://www.w3schools.com/html/mov_bbb.mp4"},
        {"id": 102, "author": "CyberSec_ET", "title": "Network Port Scanning & Defense Systems Matrix 🛡️",
         "likes": 4512, "shares": 928, "video": "https://www.w3schools.com/html/movie.mp4"}
    ]

# ==========================================
# 2. GLOBAL LOCALIZATION ENGINE MATRIX
# ==========================================
st.sidebar.markdown(
    "<h1 style='color: #4e82b4; font-size: 2.2rem; font-weight: 700; margin-bottom:0;'>🇪🇹 LUCY CORE</h1>",
    unsafe_allow_html=True)
st.sidebar.markdown(
    "<p style='color: #7f91a4; font-size: 0.85rem; margin-top:-5px; letter-spacing:0.05em;'>ADVANCED ENGINE</p>",
    unsafe_allow_html=True)
st.sidebar.markdown("---")

current_lang = st.sidebar.selectbox("🌐 LANGUAGE / ቋንቋ", ["English", "አማርኛ (Amharic)", "Afaan Oromoo"])

ui_lexicon = {
    "English": {
        "nav": "NAVIGATION MATRIX", "chat": "💬 Telegram Chat", "feed": "📺 TikTok Immersive Feed",
        "vid": "📹 Video Classroom", "ai": "🧠 System AI Hub",
        "chat_cap": "Structural replication of the Telegram architecture engine.",
        "post_cap": "TikTok vertical format video engine layout simulation."
    },
    "አማርኛ (Amharic)": {
        "nav": "ዋና ማውጫ", "chat": "💬 ቴሌግራም ቻት", "feed": "📺 ቲክቶክ ቪዲዮ መጋቢ", "vid": "📹 ቀጥታ የቪዲዮ ስብሰባ",
        "ai": "🧠 ሉሲ አርቲፊሻል ኢንተለጀንስ",
        "chat_cap": "የቴሌግራም መዋቅር ልክ እንደ ዋናው መተግበሪያ።", "post_cap": "የቲክቶክ ቪዲዮ ቅርፅ እና ቀጥታ የመስተጋብር ቁልፎች።"
    }
}.get(current_lang, {
    "nav": "NAVIGATION MATRIX", "chat": "💬 Telegram Chat", "feed": "📺 TikTok Immersive Feed",
    "vid": "📹 Video Classroom", "ai": "🧠 System AI Hub",
    "chat_cap": "Structural replication of the Telegram architecture engine.",
    "post_cap": "TikTok vertical format video engine layout simulation."
})

selected_view = st.sidebar.radio(ui_lexicon["nav"],
                                 [ui_lexicon["chat"], ui_lexicon["feed"], ui_lexicon["vid"], ui_lexicon["ai"]])

# ==========================================
# SECTION 1: TELEGRAM CHAT WINDOW
# ==========================================
if selected_view == ui_lexicon["chat"]:
    st.caption(ui_lexicon["chat_cap"])
    tg_col1, tg_col2 = st.columns([1.1, 3])

    with tg_col1:
        st.markdown("<h3 style='font-size:1.1rem; color:#7f91a4; margin-bottom:12px;'>Chats</h3>",
                    unsafe_allow_html=True)
        target_room = st.radio("Switch Chat Room", ["Tech Ethiopia 🇪🇹 [Group]", "Lucy Announcements 📢 [Channel]"],
                               label_visibility="collapsed")
        clean_room_name = target_room.split(" [")[0]
        room_type = "Channel" if "Channel" in target_room else "Group"
        room_meta = "4,120 subscribers" if room_type == "Channel" else "248 members, 42 online"

    with tg_col2:
        st.markdown(
            f'<div class="tg-header"><div class="tg-header-title">{clean_room_name}</div><div class="tg-header-subtitle">{room_meta}</div></div>',
            unsafe_allow_html=True)
        st.markdown("<div class='tg-chat-box'>", unsafe_allow_html=True)
        for msg in st.session_state.chat_db:
            if msg["room"] == clean_room_name or msg["type"] == "Channel":
                is_me = msg["sender"] == "Behailu (Beya)"
                st.markdown(
                    f'<div class="tg-bubble {"tg-bubble-out" if is_me else "tg-bubble-in"}"><div>{msg["msg"]}</div><div class="tg-bubble-meta">{msg["time"]}</div><div style="clear: both;"></div></div>',
                    unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.form(key="tg_input", clear_on_submit=True):
            in_c1, in_c2, in_c3 = st.columns([0.4, 4, 0.6])
            with in_c2: typed_msg = st.text_input("Message", placeholder="Write a message...",
                                                  label_visibility="collapsed")
            with in_c3:
                if st.form_submit_button("🚀 Send") and typed_msg:
                    st.session_state.chat_db.append(
                        {"room": clean_room_name, "type": room_type, "sender": "Behailu (Beya)", "msg": typed_msg,
                         "time": datetime.now().strftime("%H:%M")})
                    st.rerun()

# ==========================================
# SECTION 2: TIKTOK IMMERSIVE FEED LAYER
# ==========================================
elif selected_view == ui_lexicon["feed"]:
    st.caption(ui_lexicon["post_cap"])

    t_layout_left, t_layout_center, t_layout_right = st.columns([1, 1.5, 1])

    with t_layout_left:
        st.markdown("<div style='background:#17212b; padding:16px; border-radius:12px;'>", unsafe_allow_html=True)
        st.markdown("### 🎬 Creator Studio")
        feed_title = st.text_input("Caption/Description")
        feed_file = st.file_uploader("Upload Clip", type=["mp4"])
        if st.button("🚀 Share to Feed Stream", use_container_width=True) and feed_title:
            st.session_state.posts_db.insert(0, {
                "id": random.randint(1000, 9999), "author": "Behailu_Beya", "title": feed_title, "likes": 0,
                "shares": 0, "video": "https://www.w3schools.com/html/mov_bbb.mp4"
            })
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with t_layout_center:
        # Loop over current posts to construct vertical TikTok containers
        for idx, post in enumerate(st.session_state.posts_db):
            st.markdown(f"""
            <div class="tiktok-wrapper">
                <div class="tiktok-video-container">
                    <!-- Text Metadata Elements Stacked inside Container Boundary -->
                    <div class="tiktok-meta-overlay">
                        <div class="tiktok-author">@{post['author']}</div>
                        <div class="tiktok-description">{post['title']}</div>
                        <div class="tiktok-music">🎵 Original Sound - @{post['author']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Use standard stream framework directly inside the layout center position
            st.video(post["video"])

            # Interactive Dock Component Layout built out using precise horizontal sub-columns
            dock_col1, dock_col2, dock_col3 = st.columns(3)
            with dock_col1:
                if st.button(f"❤️ {post['likes']}", key=f"tk_l_{post['id']}", use_container_width=True):
                    st.session_state.posts_db[idx]["likes"] += 1
                    st.rerun()
            with dock_col2:
                if st.button(f"🔗 {post['shares']}", key=f"tk_s_{post['id']}", use_container_width=True):
                    st.session_state.posts_db[idx]["shares"] += 1
                    st.toast("Link copied to clipboard structure!")
                    st.rerun()
            with dock_col3:
                if st.button("🌐 Translate", key=f"tk_t_{post['id']}", use_container_width=True):
                    st.info(f"**AI Transliteration Matrix:**\n* ማሳሰቢያ: {post['title']}")

            st.markdown("<hr style='border:1px solid #202b36;' />", unsafe_allow_html=True)

# ==========================================
# SECTION 3: VIDEO CONFERENCING
# ==========================================
elif selected_view == "📹 Video Classroom":
    st.markdown("<div class='tg-chat-box'>P2P Signaling Engine Active. Complete Camera Authorization.</div>",
                unsafe_allow_html=True)

# ==========================================
# SECTION 4: SYSTEM AI HUB
# ==========================================
elif selected_view == "🧠 System AI Hub":
    st.markdown("### Lucy System AI Node Engine")
    st.text_input("Query Core", placeholder="Analyze Python infrastructure matrices...")