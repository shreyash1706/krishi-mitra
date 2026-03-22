import streamlit as st
import requests
import json
import copy
import os
from dotenv import load_dotenv
from translator import KrishiMitraTranslator

# Load environment variables
load_dotenv()

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Krishi Mitra", page_icon="🚜", layout="wide")

API_URL = "http://127.0.0.1:8000/chat"

# Initialize translator
@st.cache_resource
def get_translator():
    api_key = os.getenv("SARVAM_API_KEY")
    if api_key:
        return KrishiMitraTranslator(api_key)
    return None

translator = get_translator()

# --------------------------------------------------
# LANGUAGE SUPPORT
# --------------------------------------------------
if "language" not in st.session_state:
    st.session_state.language = "English"  # Default language

if "last_language" not in st.session_state:
    st.session_state.last_language = st.session_state.language

# UI Translations
translations = {
    "English": {
        "title": "🚜 Krishi Mitra",
        "subtitle": "Your AI Farming Assistant",
        "farmer_details": "Farmer Details",
        "user_id": "User ID",
        "name": "Name",
        "select_district": "Select District",
        "village": "Village / Taluka",
        "enter_chat": "Enter Chat",
        "new_chat": "➕ New Chat",
        "your_chats": "💬 Your Chats",
        "farmer_info": "👨‍🌾 Farmer Info",
        "back_to_details": "🔙 Back to Details",
        "logout": "🚪 Logout",
        "logout_confirm": "⚠ Do you want to logout?",
        "yes_logout": "✅ Yes, Logout",
        "cancel": "❌ Cancel",
        "ask_question": "Ask about crops, markets, pests...",
        "analyzing": "Krishi-Mitra is analyzing your request",
        "backend_error": "Backend not running",
        "required_error": "User ID and Name required",
        "register_error": "Failed to connect to backend",
        "welcome": "Namaskar {}! How can I help you?",
        "new_chat_welcome": "New chat started. How can I help?",
        "agent_prefix": "🧭 Agent:",
        "chat_title": "Chat",
        "translation_status": "🌐 Translating..."
    },
    "Marathi": {
        "title": "🚜 कृषी मित्र",
        "subtitle": "तुमचा AI शेती सहाय्यक",
        "farmer_details": "शेतकरी तपशील",
        "user_id": "वापरकर्ता आयडी",
        "name": "नाव",
        "select_district": "जिल्हा निवडा",
        "village": "गाव / तालुका",
        "enter_chat": "चॅट सुरू करा",
        "new_chat": "➕ नवीन चॅट",
        "your_chats": "💬 तुमचे चॅट",
        "farmer_info": "👨‍🌾 शेतकरी माहिती",
        "back_to_details": "🔙 मागे",
        "logout": "🚪 बाहेर पडा",
        "logout_confirm": "⚠ तुम्हाला बाहेर पडायचे आहे का?",
        "yes_logout": "✅ होय, बाहेर पडा",
        "cancel": "❌ नको",
        "ask_question": "पिके, बाजारभाव, कीड याबद्दल विचारा...",
        "analyzing": "कृषी मित्र तुमची विचारणा विश्लेषित करत आहे",
        "backend_error": "बॅकएंड सुरू नाही",
        "required_error": "वापरकर्ता आयडी आणि नाव आवश्यक आहे",
        "register_error": "बॅकएंडशी कनेक्ट झाले नाही",
        "welcome": "नमस्कार {}! मी तुम्हाला कशी मदत करू शकते?",
        "new_chat_welcome": "नवीन चॅट सुरू झाला. मी कशी मदत करू?",
        "agent_prefix": "🧭 एजंट:",
        "chat_title": "चॅट",
        "translation_status": "🌐 भाषांतर करत आहे..."
    }
}

def t(key):
    """Get translation for current language"""
    # If user is logged in, use their stored language preference
    if st.session_state.user_details and "language" in st.session_state.user_details:
        lang = st.session_state.user_details["language"]
    else:
        lang = st.session_state.language
    return translations[lang].get(key, key)

def translate_to_english(text, source_lang):
    """Translate text to English if needed"""
    if not translator:
        return text
    
    if source_lang == 'mr':
        try:
            with st.spinner(t("translation_status")):
                translated = translator.translate(text, 'mr', 'en')
                return translated
        except Exception as e:
            st.warning(f"Translation to English failed: {e}")
            return text
    return text

def translate_to_marathi(text):
    """Translate English response to Marathi if needed"""
    if not translator:
        return text
    
    if st.session_state.language == "Marathi":
        try:
            translated = translator.translate(text, 'en', 'mr')
            return translated
        except Exception as e:
            st.warning(f"Translation to Marathi failed: {e}")
            return text
    return text

def update_welcome_message_language():
    """Update welcome message when language changes"""
    if st.session_state.user_details and st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "assistant" and msg.get("agent") == "system":
                name = st.session_state.user_details["name"]
                current_lang = st.session_state.user_details.get("language", "English")
                
                if current_lang == "Marathi":
                    # Check if message is in English and needs translation
                    if "Namaskar" in msg["content"] or "How can I help" in msg["content"]:
                        msg["content"] = "नमस्कार {}! मी तुम्हाला कशी मदत करू शकते?".format(name)
                else:
                    # Check if message is in Marathi and needs translation
                    if "नमस्कार" in msg["content"]:
                        msg["content"] = "Namaskar {}! How can I help you?".format(name)
                break  # Only update the first system message

# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------
if "user_details" not in st.session_state:
    st.session_state.user_details = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

if "viewing_history" not in st.session_state:
    st.session_state.viewing_history = False

# --------------------------------------------------
# LOAD DISTRICT DATA
# --------------------------------------------------
try:
    with open("maharashtra_district_coords.json", "r") as f:
        district_data = json.load(f)
    district_list = sorted(list(district_data.keys()))
except FileNotFoundError:
    district_list = ["Ahmednagar", "Pune", "Nashik", "Nagpur", "Kolhapur"]
    st.warning("District coordinates file not found. Using default districts.")

# --------------------------------------------------
# PAGE 1 → FARMER DETAILS
# --------------------------------------------------
if st.session_state.user_details is None:

    st.title(t("title"))
    st.subheader(t("farmer_details"))

    # Language selector at top
    col1, col2 = st.columns([3, 1])
    with col2:
        language = st.selectbox(
            "🌐 Language / भाषा",
            ["English", "Marathi"],
            index=0 if st.session_state.language == "English" else 1
        )
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()

    with st.form("user_form"):
        user_id = st.text_input(t("user_id"))
        name = st.text_input(t("name"))
        district = st.selectbox(t("select_district"), district_list)
        village = st.text_input(t("village"))

        submitted = st.form_submit_button(t("enter_chat"))

    if submitted:
        if not user_id or not name:
            st.error(t("required_error"))
        else:
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/register",
                    json={
                        "user_id": user_id,
                        "name": name,
                        "village": village,
                        "district": district
                    },
                    timeout=10
                )
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                st.error(f"{t('register_error')}: {e}")
                st.stop()

            # Capture the current language at registration time
            current_lang = st.session_state.language
            
            st.session_state.user_details = {
                "user_id": user_id,
                "name": name,
                "village": village,
                "district": district,
                "language": current_lang
            }

            # Generate welcome message in the correct language
            if current_lang == "Marathi":
                welcome_msg = "नमस्कार {}! मी तुम्हाला कशी मदत करू शकते?".format(name)
            else:
                welcome_msg = "Namaskar {}! How can I help you?".format(name)
            
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": welcome_msg,
                    "agent": "system",
                    "original_content": welcome_msg
                }
            ]

            st.session_state.viewing_history = False
            st.rerun()

    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.title(t("title"))

    # Language switcher in sidebar
    language = st.selectbox(
        "🌐 Language / भाषा",
        ["English", "Marathi"],
        index=0 if st.session_state.language == "English" else 1
    )
    if language != st.session_state.language:
        st.session_state.language = language
        # Update user_details language if logged in
        if st.session_state.user_details:
            st.session_state.user_details["language"] = language
            # Update welcome message to new language
            update_welcome_message_language()
        st.rerun()

    st.divider()

    # ➕ NEW CHAT
    if st.button(t("new_chat"), use_container_width=True):

        current_chat = st.session_state.messages

        if (
            not st.session_state.viewing_history and
            len(current_chat) > 1
        ):
            st.session_state.chat_history.append(
                copy.deepcopy(current_chat)
            )

        st.session_state.viewing_history = False

        # Get new chat welcome message in current language
        if st.session_state.language == "Marathi":
            new_chat_msg = "नवीन चॅट सुरू झाला. मी कशी मदत करू?"
        else:
            new_chat_msg = "New chat started. How can I help?"
        
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": new_chat_msg,
                "agent": "system",
                "original_content": new_chat_msg
            }
        ]

        st.session_state.session_id = None
        st.rerun()

    st.divider()

    # 💬 CHAT HISTORY
    st.subheader(t("your_chats"))

    for i, chat in enumerate(reversed(st.session_state.chat_history)):

        title = t("chat_title")
        for msg in chat:
            if msg["role"] == "user":
                # Truncate to 25 chars
                title = msg["content"][:25] if len(msg["content"]) > 25 else msg["content"]
                break

        if st.button(title, key=f"history_{i}"):
            st.session_state.messages = copy.deepcopy(chat)
            st.session_state.session_id = None
            st.session_state.viewing_history = True
            st.rerun()

    st.divider()

    # 👨‍🌾 FARMER INFO
    st.subheader(t("farmer_info"))
    st.write(f"{t('name')}: {st.session_state.user_details['name']}")
    st.write(f"{t('village')}: {st.session_state.user_details['village'] or 'Not specified'}")
    st.write(f"{t('select_district')}: {st.session_state.user_details['district']}")

    st.divider()

    # 🔙 BACK BUTTON
    if st.button(t("back_to_details"), use_container_width=True):
        st.session_state.user_details = None
        st.session_state.messages = []
        st.session_state.session_id = None
        st.session_state.show_logout_confirm = False
        st.session_state.viewing_history = False
        st.rerun()

    # --------------------------------------------------
    # LOGOUT WITH CONFIRMATION
    # --------------------------------------------------
    if not st.session_state.show_logout_confirm:
        if st.button(t("logout"), use_container_width=True):
            st.session_state.show_logout_confirm = True
            st.rerun()

    if st.session_state.show_logout_confirm:
        st.warning(t("logout_confirm"))

        col1, col2 = st.columns(2)

        with col1:
            if st.button(t("yes_logout"), use_container_width=True):
                st.session_state.clear()
                st.rerun()

        with col2:
            if st.button(t("cancel"), use_container_width=True):
                st.session_state.show_logout_confirm = False
                st.rerun()

# --------------------------------------------------
# MAIN CHAT UI
# --------------------------------------------------
st.title(t("title"))
st.caption(t("subtitle"))
st.divider()

# Display chat messages with translation support
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        agent = msg.get("agent")

        if msg["role"] == "assistant" and agent and agent != "system":
            st.caption(f"{t('agent_prefix')} {agent.upper()}")

        # Display content (already in user's preferred language)
        st.markdown(msg["content"])

# --------------------------------------------------
# CHAT INPUT WITH TRANSLATION
# --------------------------------------------------
if prompt := st.chat_input(t("ask_question")):

    st.session_state.viewing_history = False

    USER_ID = st.session_state.user_details["user_id"]
    
    # Detect language of user input
    if translator:
        input_lang = translator.detect_language(prompt)
    else:
        input_lang = 'en'  # Default to English if translator not available
    
    # Add user message to chat (in original language)
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "original_content": prompt,
        "language": input_lang
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner(t("analyzing")):
            
            try:
                # Translate query to English for LLM if needed
                if input_lang == 'mr' and translator:
                    english_query = translate_to_english(prompt, input_lang)
                else:
                    english_query = prompt
                
                # Send to backend
                payload = {
                    "user_id": USER_ID,
                    "query": english_query,
                }
                
                if st.session_state.session_id:
                    payload["session_id"] = st.session_state.session_id
                
                response = requests.post(API_URL, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()
                
                reply = data.get("reply", "No reply")
                agent = data.get("agent")
                
                # Translate response to user's language if needed
                if st.session_state.language == "Marathi" and translator:
                    final_reply = translate_to_marathi(reply)
                else:
                    final_reply = reply
                
                if not st.session_state.session_id:
                    st.session_state.session_id = data.get("session_id")
                
                if agent:
                    st.caption(f"{t('agent_prefix')} {agent.upper()}")
                
                st.markdown(final_reply)
                
                # Store response in chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_reply,
                    "original_content": reply,
                    "agent": agent,
                    "language": st.session_state.language
                })
                
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to backend. Make sure the server is running.")
            except requests.exceptions.RequestException as e:
                st.error(f"{t('backend_error')}: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")