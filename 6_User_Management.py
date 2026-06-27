import streamlit as st
import pandas as pd
from utils.auth import require_role
from utils.db import supabase

st.set_page_config(page_title="User Management", page_icon="👤", layout="wide")
require_role(["admin"])

st.title("👤 Staff / User Management")
st.caption("Create login accounts for doctors, receptionists, and pharmacists.")

tab1, tab2 = st.tabs(["📋 View Staff", "➕ Add New User"])

# ---------------- VIEW ----------------
with tab1:
    data = supabase.table("profiles").select("*").order("full_name").execute().data
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# ---------------- ADD NEW ----------------
with tab2:
    st.info(
        "New users get a login (email + password) and a role. "
        "They'll use these exact credentials on the Home page to log in."
    )
    with st.form("add_user", clear_on_submit=True):
        full_name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        password = st.text_input("Password*", type="password")
        role = st.selectbox("Role", ["doctor", "receptionist", "pharmacist", "admin"])
        department = st.text_input("Department")
        submit = st.form_submit_button("Create User")

        if submit:
            if not full_name.strip() or not email.strip() or not password:
                st.error("Full name, email and password are required.")
            else:
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    user_id = res.user.id
                    supabase.table("profiles").insert({
                        "id": user_id,
                        "full_name": full_name.strip(),
                        "role": role,
                        "department": department,
                    }).execute()
                    st.success(f"User '{full_name}' created with role '{role}'.")
                    st.caption(
                        "Note: depending on your Supabase Auth email-confirmation settings, "
                        "this user may need to confirm their email before they can log in."
                    )
                except Exception as e:
                    st.error(f"Error creating user: {e}")
