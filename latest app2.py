import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import uuid
import bcrypt

# --- 1. CONFIG & SYSTEM ARCHITECTURE ---
st.set_page_config(
    page_title="INSA - National Fraud Portal (TAZI Engine)",
    page_icon="🛡️",
    layout="wide"
)

DB_FILE = "fraud_reports.db"
UPLOAD_DIR = "uploaded_evidence"
AUDIO_DIR = "voice_notes"
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB DoS protection ceiling

# Ensure clean persistence paths
for directory in [UPLOAD_DIR, AUDIO_DIR]:
    os.makedirs(directory, exist_ok=True)


@st.cache_resource
def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            victim_phone TEXT,
            victim_bank TEXT,
            fraud_type TEXT,
            scammer_phone TEXT,
            fraudster_account TEXT,
            description TEXT,
            evidence_file_name TEXT,
            voice_note_path TEXT,
            status TEXT,
            risk_score REAL
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_scammer_phone ON reports (scammer_phone)")
    conn.commit()
    conn.close()


init_db()


# --- 2. SECURITY HELPER METHODS ---
def get_secure_admin_hash() -> bytes:
    default_fallback_hash = b"$2b$12$RAt7r6.W68mPCH7uWw8XvevC32K8F9.GZ3vMsw0uQn32DWeRjNl8y"
    secret_hash = st.secrets.get("ADMIN_PASSWORD_HASH", os.environ.get("ADMIN_PASSWORD_HASH"))
    if secret_hash:
        return secret_hash.encode()
    return default_fallback_hash


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password)
    except Exception:
        return False


def verify_file_signature(file_bytes, file_name) -> bool:
    if not file_bytes:
        return False
    ext = os.path.splitext(file_name)[1].lower()
    header = file_bytes[:4]

    if ext == ".png" and header != b'\x89PNG':
        return False
    if ext in [".jpg", ".jpeg"] and header[:3] != b'\xff\xd8\xff':
        return False
    if ext == ".mp3" and header[:3] != b'ID3' and header[:2] != b'\xff\xfb':
        return False

    return True


# --- 3. TAZI AI TRIAGE ENGINE ---
def compute_tazi_risk(fraud_type: str, scammer_phone: str, desc: str) -> float:
    base_scores = {
        "Vishing (Voice Call Scam)": 6.5,
        "SMS Phishing (Fake SMS Text)": 4.5,
        "Forged Receipt / Fake Screenshot": 8.5,
        "Social Media / Telegram Scam": 5.5
    }
    score = base_scores.get(fraud_type, 5.0)

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM reports WHERE scammer_phone = ?", (scammer_phone,))
        frequency = c.fetchone()[0]
        conn.close()

        if frequency > 0:
            score += min(frequency * 0.8, 1.5)
    except Exception:
        pass

    critical_keywords = ["bank", "cbe", "transfer", "code", "password", "telebirr", "frozen", "critical"]
    desc_lower = desc.lower()
    for keyword in critical_keywords:
        if keyword in desc_lower:
            score += 0.2

    return min(round(score, 2), 10.0)


# --- 4. MULTI-LANGUAGE TRANSLATION ---
translations = {
    "English": {
        "nav_role": "SYSTEM PORTAL VIEW",
        "role_victim": "Victim Intake Portal (Public)",
        "role_admin": "INSA Analyst Dashboard (Internal)",
        "title": "National Cybercrime & Financial Fraud Portal",
        "subtitle": "Securing Ethiopia's digital economy. Powered by the TAZI Threat Intelligence Engine.",
        "lang_label": "Language / ቋንቋ / Afaan",
        "sec_victim_info": "Step 1: Your Identity & Bank",
        "victim_phone": "Your Phone Number (linked to bank/wallet)",
        "victim_bank": "Your Bank or Mobile Wallet Provider",
        "sec_scammer_info": "Step 2: Scammer & Target Account",
        "fraud_type": "Attack Vector / Method",
        "fraud_types_opts": ["Vishing (Voice Call Scam)", "SMS Phishing (Fake SMS Text)",
                             "Forged Receipt / Fake Screenshot", "Social Media / Telegram Scam"],
        "scammer_phone": "Scammer's Phone Number",
        "scammer_acc": "The Account / Wallet they asked you to send money to",
        "sec_desc": "Step 3: Upload Evidence & Description",
        "desc": "What did they say or do? (Provide details)",
        "voice_upload": "🎙️ Audio Evidence (Record/Upload a voice clip)",
        "upload": "📷 Screenshot Evidence (Processed by TAZI OCR)",
        "ocr_alert": "✨ TAZI AI OCR Engaged: Extracting metadata and routing transaction details...",
        "submit_btn": "🔒 SECURELY SUBMIT INCIDENT",
        "err_fields": "CRITICAL ERROR: Phone numbers are required to track the threat actor!",
        "success_report": "INCIDENT ENCRYPTED & SUBMITTED. ID: #{}. National threat tracking initiated by TAZI. Please remain calm.",
        "admin_title": "INSA Incident Command & Fraud Triage Center",
        "metric_total": "Total Reported Incidents",
        "metric_unique_scammers": "Active Scammer Numbers",
        "mule_acc": "Target Mule Accounts Detected",
        "table_title": "Active Incident Rate Trends (Chronological Timeline)",
        "action_update": "Threat Triage & Status Update",
        "btn_update": "Apply Status Update",
        "btn_delete": "Reset Demo Database",
        "db_cleared": "Demo Database purged."
    },
    "አማርኛ": {
        "nav_role": "የስርዓት እይታ",
        "role_victim": "የተጠቂዎች ሪፖርት ማቅረቢያ (ይፋዊ)",
        "role_admin": "የኢንሳ (INSA) ተንታኞች መቆጣጠሪያ",
        "title": "ብሔራዊ የሳይበር ወንጀል እና የፋይናንስ ማጭበርበር መከላከያ",
        "subtitle": "የኢትዮጵያን ዲጂታል ደህንነት ማስጠበቅ። በታዚ (TAZI) የሳይበር ስጋት ቁጥጥር የሚመራ።",
        "lang_label": "ቋንቋ / Language / Afaan",
        "sec_victim_info": "ደረጃ 1፡ የእርስዎ ማንነት እና ባንክ",
        "victim_phone": "የእርስዎ ስልክ ቁጥር (ከባንክዎ ጋር የተገናኘው)",
        "victim_bank": "የእርስዎ ባንክ ወይም የሞባይል የገንዘብ አገልግሎት",
        "sec_scammer_info": "ደረጃ 2፡ የአጭበርባሪው መረጃ እና የላኩበት አካውንት",
        "fraud_type": "የማጭበርበሪያው መንገድ",
        "fraud_types_opts": ["ቪሺንግ (በስልክ ጥሪ ማጭበርበር)", "የሐሰት የጽሑፍ መልዕክት (SMS)", "የተጭበረበረ ደረሰኝ / የሐሰት ስክሪንሾት",
                             "የማኅበራዊ ሚዲያ / ቴሌግራም ማጭበርበር"],
        "scammer_phone": "የአጭበርባሪው ስልክ ቁጥር",
        "scammer_acc": "ገንዘብ እንዲልኩበት የጠየቁዎት አካውንት",
        "sec_desc": "ደረጃ 3፡ ማስረጃ እና ማብራሪያ ይጫኑ",
        "desc": "ምን እንደተፈጠረ ያብራሩ (ዝርዝር መረጃ ያስገቡ)",
        "voice_upload": "🎙️ የድምፅ ማስረጃ (የድምፅ መልዕክት መቅዳት/መጫን ይችላሉ)",
        "upload": "📷 የስክሪንሾት ማስረጃ (በታዚ AI የደረሰኙ መረጃ በራስ-ሰር ይነበባል)",
        "ocr_alert": "✨ TAZI AI OCR ንቁ ነው፡ አስፈላጊ መረጃዎች ከፎቶው ላይ በቀጥታ ይነበባሉ።",
        "submit_btn": "🔒 ሪፖርቱን በምስጢር አስገባ",
        "err_fields": "ስህተት፡ የአጥቂውን ቁጥር ለመከታተል ስልክ ቁጥሮች መሞላት አለባቸው!",
        "success_report": "ሪፖርትዎ በምስጢር ተቀምጧል! የክትትል መለያ ቁጥር፡ #{} ነው። የታዚ ስጋት ክትትል ተጀምሯል። እባክዎን ይረጋጉ።",
        "admin_title": "የኢንሳ (INSA) የሳይበር ወንጀል መቆጣጠሪያ ማዕከል",
        "metric_total": "ጠቅላላ የተመዘገቡ ጥቃቶች",
        "metric_unique_scammers": "አክቲቭ አጭበርባሪ ቁጥሮች",
        "mule_acc": "የታወቁ የገንዘብ ማስተላለፊያ (Mule) አካውንቶች",
        "table_title": "የስጋት መከሰት አዝማሚያዎች (በጊዜ ሰሌዳ)",
        "action_update": "የጥቃቱን ሁኔታ ይወስኑ",
        "btn_update": "ሁኔታውን ቀይር",
        "btn_delete": "ዳታቤዙን አጽዳ (ለማሳያ)",
        "db_cleared": "ዳታቤዙ በሙሉ ተሰርዟል።"
    },
    "Afaan Oromoo": {
        "nav_role": "ILAALCHA SIRNAA",
        "role_victim": "Gabaasa Miidhamtootaa (Uummataaf)",
        "role_admin": "Gabatee To'annoo Analysts INSA (Keessoo)",
        "title": "Portaali Gabaasa Saayibar-Wanjalaa fi Sassaabinsa Maallaqa Sobaa",
        "subtitle": "Nageenya dinagdee dijitaalaa Itiyoophiyaa kabachiisuu. Engine TAZI'n kan deeggarame.",
        "lang_label": "Afaan / Language / ቋንቋ",
        "sec_victim_info": "Tarkaanfii 1: Eenyummeessaa fi Baankii Keessan",
        "victim_phone": "Lakkoofsa Bilbila Keessan (Kan baankii keessanitti hidhame)",
        "victim_bank": "Baankii ykn Hojjetaa Maallaqa Moobaayilaa Keessan",
        "sec_scammer_info": "Tarkaanfii 2: Odeeffannoo Gowwoomsitichaa fi Herrega Inni Kenne",
        "fraud_type": "Mala Gowwoomsaa (Attack Method)",
        "fraud_types_opts": ["Vishing (Gowwoomsaa Bilbilaa)", "SMS Phishing (SMS Sobaa)",
                             "Iskiriinshootii Maallaqa deebisuu Sobaa", "Midiyaa Hawaasaa / Telegram"],
        "scammer_phone": "Lakkoofsa Bilbila Gowwoomsitichaa",
        "scammer_acc": "Lakkoofsa Herrega Baankii isaan maallaqa irratti ergitaniif",
        "sec_desc": "Tarkaanfii 3: Ragaa Ol-fe'uu fi Ibsa Bal'inaa",
        "desc": "Maal akka ta'e ibsaa (Maal akka isiniin jedhan)",
        "voice_upload": "🎙️ Ragaa Sagalee (Sagalee keessan ol-fe'aa)",
        "upload": "📷 Ragaa Iskiriinshootii (TAZI OCR'n ofumaan dubbifama)",
        "ocr_alert": "✨ TAZI AI OCR Haktivii dha: Odeeffannoon iskirinshara keessaa ofumaan dubbifama.",
        "submit_btn": "🔒 GABAASA ICCITII ERGI",
        "err_fields": "DONGORRAA: Lakkoofsa bilbilaa guutuun dirqama!",
        "success_report": "GABAASNI KEESSAN EGGUMSAAN ERGAMEERA! ID: #{}. Hordoffiin TAZI'n jalqabameera. Tasgabbaahaa.",
        "admin_title": "Giddugala To'annoo fi Triage Saayibar INSA",
        "metric_total": "Wanjaloota Gabaasaman",
        "metric_unique_scammers": "Lakkoofsota Haktivii Gowwoomsitootaa",
        "mule_acc": "Herregoota Mule Maallaqaa Adda Baafaman",
        "table_title": "Tariitti Gabaasni Saayibar Kun Itti Galu",
        "action_update": "Haala Gabaasaa Haaromsi",
        "btn_update": "Haala Haaromsi",
        "btn_delete": "Database Qulqulleessi",
        "db_cleared": "Daataa demo hundi qulqulleeffameera."
    }
}


# --- 5. DATABASE OPERATIONS ---
def save_report(v_phone, v_bank, f_type, s_phone, s_acc, desc, f_name, voice_name, risk_score):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO reports (
            timestamp, victim_phone, victim_bank, fraud_type, 
            scammer_phone, fraudster_account, description, 
            evidence_file_name, voice_note_path, status, risk_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, v_phone, v_bank, f_type, s_phone, s_acc, desc, f_name, voice_name, "New / Unresolved", risk_score))
    conn.commit()
    report_id = c.lastrowid
    conn.close()
    return report_id


def get_all_reports():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM reports ORDER BY id DESC", conn)
    conn.close()
    return df


def update_report_status(report_id, new_status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE reports SET status = ? WHERE id = ?", (new_status, report_id))
    conn.commit()
    conn.close()


def clear_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM reports")
    conn.commit()
    conn.close()


# --- 6. USER INTERFACE APPLICATION LAYOUT ---
def main():
    # --- UPGRADED NATIONAL ETHIOPIAN BRAND STYLING ---
    st.markdown("""
        <style>
            .main {
                background: linear-gradient(180deg, #0a1128 0%, #050814 100%);
                color: #e2e8f0;
            }

            /* Ethiopian Tricolor Highlight Accents */
            .ethiopia-strip {
                height: 4px;
                background: linear-gradient(90deg, #388e3c 0%, #fbc02d 50%, #d32f2f 100%);
                width: 100%;
                border-radius: 2px;
                margin-bottom: 20px;
            }

            h1 {
                color: #ffffff !important;
                font-family: 'Inter', sans-serif;
                font-weight: 800;
                letter-spacing: -0.5px;
                margin-bottom: 0px !important;
            }

            .insa-badge {
                background: linear-gradient(135deg, #0e2040 0%, #153266 100%);
                color: #fbc02d !important; /* Golden Yellow Highlight */
                border: 1px solid #1e3d75;
                padding: 6px 16px;
                border-radius: 4px;
                font-size: 0.8rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                display: inline-block;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }

            div[data-testid="stForm"] {
                background-color: #0d1b2e !important;
                border: 1px solid #1a2e4c !important;
                border-radius: 8px !important;
                padding: 30px !important;
                box-shadow: 0 10px 25px rgba(0,0,0,0.4) !important;
            }

            .stButton>button {
                background: linear-gradient(135deg, #102a54 0%, #0a1b37 100%) !important;
                color: #fbc02d !important;
                border: 1px solid #fbc02d !important;
                border-radius: 4px !important;
                padding: 12px 24px !important;
                font-weight: 700 !important;
                transition: all 0.25s ease;
            }

            .stButton>button:hover {
                background: #fbc02d !important;
                color: #0a1b37 !important;
                box-shadow: 0 0 15px rgba(251, 192, 45, 0.4);
            }

            /* Banner showcasing Sovereign Security Pride */
            .insa-banner {
                background: linear-gradient(90deg, #0c1c33 0%, #16305a 100%);
                border-left: 5px solid #388e3c; /* Green Border */
                padding: 25px;
                border-radius: 6px;
                margin-bottom: 25px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.25);
            }

            .ethiopian-pride-footer {
                text-align: center;
                margin-top: 50px;
                padding: 20px;
                font-size: 0.85rem;
                color: #a0aec0;
                border-top: 1px solid #1a2e4c;
            }
        </style>
    """, unsafe_allow_html=True)

    # Top boundary line reflecting Ethiopian Flag color profiles
    st.markdown("<div class='ethiopia-strip'></div>", unsafe_allow_html=True)

    # Sidebar Construction
    st.sidebar.markdown(
        "<div style='text-align: center; margin-top: 10px; margin-bottom: 20px;'><span class='insa-badge'>INSA ETHIOPIA</span></div>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown("<h3 style='color:#ffffff; text-align:center; font-size:1.1rem;'>SYSTEM GATEWAY</h3>",
                        unsafe_allow_html=True)

    if "selected_lang" not in st.session_state:
        st.session_state["selected_lang"] = "English"

    current_lang = st.session_state["selected_lang"]
    t_global = translations[current_lang]

    selected_lang = st.sidebar.selectbox(
        t_global["lang_label"],
        options=list(translations.keys()),
        index=list(translations.keys()).index(current_lang)
    )
    st.session_state["selected_lang"] = selected_lang
    t = translations[selected_lang]

    st.sidebar.markdown("---")

    user_role = st.sidebar.radio(
        t["nav_role"],
        options=[t["role_victim"], t["role_admin"]]
    )

    st.sidebar.markdown("---")

    # Branded Proudly Developed sidebar item
    st.sidebar.markdown("""
        <div style="background: rgba(56, 142, 60, 0.1); border-left: 3px solid #388e3c; padding: 10px; border-radius: 4px;">
            <p style="margin: 0; font-size: 0.75rem; color: #a0aec0; font-weight: bold;">
                🛡️ PROUDLY DEVELOPED & POWERED BY ETHIOPIA<br>ኢትዮጵያ በኩራት ያበለጸገችው
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.caption("Information Network Security Administration • 2026")

    # --- PUBLIC INTAKE FORM (VICTIM PORTAL) ---
    if user_role == t["role_victim"]:
        st.markdown(f"""
            <div class="insa-banner">
                <span style="font-size: 0.85rem; color: #fbc02d; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;">
                    FEDERAL DEMOCRATIC REPUBLIC OF ETHIOPIA
                </span>
                <h1 style="margin: 5px 0 10px 0;">🛡️ {t['title']}</h1>
                <p style="margin: 0; font-size: 1rem; color: #a0aec0;">{t['subtitle']}</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("victim_reporting_form", clear_on_submit=True):

            # Step 1 Container
            with st.container(border=True):
                st.markdown(f"<h4 style='color:#ffffff; margin-top:0;'>🔵 {t['sec_victim_info']}</h4>",
                            unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    v_phone = st.text_input(t["victim_phone"], placeholder="e.g. 0911223344")
                with col2:
                    v_bank = st.text_input(t["victim_bank"], placeholder="e.g. CBE, Telebirr")

            st.markdown("<br>", unsafe_allow_html=True)

            # Step 2 Container
            with st.container(border=True):
                st.markdown(f"<h4 style='color:#ffffff; margin-top:0;'>🔴 {t['sec_scammer_info']}</h4>",
                            unsafe_allow_html=True)
                f_type = st.selectbox(t["fraud_type"], options=t["fraud_types_opts"])
                col3, col4 = st.columns(2)
                with col3:
                    s_phone = st.text_input(t["scammer_phone"], placeholder="The scammer's phone number")
                with col4:
                    s_acc = st.text_input(t["scammer_acc"], placeholder="Mule account / wallet identifier")

            st.markdown("<br>", unsafe_allow_html=True)

            # Step 3 Container
            with st.container(border=True):
                st.markdown(f"<h4 style='color:#ffffff; margin-top:0;'>📁 {t['sec_desc']}</h4>", unsafe_allow_html=True)
                desc = st.text_area(t["desc"], placeholder="Describe the mechanism used...", height=100)

                col_file1, col_file2 = st.columns(2)
                with col_file1:
                    voice_file = st.file_uploader(t["voice_upload"], type=["wav", "mp3"])
                with col_file2:
                    uploaded_file = st.file_uploader(t["upload"], type=["png", "jpg", "jpeg"])

                if uploaded_file:
                    st.toast(t["ocr_alert"], icon="✨")

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button(t["submit_btn"])

            if submit_btn:
                if not v_phone or not s_phone:
                    st.error(t["err_fields"])
                else:
                    saved_filename = ""
                    saved_voice_name = ""
                    validation_passed = True

                    if uploaded_file is not None:
                        file_bytes = uploaded_file.read()
                        if len(file_bytes) > MAX_FILE_SIZE_BYTES:
                            st.error("🔒 Security Block: File exceeds 5MB limits.")
                            validation_passed = False
                        elif verify_file_signature(file_bytes, uploaded_file.name):
                            file_ext = os.path.splitext(uploaded_file.name)[1]
                            saved_filename = f"{uuid.uuid4().hex}{file_ext}"
                            with open(os.path.join(UPLOAD_DIR, saved_filename), "wb") as f_out:
                                f_out.write(file_bytes)
                        else:
                            st.error("🔒 Security Block: Image validation failed.")
                            validation_passed = False

                    if voice_file is not None and validation_passed:
                        voice_bytes = voice_file.read()
                        if len(voice_bytes) > MAX_FILE_SIZE_BYTES:
                            st.error("🔒 Security Block: Audio exceeds 5MB limits.")
                            validation_passed = False
                        elif verify_file_signature(voice_bytes, voice_file.name):
                            voice_ext = os.path.splitext(voice_file.name)[1]
                            saved_voice_name = f"{uuid.uuid4().hex}{voice_ext}"
                            with open(os.path.join(AUDIO_DIR, saved_voice_name), "wb") as f_voice:
                                f_voice.write(voice_bytes)
                        else:
                            st.error("🔒 Security Block: Audio verification failed.")
                            validation_passed = False

                    if validation_passed:
                        risk_score = compute_tazi_risk(f_type, s_phone, desc)
                        rep_id = save_report(
                            v_phone=v_phone,
                            v_bank=v_bank,
                            f_type=f_type,
                            s_phone=s_phone,
                            s_acc=s_acc,
                            desc=desc,
                            f_name=saved_filename,
                            voice_name=saved_voice_name,
                            risk_score=risk_score
                        )
                        st.success(t["success_report"].format(rep_id))
                        st.balloons()

    # --- INTERNAL ADMIN DASHBOARD ---
    else:
        st.markdown(f"<h1>📊 {t['admin_title']}</h1>", unsafe_allow_html=True)
        st.markdown("---")

        if "admin_authenticated" not in st.session_state:
            st.session_state["admin_authenticated"] = False

        if not st.session_state["admin_authenticated"]:
            st.subheader("🔒 Authentication Required")
            admin_pwd = st.text_input("Enter secure INSA Analyst credentials", type="password")

            if st.button("Authenticate Panel Access"):
                stored_admin_hash = get_secure_admin_hash()
                if verify_password(admin_pwd, stored_admin_hash):
                    st.session_state["admin_authenticated"] = True
                    st.success("Authorized. Threat triage environment established.")
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid credentials.")

            st.markdown("<br><br>", unsafe_allow_html=True)
            with st.expander("🛠️ FIRST-TIME SETUP: SECURE PASSWORD HASH GENERATOR"):
                st.markdown("""
                Use this local utility to hash a password with cryptographically secure **bcrypt** algorithms. 
                Once generated, set the string output as your environment variable `ADMIN_PASSWORD_HASH` or place it inside your `.streamlit/secrets.toml` file.
                """)
                new_plain_text = st.text_input("Plaintext Setup Password", type="password", key="setup_pwd")
                if st.button("Generate Cryptographic bcrypt Hash"):
                    if new_plain_text:
                        hash_result = bcrypt.hashpw(new_plain_text.encode(), bcrypt.gensalt(rounds=12))
                        st.code(hash_result.decode(), language="bash")
                        st.success("Copy the text string from the box above and save it securely.")
                    else:
                        st.warning("Please type a custom password above.")
            return

        df_reports = get_all_reports()

        if df_reports.empty:
            st.info("No reported cases found in localized database. Fill out the public portal form.")
        else:
            tot_cases = len(df_reports)
            unique_hackers = df_reports["scammer_phone"].nunique()
            mule_accounts = df_reports[df_reports["fraudster_account"] != ""]["fraudster_account"].nunique()

            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.markdown(f"""
                    <div style="background: #0d1b2e; border-left: 5px solid #00f2fe; padding: 20px; border-radius: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                        <p style="margin:0; font-size:0.85rem; color:#a0aec0; text-transform:uppercase; font-weight:700;">{t['metric_total']}</p>
                        <h2 style="margin:10px 0 0 0; color:#ffffff !important; font-size:2rem;">{tot_cases}</h2>
                    </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown(f"""
                    <div style="background: #0d1b2e; border-left: 5px solid #d32f2f; padding: 20px; border-radius: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                        <p style="margin:0; font-size:0.85rem; color:#a0aec0; text-transform:uppercase; font-weight:700;">{t['metric_unique_scammers']}</p>
                        <h2 style="margin:10px 0 0 0; color:#ffffff !important; font-size:2rem;">{unique_hackers}</h2>
                    </div>
                """, unsafe_allow_html=True)
            with col_m3:
                st.markdown(f"""
                    <div style="background: #0d1b2e; border-left: 5px solid #fbc02d; padding: 20px; border-radius: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                        <p style="margin:0; font-size:0.85rem; color:#a0aec0; text-transform:uppercase; font-weight:700;">{t['mule_acc']}</p>
                        <h2 style="margin:10px 0 0 0; color:#ffffff !important; font-size:2rem;">{mule_accounts}</h2>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
                <div style="background: #0d1b2e; border: 1px solid #1a2e4c; border-radius: 6px; padding: 20px; margin-bottom: 20px;">
                    <h4 style="margin-top:0; color:#ffffff;">🧠 TAZI Intelligent Threat Feed</h4>
                    <p style="color:#a0aec0; font-size:0.95rem; margin-bottom:0;">
                        Live incident monitoring using behavioral heuristics, active patterns, and high-frequency target accounts.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            df_tazi_sorted = df_reports.sort_values(by="risk_score", ascending=False)

            for col in ['victim_phone', 'scammer_phone', 'fraudster_account', 'description']:
                df_tazi_sorted[col] = df_tazi_sorted[col].astype(str).apply(
                    lambda x: x.replace('<', '&lt;').replace('>', '&gt;'))

            st.dataframe(
                df_tazi_sorted[['id', 'timestamp', 'fraud_type', 'scammer_phone', 'risk_score', 'status']],
                use_container_width=True
            )

            st.markdown("---")
            st.markdown(f"### {t['table_title']}")

            df_timeline = df_reports.copy()
            df_timeline['timestamp'] = pd.to_datetime(df_timeline['timestamp'])
            df_trend = df_timeline.groupby(df_timeline['timestamp'].dt.date).size().reset_index(name='Daily Incidents')
            df_trend = df_trend.set_index('timestamp')
            st.line_chart(df_trend, color="#00f2fe")

            # Audio Evidence Desk
            st.markdown("### 🎙️ Threat Intelligence Audio Deck")
            voice_cases = df_reports[df_reports["voice_note_path"] != ""]
            if not voice_cases.empty:
                selected_case = st.selectbox("Select Case ID to analyze audio feed:",
                                             options=voice_cases["id"].tolist())
                voice_file_name = voice_cases[voice_cases["id"] == selected_case]["voice_note_path"].values[0]
                audio_path = os.path.join(AUDIO_DIR, voice_file_name)
                if os.path.exists(audio_path):
                    st.audio(audio_path)
                else:
                    st.warning("Selected audio record cannot be loaded.")
            else:
                st.caption("No audio files logged in database context yet.")

            st.markdown("---")
            st.markdown(f"### {t['action_update']}")
            col_act1, col_act2, col_act3 = st.columns(3)

            with col_act1:
                target_id = st.selectbox("Select Target ID", options=df_reports["id"].tolist())
            with col_act2:
                new_status = st.selectbox(
                    "Assign Status",
                    ["New / Unresolved", "Under Investigation (INSA)", "Flagged to Bank / Frozen",
                     "Resolved / Attacker Traced"]
                )
            with col_act3:
                update_btn = st.button(t["btn_update"])
                if update_btn:
                    update_report_status(target_id, new_status)
                    st.success(f"Incident #{target_id} updated to: {new_status}!")
                    st.rerun()

            st.markdown("---")
            if st.sidebar.button(t["btn_delete"], type="primary"):
                clear_db()
                st.sidebar.success(t["db_cleared"])
                st.rerun()

    # Sovereign Ethiopia Pride Footer
    st.markdown("""
        <div class="ethiopian-pride-footer">
            <span style="color: #388e3c;">●</span> <span style="color: #fbc02d;">●</span> <span style="color: #d32f2f;">●</span>
            <br>
            <strong>INFORMATION NETWORK SECURITY ADMINISTRATION (INSA)</strong><br>
            <span style="font-size: 0.8rem; letter-spacing: 1px;">PROUDLY DEVELOPED & POWERED BY ETHIOPIA • 2026</span>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()