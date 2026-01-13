import streamlit as st

# ---------------- Page Setup ----------------
st.set_page_config(page_title="AutoStream Chatbot", layout="centered")
st.title("AutoStream Chatbot")

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "lead_step" not in st.session_state:
    st.session_state.lead_step = None  # None | name | email | platform

if "lead_data" not in st.session_state:
    st.session_state.lead_data = {}

# ---------------- Pricing & Policies ----------------
PRICING_TEXT = """
**Basic Plan**
- $29/month
- 10 videos/month
- 720p resolution

**Pro Plan**
- $79/month
- Unlimited videos
- 4K resolution
- AI captions

**Company Policies**
- No refunds after 7 days
- 24/7 support available only on Pro plan
"""

# ---------------- Bot Logic ----------------
def bot_reply(text):
    text = text.lower().strip()

    # ----- STEP-BY-STEP LEAD CAPTURE -----
    if st.session_state.lead_step == "name":
        st.session_state.lead_data["name"] = text
        st.session_state.lead_step = "email"
        return "What is your email address?"

    if st.session_state.lead_step == "email":
        st.session_state.lead_data["email"] = text
        st.session_state.lead_step = "platform"
        return "Which platform are you using? (YouTube / Instagram / TikTok)"

    if st.session_state.lead_step == "platform":
        st.session_state.lead_data["platform"] = text
        st.session_state.lead_step = None
        return (
            "✅ Lead captured successfully!\n\n"
            f"**Name:** {st.session_state.lead_data['name']}\n"
            f"**Email:** {st.session_state.lead_data['email']}\n"
            f"**Platform:** {st.session_state.lead_data['platform']}"
        )

    # ----- HIGH INTENT FIRST -----
    if "i want" in text or "try" in text or "buy" in text or "subscribe" in text:
        st.session_state.lead_step = "name"
        return "Great! What is your name?"

    # ----- PRICING -----
    if "pricing" in text or "price" in text or "plans" in text:
        return PRICING_TEXT

    # ----- GREETING -----
    if text in ["hi", "hello", "hey"]:
        return "Hello! Ask me about pricing or plans."

    return "Sorry, I can help with pricing or subscription plans."

# ---------------- Display Chat ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- Chat Input ----------------
user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    reply = bot_reply(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()