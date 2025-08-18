import streamlit as st

# Page config
st.set_page_config(page_title="Counter App", page_icon="🔢", layout="centered")

# Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔢 Simple Counter App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Click ➕ or ➖ to change the number. It's that easy!</p>", unsafe_allow_html=True)
st.divider()

# Initialize counter
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("➖", use_container_width=True):
        st.session_state.counter -= 1

with col2:
    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.counter}</h2>", unsafe_allow_html=True)

with col3:
    if st.button("➕", use_container_width=True):
        st.session_state.counter += 1

# Footer
st.divider()
