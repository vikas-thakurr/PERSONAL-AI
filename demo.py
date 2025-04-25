import streamlit as st
import ollama
import base64
import os

st.set_page_config(page_title="Personal AI")

# Load background image
def get_base64(background):
    if os.path.exists(background):
        with open(background, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

bin_str = get_base64("background.png")

if bin_str:
    st.markdown(f"""
        <style>
            .main {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
        """, unsafe_allow_html=True)

# Session state
st.session_state.setdefault('conversation_history', [])

# AI response generation
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    try:
        response = ollama.chat(model="llama3:8b", messages=st.session_state['conversation_history'])
        ai_response = response['message']['content']
        st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
        return ai_response
    except Exception as e:
        return f"Error: {e}"

def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    try:
        response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"

def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    try:
        response = ollama.chat(model="llama3:8b", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"

# UI
st.title("🤖 Personal Support AI Agent🤖")

for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Give me a positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")

with col3:
    if st.button("About Creator"):
        st.markdown("""
        **Creator:** Vikas Thakur  
        **Affiliation:** Student of Delhi Skill and Entrepreneurship University  
        **Project:** Final Semester Major Project
        **Submitted to:** Sh.  Gurvinder Singh 
        """)
