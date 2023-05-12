import streamlit as st

# Custom CSS for chat bubbles
st.markdown(
    """
<style>
.bubble {
    display: inline-block;
    border-radius: 20px;
    padding: 10px 15px;
    background-color: #f0f0f0;
    margin-bottom: 5px;
    width: fit-content;
    max-width: 70%;
    position: relative;
}
.bubble-user {
    background-color: #4b79f3;
    color: white;
    margin-left: 30%;
}
.bubble::before {
    content: '';
    position: absolute;
    width: 0;
    height: 0;
}
.bubble-user::before {
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-right: 8px solid #4b79f3;
    left: -8px;
    top: 10px;
}
.bubble-bot::before {
    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-left: 8px solid #f0f0f0;
    right: -8px;
    top: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# Chat interface
st.title("Chat Interface")

chat_history = []

user_input = st.text_input("Type your message:")
if st.button("Send"):
    chat_history.append(("user", user_input))
    chat_history.append(("bot", f"Response to: {user_input}"))  # Replace with your response logic
    user_input = ""

# Display chat history
for role, message in chat_history:
    if role == "user":
        st.markdown(f'<div class="bubble bubble-user"><img src="img/user.png" width="20" style="vertical-align: middle;">&nbsp;{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble bubble-bot"><img src="img/bot.png" width="20" style="vertical-align: middle;">&nbsp;{message}</div>', unsafe_allow_html=True)