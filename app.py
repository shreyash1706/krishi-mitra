import streamlit as st
import requests
import json
import copy
import os
from dotenv import load_dotenv
from translator import KrishiMitraTranslator

load_dotenv()

# Initialize translator
@st.cache_resource
def get_translator():
    api_key = os.getenv("SARVAM_API_KEY")
    if api_key:
        return KrishiMitraTranslator(api_key)
    return None

translator = get_translator()

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Krishi Mitra", page_icon="🚜", layout="wide")

API_URL = "http://127.0.0.1:8000/chat"

# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------

if "user_details" not in st.session_state:
    st.session_state.user_details = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

# ✅ NEW FLAG TO PREVENT DUPLICATION
if "viewing_history" not in st.session_state:
    st.session_state.viewing_history = False


# --------------------------------------------------
# LOAD DISTRICT DATA
# --------------------------------------------------

with open("maharashtra_district_coords.json", "r") as f:
    district_data = json.load(f)

district_list = sorted(list(district_data.keys()))


# --------------------------------------------------
# PAGE 1 → FARMER DETAILS
# --------------------------------------------------

if st.session_state.user_details is None:

    st.title("🚜 Krishi Mitra")
    st.subheader("Farmer Details")

    with st.form("user_form"):
        user_id = st.text_input("User ID")
        name = st.text_input("Name")
        district = st.selectbox("Select District", district_list)
        village = st.text_input("Village / Taluka")

        submitted = st.form_submit_button("Enter Chat")

    if submitted:
        if not user_id or not name:
            st.error("User ID and Name required")
        else:
            # 1️⃣ Hit the new FastAPI registration endpoint immediately
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/register", # Adjust port/URL if hosted elsewhere
                    json={
                        "user_id": user_id,
                        "name": name,
                        "village": village,
                        "district": district
                    }
                )
                response.raise_for_status() # Raise an error if the backend fails
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")
                st.stop()

            # 2️⃣ Save to session state
            st.session_state.user_details = {
                "user_id": user_id,
                "name": name,
                "village": village,
                "district": district
            }

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"Namaskar {name}! How can I help you?",
                    "agent": "system"
                }
            ]

            st.session_state.viewing_history = False
            st.rerun()

    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🚜 Krishi Mitra")

    # ➕ NEW CHAT
    if st.button("➕ New Chat", use_container_width=True):

        current_chat = st.session_state.messages

        # ✅ Save only if:
        # 1. Not viewing history
        # 2. Chat has real conversation
        if (
            not st.session_state.viewing_history and
            len(current_chat) > 1
        ):
            st.session_state.chat_history.append(
                copy.deepcopy(current_chat)
            )

        # Reset flag
        st.session_state.viewing_history = False

        # Start fresh chat
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "New chat started. How can I help?",
                "agent": "system"
            }
        ]

        st.session_state.session_id = None
        st.rerun()

    st.divider()

    # 💬 CHAT HISTORY
    st.subheader("💬 Your Chats")

    for i, chat in enumerate(reversed(st.session_state.chat_history)):

        title = "Chat"
        for msg in chat:
            if msg["role"] == "user":
                title = msg["content"][:25]
                break

        if st.button(title, key=f"history_{i}"):

            st.session_state.messages = copy.deepcopy(chat)
            st.session_state.session_id = None
            st.session_state.viewing_history = True  # ✅ Important
            st.rerun()

    st.divider()

    # 👨‍🌾 FARMER INFO
    st.subheader("👨‍🌾 Farmer Info")
    st.session_state.language = st.selectbox(
        "🌍 Select Language",
        ["English", "Marathi"],
        index=0 if st.session_state.language=="English" else 1
    )
    st.write(f"Name: {st.session_state.user_details['name']}")
    st.write(f"Village: {st.session_state.user_details['village']}")
    st.write(f"District: {st.session_state.user_details['district']}")

    st.divider()

    # 🔙 BACK BUTTON
    if st.button("🔙 Back to Details", use_container_width=True):
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
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.show_logout_confirm = True
            st.rerun()

    if st.session_state.show_logout_confirm:

        st.warning("⚠ Do you want to logout?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Yes, Logout", use_container_width=True):
                st.session_state.clear()
                st.rerun()

        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_logout_confirm = False
                st.rerun()


# --------------------------------------------------
# MAIN CHAT UI
# --------------------------------------------------

st.title("🚜 Krishi Mitra")
st.caption("Your AI Farming Assistant")
st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        agent = msg.get("agent")

        if msg["role"] == "assistant" and agent and agent != "system":
            st.caption(f"🧭 Agent: {agent.upper()}")

        if msg.get("reasoning"):
            formatted_reasoning = msg['reasoning'].replace('\n', '\n> ')
            st.markdown(f"> 🤔 **Thought Process:**\n> {formatted_reasoning}\n\n---\n")

        st.markdown(msg["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

if prompt := st.chat_input("Ask about crops, markets, pests..."):

    st.session_state.viewing_history = False  # ✅ Important

    USER_ID = st.session_state.user_details["user_id"]

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            english_query = prompt
            
            # Translate Marathi user input to English for accurate RAG Retrieval
            if st.session_state.language == "Marathi" and translator:
                # Basic check if input is Marathi
                if translator.detect_language(prompt) == 'mr':
                    with st.spinner("🌍 Translating query..."):
                        english_query = translator.translate(prompt, 'mr', 'en')

            payload = {
                "user_id": USER_ID,
                "query": english_query, # Send English for precise vector match
                "output_language": st.session_state.language # Tell backend to streams Marathi
            }

            if st.session_state.session_id:
                payload["session_id"] = st.session_state.session_id

            st.session_state.current_agent = "Crop Planner"
            agent_placeholder = st.empty()
            
            reasoning_text = ""
            content_text = ""
            
            # Create placeholders using st.status for a ChatGPT-like "Thinking..."
            status = st.status("🧠 Thinking...", expanded=False)
            with status:
                reasoning_placeholder = st.empty()
            
            content_placeholder = st.empty()
            
            # Fetch and process the stream manually to handle both reasoning and chunks
            with requests.post(API_URL, json=payload, stream=True) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if data.get("agent"):
                                st.session_state.current_agent = data["agent"]
                                agent_placeholder.caption(f"🧭 Agent: {data['agent'].upper()}")
                            if not st.session_state.session_id and data.get("session_id"):
                                st.session_state.session_id = data.get("session_id")
                            
                            if "reasoning" in data:
                                reasoning_text += data["reasoning"]
                                reasoning_placeholder.markdown(reasoning_text + "▌")
                            
                            if "chunk" in data:
                                # When main content starts, thinking is mostly done
                                if status is not None:
                                    status.update(label="Finished thinking", state="complete", expanded=False)
                                    reasoning_placeholder.markdown(reasoning_text) # remove cursor
                                    status = None
                                content_text += data["chunk"]
                                content_placeholder.markdown(content_text + "▌")
                        except json.JSONDecodeError:
                            pass
            
            # Clean up when stream ends
            if status is not None:
                status.update(label="Finished thinking", state="complete", expanded=False)
                if reasoning_text:
                    reasoning_placeholder.markdown(reasoning_text)
                else:
                    reasoning_placeholder.markdown("*(Completed in background)*")
            
            # Post the thought process visibly in the output
            final_display_text = ""
            if reasoning_text:
                formatted_reasoning = reasoning_text.replace('\n', '\n> ')
                final_display_text += f"> 🤔 **Thought Process:**\n> {formatted_reasoning}\n\n---\n\n"
            final_display_text += content_text
            
            content_placeholder.markdown(final_display_text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": content_text,
                "reasoning": reasoning_text,
                "agent": st.session_state.current_agent
            })

        except requests.exceptions.RequestException as e:
            st.error(f"Backend HTTP Exception: {e}")
        except Exception as e:
            st.error(f"Backend disconnected or unreachable: {e}")
