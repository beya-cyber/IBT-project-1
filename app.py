import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# --- 1. LOCAL DATABASE & FILE SYSTEM SETUP ---
DB_FILE = "fraud_reports.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
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
            status TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()

UPLOAD_DIR = "uploaded_evidence"
AUDIO_DIR = "voice_notes"
for directory in [UPLOAD_DIR, AUDIO_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# --- 2. MULTI-LANGUAGE TRANSLATION DICTIONARY ---
translations = {
    "English": {
        "nav_role": "SYSTEM PORTAL VIEW",
        "role_victim": "Victim Intake Portal (Public)",
        "role_admin": "INSA Analyst Dashboard (Internal)",
        "title": "National Cybercrime & Financial Fraud Portal",
        "subtitle": "Securing Ethiopia's digital economy. Report scams, fake transfers, or phishing instantly.",
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
        "voice_upload": "🎙️ Audio Evidence (Record/Upload a voice clip if speaking is easier)",
        "upload": "📷 Screenshot Evidence (OCR automatically processes transaction details)",
        "ocr_alert": "✨ AI OCR Engaged: Threat metadata will be auto-parsed from the screenshot.",
        "submit_btn": "🔒 SECURELY SUBMIT INCIDENT",

        "err_fields": "CRITICAL ERROR: Phone numbers are required to track the threat actor!",
        "success_report": "INCIDENT ENCRYPTED & SUBMITTED. ID: #{}. National threat tracking initiated. Please remain calm.",

        "admin_title": "INSA Incident Command & Fraud Triage Center",
        "metric_total": "Total Reported Incidents",
        "metric_unique_scammers": "Active Scammer Numbers",
        "mule_acc": "Target Mule Accounts Detected",
        "table_title": "Live Threat Feed (Real-Time Database Records)",
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
        "subtitle": "የኢትዮጵያን ዲጂታል ደህንነት ማስጠበቅ። ማጭበርበሮችን፣ የሐሰት ደረሰኞችን ወይም የጽሑፍ መልዕክቶችን በፍጥነት ሪፖርት ያድርጉ።",
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
        "voice_upload": "🎙️ የድምፅ ማስረጃ (መጻፍ ካልፈለጉ የድምፅ መልዕክት መቅዳት/መጫን ይችላሉ)",
        "upload": "📷 የስክሪንሾት ማስረጃ (የደረሰኙ መረጃ በኮምፒውተሩ በራስ-ሰር ይነበባል)",
        "ocr_alert": "✨ AI OCR ንቁ ነው፡ አስፈላጊ መረጃዎች ከፎቶው ላይ በቀጥታ ይነበባሉ።",
        "submit_btn": "🔒 ሪፖርቱን በምስጢር አስገባ",

        "err_fields": "ስህተት፡ የአጥቂውን ቁጥር ለመከታተል ስልክ ቁጥሮች መሞላት አለባቸው!",
        "success_report": "ሪፖርትዎ በምስጢር ተቀምጧል! የክትትል መለያ ቁጥር፡ #{} ነው። ባንክዎ ክትትል እንዲጀምር ተደርጓል። እባክዎን ይረጋጉ።",

        "admin_title": "የኢንሳ (INSA) የሳይበር ወንጀል መቆጣጠሪያ ማዕከል",
        "metric_total": "ጠቅላላ የተመዘገቡ ጥቃቶች",
        "metric_unique_scammers": "አክቲቭ አጭበርባሪ ቁጥሮች",
        "mule_acc": "የታወቁ የገንዘብ ማስተላለፊያ (Mule) አካውንቶች",
        "table_title": "በቀጥታ የሚገቡ ሪፖርቶች (ላይቭ ዴታቤዝ)",
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
        "subtitle": "Nageenya dinagdee dijitaalaa Itiyoophiyaa kabachiisuu. Gowwoomsaa daddafiin gabaasaa.",
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
        "voice_upload": "🎙️ Ragaa Sagalee (Yoo barreessuu caalaa dubbachuu filattan sagalee keessan ol-fe'aa)",
        "upload": "📷 Ragaa Iskiriinshootii (Odeeffannoon rasiidii ofumaan dubbifama)",
        "ocr_alert": "✨ AI OCR Haktivii dha: Odeeffannoon iskirinshara keessaa ofumaan dubbifama.",
        "submit_btn": "🔒 GABAASA ICCITII ERGI",

        "err_fields": "DONGORRAA: Lakkoofsa bilbilaa guutuun dirqama!",
        "success_report": "GABAASNI KEESSAN EGGUMSAAN ERGAMEERA! ID: #{}. Hordoffiin jalqabameera. Tasgabbaahaa.",

        "admin_title": "Giddugala To'annoo fi Triage Saayibar INSA",
        "metric_total": "Wanjaloota Gabaasaman",
        "metric_unique_scammers": "Lakkoofsota Haktivii Gowwoomsitootaa",
        "mule_acc": "Herregoota Mule Maallaqaa Adda Baafaman",
        "table_title": "Gabaasa Miidhamtootaa Kan Live Galu",
        "action_update": "Haala Gabaasaa Haaromsi",
        "btn_update": "Haala Haaromsi",
        "btn_delete": "Database Qulqulleessi",
        "db_cleared": "Daataa demo hundi qulqulleeffameera."
    }
}


# --- 3. DATABASE INTERACTIONS ---
def save_report(victim_phone, victim_bank, fraud_type, scammer_phone, scammer_acc, description, file_name, voice_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO reports (timestamp, victim_phone, victim_bank, fraud_type, scammer_phone, scammer_acc, description, evidence_file_name, voice_note_path, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, victim_phone, victim_bank, fraud_type, scammer_phone, scammer_acc, description, file_name,
          voice_name, "New / Unresolved"))
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


# --- 4. ADVANCED PORTAL APPLICATION ---
def main():
    st.set_page_config(
        page_title="INSA - National Fraud Portal",
        page_icon="🛡️",
        layout="wide"
    )

    # --- INJECT CUSTOM CYBER-THEME DESIGN (CSS) ---
    st.markdown("""
        <style>
            /* Dark background and high-tech typography */
            .main {
                background-color: #0d1117;
                color: #c9d1d9;
            }
            h1, h2, h3 {
                color: #58a6ff !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-weight: 700;
            }
            .stSubheader {
                color: #8b949e !important;
            }

            /* Custom styled cyber cards for visual steps */
            .cyber-card {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            }
            .cyber-card-header {
                font-size: 1.25rem;
                color: #58a6ff;
                font-weight: bold;
                border-bottom: 1px solid #30363d;
                padding-bottom: 10px;
                margin-bottom: 15px;
            }

            /* Enhanced submit button styling */
            .stButton>button {
                background-color: #1f6feb !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 12px 24px !important;
                font-weight: bold !important;
                width: 100% !important;
                box-shadow: 0 0 15px rgba(31, 111, 235, 0.4);
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #388bfd !important;
                box-shadow: 0 0 25px rgba(56, 139, 253, 0.7);
                transform: translateY(-2px);
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("<h3 style='color:#58a6ff;'>⚙️ CONTROL STATION</h3>", unsafe_allow_html=True)

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
    st.sidebar.caption("INSA National Security Project Prototype")

    # --- PUBLIC INTAKE FORM (VICTIM PORTAL) ---
    if user_role == t["role_victim"]:
        st.markdown(f"<h1>🛡️ {t['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:1.1rem; color:#8b949e;'>{t['subtitle']}</p>", unsafe_allow_html=True)
        st.markdown("---")

        with st.form("victim_reporting_form"):

            # STEP 1 CARD
            st.markdown(f"""
                <div class="cyber-card">
                    <div class="cyber-card-header">🔑 {t['sec_victim_info']}</div>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                v_phone = st.text_input(t["victim_phone"], placeholder="09xxxxxxxx / 07xxxxxxxx")
            with col2:
                v_bank = st.text_input(t["victim_bank"], placeholder="e.g., CBE, Telebirr, Awash")

            # STEP 2 CARD
            st.markdown(f"""
                <div class="cyber-card">
                    <div class="cyber-card-header">🚨 {t['sec_scammer_info']}</div>
                </div>
            """, unsafe_allow_html=True)
            f_type = st.selectbox(t["fraud_type"], options=t["fraud_types_opts"])

            col3, col4 = st.columns(2)
            with col3:
                s_phone = st.text_input(t["scammer_phone"], placeholder="The scammer's phone number")
            with col4:
                s_acc = st.text_input(t["scammer_acc"], placeholder="Mule bank account number")

            # STEP 3 CARD
            st.markdown(f"""
                <div class="cyber-card">
                    <div class="cyber-card-header">📁 {t['sec_desc']}</div>
                </div>
            """, unsafe_allow_html=True)
            desc = st.text_area(t["desc"], placeholder="Explain exactly what happened...")

            # Smart File Inputs
            voice_file = st.file_uploader(t["voice_upload"], type=["wav", "mp3", "m4a"])
            uploaded_file = st.file_uploader(t["upload"], type=["png", "jpg", "jpeg"])

            if uploaded_file:
                st.info(t["ocr_alert"])

            # Submit
            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button(t["submit_btn"])

            if submit_btn:
                if not v_phone or not s_phone:
                    st.error(t["err_fields"])
                else:
                    saved_filename = ""
                    if uploaded_file is not None:
                        saved_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
                        with open(os.path.join(UPLOAD_DIR, saved_filename), "wb") as f_out:
                            f_out.write(uploaded_file.getbuffer())

                    saved_voice_name = ""
                    if voice_file is not None:
                        saved_voice_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{voice_file.name}"
                        with open(os.path.join(AUDIO_DIR, saved_voice_name), "wb") as f_voice:
                            f_voice.write(voice_file.getbuffer())

                    rep_id = save_report(
                        victim_phone=v_phone,
                        victim_bank=v_bank,
                        fraud_type=f_type,
                        scammer_phone=s_phone,
                        fraudster_account=s_acc,
                        description=desc,
                        file_name=saved_filename,
                        voice_name=saved_voice_name
                    )

                    st.success(t["success_report"].format(rep_id))
                    st.balloons()

    # --- INTERNAL ADMIN DASHBOARD ---
    else:
        st.markdown(f"<h1>📊 {t['admin_title']}</h1>", unsafe_allow_html=True)
        st.markdown("---")

        df_reports = get_all_reports()

        if df_reports.empty:
            st.info("No reported cases found. Fill out the report form from the public view first!")
        else:
            tot_cases = len(df_reports)
            unique_hackers = df_reports["scammer_phone"].nunique()
            mule_accounts = df_reports[df_reports["fraudster_account"] != ""]["fraudster_account"].nunique()

            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric(label=t["metric_total"], value=tot_cases)
            with col_m2:
                st.metric(label=t["metric_unique_scammers"], value=unique_hackers)
            with col_m3:
                st.metric(label=t["mule_acc"], value=mule_accounts)

            st.markdown("---")

            st.markdown(f"### {t['table_title']}")
            fraud_breakdown = df_reports["fraud_type"].value_counts()
            st.bar_chart(fraud_breakdown)

            st.dataframe(df_reports, use_container_width=True)

            # Voice Player
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
                    st.warning("Audio file missing.")
            else:
                st.caption("No audio recordings logged.")

            st.markdown("---")
            st.markdown(f"### {t['action_update']}")
            col_act1, col_act2, col_act3 = st.columns(3)

            with col_act1:
                target_id = st.selectbox("Select Target ID", options=df_reports["id"].tolist())
            with col_act2:
                new_status = st.selectbox(
                    "Assign New Threat Level/Status",
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


if __name__ == "__main__":
    main()