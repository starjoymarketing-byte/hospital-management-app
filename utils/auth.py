import streamlit as st
from utils.db import supabase


def login(email: str, password: str):
    """Attempt to log in via Supabase Auth and load the user's profile/role."""
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = res.user
        profile_res = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
        st.session_state["user"] = user
        st.session_state["profile"] = profile_res.data
        st.session_state["authenticated"] = True
        return True, None
    except Exception as e:
        return False, str(e)


def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    for key in ["user", "profile", "authenticated"]:
        st.session_state.pop(key, None)


def require_login():
    """Stop page execution if the user isn't logged in."""
    if not st.session_state.get("authenticated"):
        st.warning("⚠️ Please log in first from the Home page (sidebar).")
        st.stop()


def require_role(allowed_roles: list[str]):
    """Stop page execution if the logged-in user's role isn't allowed here."""
    require_login()
    role = st.session_state["profile"]["role"]
    if role not in allowed_roles:
        st.error(f"🚫 Your role ('{role}') doesn't have access to this page.")
        st.stop()
