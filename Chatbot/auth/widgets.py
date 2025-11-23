
import streamlit as st
from streamlit_cookies_manager import CookieManager




class AuthWidget:
    def __init__(self, auth_service, cookie_name="chatbot_session"):
        self.auth = auth_service
        self.cookies = CookieManager(prefix="chatbot")  
        if not self.cookies.ready():
            st.stop()

        self.cookie_name = cookie_name

    def login_view(self):
        st.subheader("Login")
        idf = st.text_input("Email or Username")
        login_pwd = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Login"):
            try:
                sess = self.auth.login(idf, login_pwd)
                self.cookies[self.cookie_name] = sess.token
                self.cookies.save()
                st.success("Logged in")
                st.experimental_rerun()
            except Exception as e:
                st.error(str(e))

    def register_view(self):
        st.subheader("Register")
        email = st.text_input("Email")
        username = st.text_input("Username")
        pwd = st.text_input("Password", type="password", key="register_pwd")

        if st.button("Create account"):
            try:
                user = self.auth.register(email, username, pwd)
                st.success(f"User {user.username} created. Please login.")
            except Exception as e:
                st.error(str(e))

    def logout_button(self):
        if st.button("Logout"):
            token = self.cookies.get(self.cookie_name)
            if token:
                self.auth.sessions.delete(token)
            self.cookies[self.cookie_name] = ""
            self.cookies.save()
            st.experimental_rerun()

    def current_session(self):
        token = self.cookies.get(self.cookie_name)
        return self.auth.validate_token(token) if token else None
