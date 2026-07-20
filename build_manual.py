# build_manual.py
from fpdf import FPDF
import os


class MasterManualPDF(FPDF):
    def header(self):
        # Only draw the standard header if we are past the cover page (page 1)
        if self.page_no() > 1:
            self.set_font("helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, "Lucy Chat: The Complete Software Development Master Manual", align="R", new_x="LMARGIN",
                      new_y="NEXT")
            self.set_draw_color(200, 200, 200)
            self.line(20, 18, 190, 18)
            self.ln(5)

    def footer(self):
        # Draw standard footer past the cover page
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(100, 10, "Author: Beya | Platform: Python & Streamlit", align="L")
            self.cell(0, 10, f"Page {self.page_no()}", align="R")

    def print_chapter_title(self, num, title):
        self.ln(10)
        self.set_font("helvetica", "B", 16)
        self.set_text_color(15, 76, 129)  # Deep Professional Blue
        self.cell(0, 10, f"Chapter {num}: {title}", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
        # Decorative line
        self.set_draw_color(15, 76, 129)
        self.set_line_width(0.8)
        self.line(self.get_x(), self.get_y(), self.get_x() + 170, self.get_y())
        self.ln(8)
        self.set_line_width(0.2)  # reset line width

    def print_section_heading(self, heading):
        self.ln(5)
        self.set_font("helvetica", "B", 12)
        self.set_text_color(40, 40, 40)
        self.cell(0, 8, heading, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def print_paragraph(self, text):
        self.set_font("times", "", 10.5)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, text)
        self.ln(4)

    def print_code_block(self, code_lines):
        self.set_fill_color(245, 245, 245)
        self.set_text_color(199, 37, 78)  # Dark Red for Code
        self.set_font("courier", "", 9)

        total_height = len(code_lines) * 4.5 + 4
        if self.get_y() + total_height > 270:
            self.add_page()

        self.cell(0, 2, "", new_x="LMARGIN", new_y="NEXT", fill=True)
        for line in code_lines:
            clean_line = line.replace("    ", "  ")
            # Ensure line can be encoded in latin-1 safely
            try:
                clean_line.encode('latin-1')
            except UnicodeEncodeError:
                clean_line = clean_line.encode('ascii', 'replace').decode('ascii')
            self.cell(0, 4.5, clean_line, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.cell(0, 2, "", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(4)
        self.set_text_color(50, 50, 50)  # reset to body color


# Initialize PDF
pdf = MasterManualPDF(orientation="P", unit="mm", format="A4")
pdf.set_margins(20, 20, 20)
pdf.set_auto_page_break(auto=True, margin=20)

# ================= PAGE 1: COVER PAGE =================
pdf.add_page()
pdf.set_fill_color(15, 76, 129)  # Elegant dark blue background banner accent
pdf.rect(0, 0, 210, 80, "F")

pdf.set_y(25)
pdf.set_font("helvetica", "B", 26)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, "LUCY CHAT", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 10, "THE COMPLETE MULTI-TASKING SOCIAL SYSTEM FOR ETHIOPIA", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_y(90)
pdf.set_font("helvetica", "B", 18)
pdf.set_text_color(40, 40, 40)
pdf.cell(0, 10, "Software Development Master Course Book", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("helvetica", "I", 12)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "An In-Depth Line-by-Line Technical Compilation Manual", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_draw_color(15, 76, 129)
pdf.set_line_width(1)
pdf.line(40, 120, 170, 120)

pdf.set_y(135)
pdf.set_font("times", "", 12)
pdf.set_text_color(60, 60, 60)
pdf.multi_cell(0, 6,
               "Designed to take ambitious local students and global innovators from writing their first line of basic variables to designing production-ready, multi-language, encrypted, and highly secure social web solutions optimized for Ethiopian infrastructure networks.\n\nIncludes complete line-by-line code breakdowns, library justifications, database strategies, security paradigms, real-time media rendering, and system scaling architectures.",
               align="C")

# Authorship & Date at the Bottom
pdf.set_y(240)
pdf.set_font("helvetica", "B", 11)
pdf.set_text_color(15, 76, 129)
pdf.cell(0, 6, "Author: Beya (Behailu)", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("helvetica", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 5, "Python Frameworks & Security Lab Publication", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, "Version 2.0 (Stable Edition) - July 2026", align="C")

# ================= PAGE 2: TABLE OF CONTENTS =================
pdf.add_page()
pdf.ln(10)
pdf.set_font("helvetica", "B", 16)
pdf.set_text_color(15, 76, 129)
pdf.cell(0, 10, "Detailed Course Curricula (Table of Contents)", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

toc_items = [
    ("Chapter 1: The Foundations of Desktop and Web Frameworks", "Page 3"),
    ("           1.1 System Demands & Language Selections", "Page 4"),
    ("           1.2 IDE Mechanics & Code Syntax Principles", "Page 6"),
    ("Chapter 2: Phase 1 - Developing the Core Multi-Language Logic Engine", "Page 8"),
    ("           2.1 Designing Memory Frameworks with Python", "Page 10"),
    ("           2.2 Deep Code Explanations & Structural Justifications", "Page 13"),
    ("Chapter 3: Phase 2 - Developing the Interactive Multilingual Web Interface", "Page 18"),
    ("           3.1 Core Architecture of Streamlit Application Interface", "Page 21"),
    ("           3.2 Dynamic Matrix Translations & User Feed Renders", "Page 25"),
    ("Chapter 4: Phase 3 - Multimedia Processing (Voice Notes & Video Storage)", "Page 30"),
    ("           4.1 Local Audio/Video File Pipelines & RAM Buffers", "Page 33"),
    ("           4.2 Modular Explanations & Network Optimization Techniques", "Page 37"),
    ("Chapter 5: Phase 4 - Cybersecurity Infrastructure & Data Protection", "Page 41"),
    ("           5.1 The Threat Landscape of Modern Networks", "Page 43"),
    ("           5.2 Implementing Cryptographic Bcrypt Hashing Engines", "Page 46"),
    ("Chapter 6: Final Integration, Compilation, & Enterprise Scaling", "Page 49"),
    ("           6.1 Deploying Lucy Chat Globally (Cloud, Local & Offline Hooks)", "Page 50"),
]

pdf.set_font("times", "", 10.5)
pdf.set_text_color(50, 50, 50)
for item, page in toc_items:
    dots_count = 80 - len(item)
    leaders = "." * dots_count
    pdf.cell(130, 7.5, item, align="L")
    pdf.cell(20, 7.5, leaders, align="R")
    pdf.cell(0, 7.5, page, align="R", new_x="LMARGIN", new_y="NEXT")

# ================= CHAPTER 1 =================
pdf.add_page()
pdf.print_chapter_title(1, "The Foundations of Desktop and Web Frameworks")
pdf.print_section_heading("1.1 System Demands & Language Selections")
pdf.print_paragraph(
    "Developing high-utility social media platforms targeted at regions with varying internet infrastructure, "
    "such as East Africa, demands extreme resource efficiency and intelligent framework selection. Traditional "
    "social development relies on complex multi-layered stacks: HTML5, CSS3, JavaScript engines, backend "
    "APIs (Node.js/Django), and standalone databases. For a software developer starting out, managing this "
    "cognitive load can significantly slow down your progress."
)
pdf.print_paragraph(
    "To solve this, our master project -- Lucy Chat -- utilizes Python combined with the Streamlit web engine. "
    "This integration lets us execute deep back-end computational logic and complex front-end UI components "
    "within a unified environment using a single programming language. This dramatically increases development "
    "velocity, reduces error tracking time, and allows us to deploy fully responsive, beautifully organized "
    "user interfaces tailored for local communities instantly."
)
pdf.print_paragraph(
    "Additionally, Python's clean syntax mimics plain English syntax. This allows you to focus 100% of your energy "
    "on core program logical architecture, cryptography, and efficient state handling, rather than fighting "
    "complex braces, semi-colons, and obscure compiling errors common in legacy languages like C++ or Java."
)

pdf.add_page()
pdf.print_section_heading("1.2 IDE Mechanics & Code Syntax Principles")
pdf.print_paragraph(
    "To build industrial-grade applications, developers use an Integrated Development Environment (IDE). "
    "Our chosen IDE is Microsoft Visual Studio Code (VS Code). VS Code acts as an advanced cockpit for "
    "software development. It offers three crucial development benefits:"
)
pdf.print_paragraph(
    "1. Linter Systems: Highlight errors in real-time as you write code, preventing logical or syntax bugs before "
    "you compile.\n"
    "2. Integrated Terminal: Allows running servers, launching virtual environments, and executing databases "
    "without leaving the main workspace.\n"
    "3. Highlighting Engine: Visualizes variables, library modules, strings, and integer variables in distinct color palettes, "
    "making the logic easily readable."
)
pdf.print_paragraph(
    "When writing Python code within VS Code, you must master indentation. Unlike other systems that use curly brackets "
    "to group logic, Python uses white space. Indenting a block of code by 4 spaces tells Python that this specific block "
    "belongs to the function, class, or loop defined directly above it. Getting this right is foundational to writing "
    "clean, executable software."
)

# ================= CHAPTER 2 =================
pdf.add_page()
pdf.print_chapter_title(2, "Phase 1 - Core Multi-Language Logic Engine")
pdf.print_section_heading("2.1 Designing Memory Frameworks with Python")
pdf.print_paragraph(
    "A social media post is not just raw text; it is a complex packet of structured data. A single message "
    "requires a sender's name, the post contents, the user's location, the chosen translation interface, and "
    "an authentication signature. We will build this internal data structures pipeline directly inside our core engine module."
)
pdf.print_paragraph(
    "This logic engine is fully sandboxed inside engine.py. Separating backend calculations from the main display "
    "layer is an industry-standard architecture known as MVC (Model-View-Controller). This ensures that if the visual "
    "layout changes, our core messaging data logic remains safe and untouched."
)

pdf.add_page()
pdf.print_section_heading("2.2 Comprehensive Engine Code Implementation")
engine_code = [
    "# ===================================================================",
    "# engine.py - CORE DATA CONVERTER & MEMORY PIPELINE",
    "# ===================================================================",
    "",
    "# Global Immutable Variables (App Manifest)",
    "APP_NAME = 'Lucy Chat'",
    "SERVER_PORT = 8501",
    "is_server_active = True",
    "",
    "# Central Dynamic Memory List (Our active RAM table)",
    "chat_database = []",
    "",
    "def save_message(sender_name, message_text, region, language):",
    "    \"\"\"",
    "    Accepts user text, packages details into a dictionary structure,",
    "    and appends the record into the dynamic database list.",
    "    \"\"\"",
    "    # Validate to prevent empty submissions",
    "    if not sender_name.strip() or not message_text.strip():",
    "        return False",
    "    ",
    "    # Packaging data using a key-value data structure",
    "    new_post = {",
    "        'sender': sender_name,",
    "        'message': message_text,",
    "        'region': region,",
    "        'language': language",
    "    }",
    "    ",
    "    # Appending to central RAM list",
    "    chat_database.append(new_post)",
    "    return True",
    "",
    "def clear_database():",
    "    \"\"\"Wipes all records from the current active memory session.\"\"\"",
    "    global chat_database",
    "    chat_database = []",
    "    return True"
]
pdf.print_code_block(engine_code)

pdf.add_page()
pdf.print_section_heading("2.3 Line-by-Line Breakdown & Structural Justifications")
pdf.print_paragraph(
    "Let us explore exactly how each component in this logic engine operates, explaining why we use it and how it behaves:\n\n"
    "* APP_NAME = 'Lucy Chat': This defines a global string variable. We capitalize global constants so team developers "
    "know these should not be modified on-the-fly. This string will populate headers and web banners.\n\n"
    "* chat_database = []: This is a standard Python List. Unlike static arrays in C, Python lists are dynamic. They can expand "
    "and shrink dynamically as users post content or delete messages, keeping memory management simple and fast.\n\n"
    "* def save_message(...): The def keyword initiates a function. We define this to handle all future message posts. "
    "Instead of writing save logic multiple times across the frontend, we write it once here to be reused.\n\n"
    "* if not sender_name.strip(): The .strip() function trims all invisible spacing characters (tabs, newlines, blank spaces). "
    "This validation logic ensures that malicious or accidental empty posts are rejected at the entrance of our pipeline.\n\n"
    "* new_post = { ... }: This is a Python Dictionary. Dictionaries store data as 'Key-Value' pairs. This is the optimal structure "
    "for databases because it allows us to query attributes directly (e.g., query post['sender']) without running slow search algorithms."
)

# ================= CHAPTER 3 =================
pdf.add_page()
pdf.print_chapter_title(3, "Phase 2 - The Multilingual Web Interface")
pdf.print_section_heading("3.1 Core Architecture of Streamlit Application Interface")
pdf.print_paragraph(
    "A professional application must welcome its users in their native language. To accommodate the rich linguistic "
    "heritage of Ethiopia, Lucy Chat natively supports English, Amharic, and Oromo. "
    "In this chapter, we will build a highly responsive and localized User Interface (UI)."
)
pdf.print_paragraph(
    "To implement this without cluttering the project code, we design a 'Translation Dictionary Matrix'. "
    "Depending on the language selected by the user in the sidebar panel, our app dynamically swaps "
    "every label, text box, alert, button, and header on the screen instantaneously."
)

pdf.add_page()
pdf.print_section_heading("3.2 The Complete Interface Code (app.py)")
app_code = [
    "# ===================================================================",
    "# app.py - MULTILINGUAL USER INTERFACE (UI) FRONTEND",
    "# ===================================================================",
    "import streamlit as st",
    "",
    "# Set visual parameters for the tab",
    "st.set_page_config(page_title='Lucy Chat', page_icon='ET', layout='centered')",
    "",
    "# The translation matrix mapped dynamically to languages",
    "translations = {",
    "    'English': {",
    "        'welcome': 'Welcome to Lucy Chat!',",
    "        'subtitle': 'Connecting Ethiopians globally',",
    "        'name_label': 'Your Name',",
    "        'msg_label': 'Write a message...',",
    "        'region_label': 'Where are you chatting from?',",
    "        'submit_btn': 'Post Message',",
    "        'feed_header': 'Live Feed'",
    "    },",
    "    'Amharic': {",
    "        'welcome': 'Enkuan Wede Lucy Chat Bedehna Metu!',",
    "        'subtitle': 'Ethiopiawyann be Alem Zurya Magenagnot',",
    "        'name_label': 'Simwon Yasgebu',",
    "        'msg_label': 'Meleket Yitsefu...',",
    "        'region_label': 'Keyet No Mitisifut?',",
    "        'submit_btn': 'Meleket Lak',",
    "        'feed_header': 'Yeqetiita Wiyeiyet'",
    "    },",
    "    'Oromo': {",
    "        'welcome': 'Baga Gara Lucy Chat Nageayan Dhuftan!',",
    "        'subtitle': 'Itoophiyaanota addunyaa guutuu walitti qabuu',",
    "        'name_label': 'Maqaa keessan',",
    "        'msg_label': 'Ergaa barreessi...',",
    "        'region_label': 'Eessaa odeessaa jirtu?',",
    "        'submit_btn': 'Ergaa Ergi',",
    "        'feed_header': 'Tamsaasa Bilisaa'",
    "    }",
    "}",
    "",
    "# Initialize dynamic Session State so chats survive browser refreshes",
    "if 'chat_history' not in st.session_state:",
    "    st.session_state.chat_history = []",
    "",
    "# Render side configuration panel",
    "selected_lang = st.sidebar.selectbox('Language', list(translations.keys()))",
    "t = translations[selected_lang]",
    "",
    "st.title(f\"Lucy Chat - {t['welcome']}\")",
    "st.caption(t['subtitle'])",
    "st.write('---')",
    "",
    "# Encapsulating inputs in a single form to optimize load time",
    "with st.form('chat_input_form', clear_on_submit=True):",
    "    col1, col2 = st.columns(2)",
    "    with col1:",
    "        username = st.text_input(t['name_label'], placeholder='e.g., Almaz')",
    "    with col2:",
    "        location = st.selectbox(t['region_label'], [",
    "            'Addis Ababa', 'Amhara', 'Oromia', 'Tigray', 'Somali', ",
    "            'Sidama', 'South Ethiopia', 'Afar', 'Benishangul-Gumuz', ",
    "            'Gambela', 'Harari', 'Diaspora (USA)', 'Diaspora (Europe)'",
    "        ])",
    "    ",
    "    user_message = st.text_area(t['msg_label'])",
    "    submit_btn = st.form_submit_button(t['submit_btn'])",
    "",
    "if submit_btn:",
    "    if username.strip() and user_message.strip():",
    "        new_post = {",
    "            'sender': username,",
    "            'message': user_message,",
    "            'region': location,",
    "            'language': selected_lang",
    "        }",
    "        st.session_state.chat_history.append(new_post)",
    "        st.success('Sent! / Telkual!')",
    "    else:",
    "        st.error('Fields cannot be empty!')",
    "",
    "# Render chronological chat list reversed",
    "st.subheader(f\"{t['feed_header']}\")",
    "for chat in reversed(st.session_state.chat_history):",
    "    with st.chat_message('user'):",
    "        st.write(f\"**{chat['sender']}** ({chat['region']})\")",
    "        st.write(chat['message'])"
]
pdf.print_code_block(app_code)

pdf.add_page()
pdf.print_section_heading("3.3 Detailed Structural Review of Application Layer")
pdf.print_paragraph(
    "* import streamlit as st: Loads the Streamlit libraries. By naming it 'st', we reduce repetitive typing, keeping our code clean and concise.\n\n"
    "* st.set_page_config(...): Set at the very top of our code. It configures browser-level metadata like the tab title ('Lucy Chat') and dynamic page scaling.\n\n"
    "* translations = { ... }: This nested dictionary matrix works as our localized interface hub. By structuring keys uniformly, we can pull strings dynamically based on user selections.\n\n"
    "* st.session_state: Because web pages run stateless protocols, they completely reload and wipe variables every time a button is clicked. session_state acts as a persistent server memory pocket that keeps our chat history safe during reloads."
)

# ================= CHAPTER 4 =================
pdf.add_page()
pdf.print_chapter_title(4, "Phase 3 - Multimedia & Voice Note Processing")
pdf.print_section_heading("4.1 Local Audio/Video File Pipelines & RAM Buffers")
pdf.print_paragraph(
    "A versatile social platform must go beyond basic text messages. Local users and diaspora families "
    "depend on sending video updates and sharing voice recordings. Because network speeds can fluctuate, "
    "multimedia must be processed efficiently."
)
pdf.print_paragraph(
    "When a user uploads a media clip, Streamlit reads the file into memory as a dynamic byte string. We then "
    "feed these raw bytes directly into the built-in HTML5 media players. This enables instant previews, "
    "saving local server space by only writing to disk when a user hits 'Send'."
)

pdf.add_page()
pdf.print_section_heading("4.2 Implementing the Multimedia Logic Layer")
media_code = [
    "# ===================================================================",
    "# APPEND THIS COMPONENT TO app.py TO ENABLE MULTITASKING MEDIA",
    "# ===================================================================",
    "st.write('---')",
    "st.subheader('Lucy Media Sharing Center')",
    "st.write('Share high-resolution videos or voice notes with your family.')",
    "",
    "# Toggle to select media output dynamically",
    "media_mode = st.radio('Choose Media Format:', ['Text Only', 'Video Post', 'Voice Memo'])",
    "",
    "if media_mode == 'Video Post':",
    "    uploaded_video = st.file_uploader('Upload MP4 Video file', type=['mp4', 'mov'])",
    "    if uploaded_video is not None:",
    "        st.video(uploaded_video)",
    "        st.success('Video loaded successfully!')",
    "",
    "elif media_mode == 'Voice Memo':",
    "    uploaded_audio = st.file_uploader('Upload Audio file (.mp3, .wav)', type=['mp3', 'wav'])",
    "    if uploaded_audio is not None:",
    "        st.audio(uploaded_audio)",
    "        st.success('Voice message loaded!')"
]
pdf.print_code_block(media_code)

pdf.add_page()
pdf.print_section_heading("4.3 Video and Audio Buffer Management Explained")
pdf.print_paragraph(
    "* st.radio('Choose Media Format:', ...): Displays a single-choice list of radio buttons. This allows users to switch between text and media layout modes without cluttering the screen.\n\n"
    "* st.file_uploader('Upload MP4 Video', type=['mp4', 'mov']): Renders an upload box. Specifying the type parameter acts as a secure format validator, blocking harmful executable files from being uploaded to our server.\n\n"
    "* if uploaded_video is not None: Prevents runtime crash errors. If a user hasn't selected a file, the uploader variable remains empty (None). Checking for this ensures our media players only load once the file is fully ready."
)

# ================= CHAPTER 5 =================
pdf.add_page()
pdf.print_chapter_title(5, "Phase 4 - Cybersecurity Infrastructure")
pdf.print_section_heading("5.1 The Threat Landscape of Modern Networks")
pdf.print_paragraph(
    "In modern social applications, security is a primary foundation, not an afterthought. When a user creates an account, "
    "their password must never be stored in plain text. If an attacker gains unauthorized access to our database, "
    "plain text credentials would compromise accounts globally. To prevent this, developers utilize one-way cryptographic hashing."
)
pdf.print_paragraph(
    "Hashing converts a user's password into a unique, fixed-length string of scrambled characters. It is a one-way process: "
    "it is mathematically impossible to reconstruct the original password from its hash. To secure Lucy Chat, we use Bcrypt, "
    "the industry standard for securing login credentials."
)

pdf.add_page()
pdf.print_section_heading("5.2 Implementing Cryptographic Password Protection")
security_code = [
    "# ===================================================================",
    "# security.py - CRYPTOGRAPHIC HASHING MODULE (BCRYPT)",
    "# ===================================================================",
    "import bcrypt",
    "",
    "def encrypt_password(plain_password: str) -> bytes:",
    "    \"\"\"",
    "    Secures a password using a 12-round salt and one-way hashing.",
    "    \"\"\"",
    "    # Convert plain text to raw bytes",
    "    password_bytes = plain_password.encode('utf-8')",
    "    ",
    "    # Generate salt with high cost calculation rounds",
    "    salt = bcrypt.gensalt(rounds=12)",
    "    ",
    "    # Scramble the bytes under cryptographic algorithm",
    "    hashed_pass = bcrypt.hashpw(password_bytes, salt)",
    "    return hashed_pass",
    "",
    "def verify_password(plain_password: str, stored_hash: bytes) -> bool:",
    "    \"\"\"",
    "    Validates credentials by hashing the input with the stored salt.",
    "    \"\"\"",
    "    password_bytes = plain_password.encode('utf-8')",
    "    ",
    "    # Returns True if hashes match",
    "    return bcrypt.checkpw(password_bytes, stored_hash)",
    "",
    "# --- Sandbox Demonstration ---",
    "if __name__ == '__main__':",
    "    test_pass = 'Abyssinia2026'",
    "    my_hash = encrypt_password(test_pass)",
    "    print(f'Original: {test_pass}')",
    "    print(f'Hashed Output: {my_hash}')",
    "    print(f'Is Match?: {verify_password(test_pass, my_hash)}')"
]
pdf.print_code_block(security_code)

pdf.add_page()
pdf.print_section_heading("5.3 Hashing and Salting Mechanics Explained")
pdf.print_paragraph(
    "* bcrypt.gensalt(rounds=12): Generates a random cryptographic salt. Adding a salt ensures that even if two users "
    "have the exact same password, they will end up with entirely different hashes. Setting rounds=12 strikes a perfect balance "
    "between server performance and brute-force protection.\n\n"
    "* plain_password.encode('utf-8'): Cryptographic libraries cannot hash plain text string characters directly. We convert "
    "the text into standard UTF-8 binary byte format so the encryption algorithms can parse and scramble them safely.\n\n"
    "* bcrypt.checkpw(...): Decrypting a hashed password is mathematically impossible. When a user logs in, we simply hash "
    "their input using the exact same salt we saved on file. If the resulting hash matches the stored one, access is securely granted."
)

# ================= CHAPTER 6 =================
pdf.add_page()
pdf.print_chapter_title(6, "Enterprise Scaling & Global Deployment")
pdf.print_section_heading("6.1 Production Hosting & Database Migration")
pdf.print_paragraph(
    "While saving message lists in your RAM memory (st.session_state) works perfectly during development, restarting the "
    "application clears that memory. For production-grade deployment, we upgrade our backend to a relational SQLite or PostgreSQL database."
)
pdf.print_paragraph(
    "To take Lucy Chat global, we use services like Streamlit Community Cloud or Heroku. The cloud platform pulls "
    "your code repository directly from GitHub, handles security certificate (HTTPS) configurations, and serves "
    "your social platform live to local users in Addis Ababa and the global Ethiopian diaspora instantly."
)
pdf.print_paragraph(
    "This brings our comprehensive textbook to a close. You now have the fundamental knowledge of a software developer. "
    "Compile, edit, and expand this platform as you build your career in software development and cybersecurity!"
)

# Output PDF to local storage
pdf_filename = "Lucy_Chat_Software_Development_Master_Manual.pdf"
pdf.output(pdf_filename)

print(f"\n=========================================================")
print(f"SUCCESS: Master Manual generated successfully!")
print(f"File saved as: {os.path.abspath(pdf_filename)}")
print(f"=========================================================\n")