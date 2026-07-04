import streamlit as st
from utils.db import supabase


def login(email: str, password: str):

    try:
        res = supabase.table("users").select("*").eq(
            "email", email
        ).eq(
            "password", password
        ).execute()

        if len(res.data) > 0:

            user = res.data[0]

            st.session_state["user"] = user
            st.session_state["profile"] = user
            st.session_state["authenticated"] = True

            return True, None

        else:

            return False, "Invalid email or password"

    except Exception as e:

        return False, str(e)



def logout():

    st.session_state["authenticated"] = False

    if "user" in st.session_state:

        del st.session_state["user"]

    if "profile" in st.session_state:

        del st.session_state["profile"]



def require_login():

    if not st.session_state.get("authenticated"):

        st.warning("Please login first from Home page")

        st.stop()



def require_role(allowed_roles):

    if not st.session_state.get("authenticated"):

        st.warning("Please login first")

        st.stop()


    user = st.session_state.get("user")


    if user:

        role = user.get("role")


        if role not in allowed_roles:

            st.error("You do not have permission")

            st.stop()