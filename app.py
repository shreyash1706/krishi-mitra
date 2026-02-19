import streamlit as st
import requests

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/chat"
USER_ID = "farmer_demo_123" # Hardcoded for testing

st.set_page_config(page_title="Krishi Mitra", page_icon="🚜", layout="centered")

# --- INITIALIZE SESSION STATE ---
# We use session state to remember the chat history and the database session ID
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaskar! I am Krishi Mitra. How can I help you with your farm today?", "agent": "system"}]
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# --- SIDEBAR (For Debugging) ---
with st.sidebar:
    st.header("⚙️ Developer Debug")
    st.info(f"**Current Session ID:** {st.session_state.session_id}")
    st.caption("Watch the terminal running FastAPI to see the live tool calls and thinking process.")
    
    if st.button("🗑️ Clear Chat & Reset Session", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Namaskar! I am Krishi Mitra. How can I help you with your farm today?", "agent": "system"}]
        st.session_state.session_id = None
        st.rerun()

# --- MAIN UI ---
st.title("🚜 Krishi Mitra")
st.caption("Your AI Farming Assistant - Ask about crops, pests, markets, and schemes!")
st.divider()

# 1. Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Show a small debug badge so you know which agent handled the response
        if msg["role"] == "assistant" and msg.get("agent") != "system":
            st.caption(f"🧭 Handled by: **{msg['agent'].upper()}** Agent")
        st.markdown(msg["content"])

# 2. Chat Input Trigger
if prompt := st.chat_input("E.g., What's the price of onion in Pune?"):
    
    # Append user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Call FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Krishi Mitra is analyzing your request..."):
            try:
                # Prepare payload
                payload = {
                    "user_id": USER_ID,
                    "query": prompt
                }
                # Attach session_id if it's an ongoing chat
                if st.session_state.session_id:
                    payload["session_id"] = st.session_state.session_id

                # Send Request
                response = requests.post(API_URL, json=payload)
                response.raise_for_status() 
                
                data = response.json()
                reply = data.get("reply", "Error: No reply generated.")
                agent_used = data.get("agent", "unknown")
                
                # Capture the new session ID if this was the first message
                if not st.session_state.session_id and data.get("session_id"):
                    st.session_state.session_id = data.get("session_id")

                # Render Response
                st.caption(f"🧭 Handled by: **{agent_used.upper()}** Agent")
                st.markdown(reply)

                # Save to UI state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply,
                    "agent": agent_used
                })

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Is your FastAPI server running on port 8000?")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")