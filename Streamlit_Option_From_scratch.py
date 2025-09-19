import streamlit as st
from streamlit_oauth import OAuth2Component
import os

# Google OAuth configuration
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "your-google-client-id")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "your-google-client-secret")
REDIRECT_URI = "http://localhost:8501"

# Initialize OAuth component
oauth2 = OAuth2Component(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    refresh_token_endpoint="https://oauth2.googleapis.com/token",
    revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
)

st.title("Google Sign-In App")

# Check if user is already authenticated
if "user_info" not in st.session_state:
    # Show sign-in button
    result = oauth2.authorize_button(
        name="Sign in with Google",
        icon="https://developers.google.com/identity/images/g-logo.png",
        redirect_uri=REDIRECT_URI,
        scope="openid email profile",
        key="google_oauth",
        extras_params={"prompt": "select_account"},
    )
    
    if result and "token" in result:
        # Get user info from Google
        import requests
        headers = {"Authorization": f"Bearer {result['token']['access_token']}"}
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo", headers=headers
        ).json()
        st.session_state.user_info = user_info
        st.rerun()
else:
    # Show hello message with user name
    user_name = st.session_state.user_info.get("name", "User")
    st.success(f"Hello, {user_name}!")
    
    # Optional: Show sign out button
    if st.button("Sign Out"):
        del st.session_state.user_info
        st.rerun()