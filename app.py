import streamlit as st
import requests
import sqlite3
import os
from dotenv import load_dotenv
from translator import KrishiMitraTranslator

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()  # Load variables from .env file

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/chat"
USER_ID = "farmer_demo_123"  # Hardcoded for testing
# Get API key from environment variable
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY')
DB_NAME = "krishi.db"  # Match your database name

# Validate API key is present
if not SARVAM_API_KEY:
    st.error("⚠️ SARVAM_API_KEY not found in environment variables. Please check your .env file.")
    st.stop()

# --- DATABASE INITIALIZATION FUNCTION ---
def init_database():
    """Initialize the database with required tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        # Create farmers table
        c.execute('''
        CREATE TABLE IF NOT EXISTS farmers
        (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        village TEXT,
        district TEXT,
        lat_long TEXT,
        soil_details TEXT,
        attributes_json TEXT
        )'''
        )
        
        # Create crop_cycles table
        c.execute('''
        CREATE TABLE IF NOT EXISTS crop_cycles (
            cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT, 
            crop_name TEXT,
            variety TEXT,
            season TEXT,
            year INTEGER,
            sowing_date TEXT,
            status INTEGER CHECK (status IN (0,1)),
            yield TEXT,
            issues_log_json TEXT,
            FOREIGN KEY (user_id) REFERENCES farmers (user_id)
        )''')
        
        # Create sessions table with TEXT session_id to match FastAPI expectations
        c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            agent_mode TEXT,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES farmers(user_id)
        )''')
        
        # Create messages table
        c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(session_id)
        )''')
        
        conn.commit()
        conn.close()
        
        # Create a default farmer if not exists
        create_default_farmer()
        
        return True
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        return False

def create_default_farmer():
    """Create a default farmer for demo purposes"""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        # Check if farmer exists
        c.execute("SELECT user_id FROM farmers WHERE user_id = ?", (USER_ID,))
        if not c.fetchone():
            c.execute('''
            INSERT INTO farmers (user_id, name, village, district, attributes_json)
            VALUES (?, ?, ?, ?, ?)
            ''', (USER_ID, "Demo Farmer", "Demo Village", "Demo District", "{}"))
            conn.commit()
            print(f"✅ Created default farmer: {USER_ID}")
        
        conn.close()
    except Exception as e:
        print(f"⚠️ Could not create default farmer: {e}")

# Initialize translator (cached to avoid re-initializing on every rerun)
@st.cache_resource
def init_translator():
    return KrishiMitraTranslator(SARVAM_API_KEY)

# Initialize database on app start
@st.cache_resource
def init_db_once():
    return init_database()

# Run database initialization
db_initialized = init_db_once()
if not db_initialized:
    st.warning("⚠️ Database initialization issue. Some features may not work properly.")

translator = init_translator()

st.set_page_config(page_title="Krishi Mitra", page_icon="🚜", layout="centered")

# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaskar! I am Krishi Mitra. How can I help you with your farm today?", "agent": "system"}]
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "last_input_lang" not in st.session_state:
    st.session_state.last_input_lang = "en"
if "auto_translate" not in st.session_state:
    st.session_state.auto_translate = True

# --- SIDEBAR (For Debugging) ---
with st.sidebar:
    st.header("⚙️ Developer Debug")
    st.info(f"**Current Session ID:** {st.session_state.session_id}")
    
    # Database status indicator
    db_status = "✅ Connected" if db_initialized else "❌ Issues"
    st.caption(f"**Database:** {db_status}")
    
    # API Key status (don't show actual key for security)
    api_status = "✅ Configured" if SARVAM_API_KEY else "❌ Missing"
    st.caption(f"**Sarvam API:** {api_status}")
    
    # Show last detected language
    last_lang = st.session_state.get("last_input_lang", "en")
    lang_display = "🇮🇳 Marathi" if last_lang == "mr" else "🇬🇧 English"
    st.caption(f"**Last input language:** {lang_display}")
    
    # Optional: Add translation toggle
    st.session_state.auto_translate = st.checkbox("🔤 Auto-translate Marathi", 
                                                  value=st.session_state.auto_translate,
                                                  help="Automatically detect and translate Marathi queries")
    
    # Database debug button
    if st.button("🔧 Check Database", use_container_width=True):
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = c.fetchall()
            st.success(f"Tables: {[t[0] for t in tables]}")
            
            # Check sessions
            c.execute("SELECT COUNT(*) FROM sessions")
            session_count = c.fetchone()[0]
            st.info(f"Sessions: {session_count}")
            
            conn.close()
        except Exception as e:
            st.error(f"DB Error: {e}")
    
    st.caption("Watch the terminal running FastAPI to see the live tool calls and thinking process.")
    
    if st.button("🗑️ Clear Chat & Reset Session", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Namaskar! I am Krishi Mitra. How can I help you with your farm today?", "agent": "system"}]
        st.session_state.session_id = None
        st.session_state.last_input_lang = "en"
        st.rerun()

# --- MAIN UI ---
st.title("🚜 Krishi Mitra")
st.caption("Your AI Farming Assistant - Ask about crops, pests, markets, and schemes! | मराठीतही विचारा")
st.divider()

# 1. Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Show language indicator if available
        if msg.get("lang") == "mr":
            st.caption("🇮🇳 **Marathi**")
        elif msg.get("lang") == "en" and msg["role"] == "user":
            st.caption("🇬🇧 **English**")
            
        # Show agent badge for assistant messages
        if msg["role"] == "assistant" and msg.get("agent") != "system":
            st.caption(f"🧭 Handled by: **{msg['agent'].upper()}** Agent")
        st.markdown(msg["content"])

# 2. Chat Input Trigger
if prompt := st.chat_input("E.g., What's the price of onion in Pune? | कांद्याचे भाव काय आहेत?"):
    
    # STEP 1: Detect language of input
    input_lang = translator.detect_language(prompt)
    st.session_state.last_input_lang = input_lang
    
    # Show language indicator
    lang_emoji = "🇮🇳" if input_lang == "mr" else "🇬🇧"
    lang_name = "Marathi" if input_lang == "mr" else "English"
    
    # STEP 2: Translate to English if Marathi
    if input_lang == "mr" and st.session_state.auto_translate:
        with st.spinner("🔄 Translating to English..."):
            try:
                english_prompt = translator.translate(prompt, 'mr', 'en')
                # Store original for display
                display_prompt = prompt
                api_query = english_prompt
                st.session_state.messages.append({
                    "role": "user", 
                    "content": display_prompt,
                    "lang": input_lang,
                    "translated": english_prompt
                })
            except Exception as e:
                st.error(f"Translation error: {e}")
                # Fallback to original
                display_prompt = prompt
                api_query = prompt
                st.session_state.messages.append({
                    "role": "user", 
                    "content": display_prompt,
                    "lang": input_lang
                })
        with st.chat_message("user"):
            st.caption(f"{lang_emoji} **{lang_name}**")
            st.markdown(display_prompt)
    else:
        # English or translation disabled
        display_prompt = prompt
        api_query = prompt
        st.session_state.messages.append({
            "role": "user", 
            "content": display_prompt,
            "lang": input_lang
        })
        with st.chat_message("user"):
            if input_lang == "mr":
                st.caption(f"{lang_emoji} **{lang_name}**")
            st.markdown(display_prompt)

    # 3. Call FastAPI Backend (always with English query)
    with st.chat_message("assistant"):
        with st.spinner("Krishi Mitra is analyzing your request..."):
            try:
                # Prepare payload - ALWAYS send English query to backend
                payload = {
                    "user_id": USER_ID,
                    "query": api_query
                }
                # Attach session_id if it's an ongoing chat
                if st.session_state.session_id:
                    payload["session_id"] = st.session_state.session_id

                # Send Request with timeout
                response = requests.post(API_URL, json=payload, timeout=60)
                response.raise_for_status() 
                
                data = response.json()
                english_reply = data.get("reply", "Error: No reply generated.")
                agent_used = data.get("agent", "unknown")
                
                # STEP 4: Translate back to Marathi if original was Marathi
                if input_lang == "mr" and st.session_state.auto_translate:
                    with st.spinner("🔄 Translating response to Marathi..."):
                        try:
                            final_reply = translator.translate(english_reply, 'en', 'mr')
                        except Exception as e:
                            st.warning(f"Translation error, showing English response: {e}")
                            final_reply = english_reply
                    st.caption(f"{lang_emoji} **Marathi Response**")
                else:
                    final_reply = english_reply
                
                # Capture the new session ID if this was the first message
                if not st.session_state.session_id and data.get("session_id"):
                    st.session_state.session_id = data.get("session_id")

                # Render Response
                if agent_used != "unknown":
                    st.caption(f"🧭 Handled by: **{agent_used.upper()}** Agent")
                st.markdown(final_reply)

                # Save to UI state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": final_reply,
                    "agent": agent_used,
                    "lang": input_lang,
                    "original_english": english_reply if input_lang == "mr" else None
                })

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Is your FastAPI server running on port 8000?")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The backend is taking too long to respond.")
            except requests.exceptions.HTTPError as e:
                if response.status_code == 500:
                    st.error("❌ Backend server error. Check the FastAPI terminal for details.")
                    # Try to get more details
                    try:
                        error_detail = response.json().get("detail", "No details")
                        st.caption(f"Error detail: {error_detail}")
                    except:
                        pass
                else:
                    st.error(f"❌ HTTP Error: {e}")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")