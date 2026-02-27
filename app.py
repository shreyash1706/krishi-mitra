import streamlit as st
import requests
import json

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Krishi Mitra", page_icon="🚜", layout="wide")

API_URL = "http://127.0.0.1:8000/chat"

# --------------------------------------------------
# SESSION STATE INIT (MUST BE AT TOP)
# --------------------------------------------------

if "user_details" not in st.session_state:
    st.session_state.user_details = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


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

        # ✅ District Dropdown
        district = st.selectbox(
            "Select District",
            district_list
        )

        # ✅ Village Text Input
        village = st.text_input("Village / Taluka")

        submitted = st.form_submit_button("Enter Chat")

    if submitted:
        if not user_id or not name:
            st.error("User ID and Name required")
        else:
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

            st.rerun()

    st.stop()


# --------------------------------------------------
# SIDEBAR → CHATGPT STYLE
# --------------------------------------------------
with st.sidebar:

    st.title("🚜 Krishi Mitra")

    # NEW CHAT BUTTON
    if st.button("➕ New Chat", use_container_width=True):

        if st.session_state.messages:
            st.session_state.chat_history.append(
                st.session_state.messages.copy()
            )

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
    st.subheader("💬 Your Chats")

    for i, chat in enumerate(reversed(st.session_state.chat_history)):

        title = "Chat"
        for msg in chat:
            if msg["role"] == "user":
                title = msg["content"][:25]
                break

        if st.button(title, key=f"history_{i}"):
            st.session_state.messages = chat.copy()
            st.rerun()

    st.divider()

    st.subheader("👨‍🌾 Farmer Info")
    st.write(f"Name: {st.session_state.user_details['name']}")
    st.write(f"Village: {st.session_state.user_details['village']}")
    st.write(f"District: {st.session_state.user_details['district']}")


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

        st.markdown(msg["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------
if prompt := st.chat_input("Ask about crops, markets, pests..."):

    USER_ID = st.session_state.user_details["user_id"]

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                payload = {
                    "user_id": USER_ID,
                    "query": prompt,
                    "name": st.session_state.user_details["name"],
                    "village": st.session_state.user_details["village"],
                    "district": st.session_state.user_details["district"]
                }

                if st.session_state.session_id:
                    payload["session_id"] = st.session_state.session_id

                response = requests.post(API_URL, json=payload)
                data = response.json()

                reply = data.get("reply", "No reply")
                agent = data.get("agent")

                if not st.session_state.session_id:
                    st.session_state.session_id = data.get("session_id")

                if agent:
                    st.caption(f"🧭 Agent: {agent.upper()}")

                st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "agent": agent
                })

            except Exception:   
                st.error("Backend not running")