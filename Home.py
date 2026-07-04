import sys
import os

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "utils"
    )
)
import streamlit as st
from auth import login, logout
from utils.db import supabase

st.set_page_config(page_title="Hospital Management System", page_icon="🏥", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ---------------- LOGIN SCREEN ----------------
if not st.session_state["authenticated"]:
    st.title("🏥 Hospital Management System")
    st.subheader("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                success, error = login(email, password)
                if success:
                    st.success("Login successful! Loading dashboard...")
                    st.rerun()
                else:
                    st.error(f"Login failed: {error}")

    st.info(
        "First time setup? An admin needs to create the very first account. "
        "See README.md → 'Creating the first admin user'."
    )

# ---------------- DASHBOARD (LOGGED IN) ----------------
else:
    profile = st.session_state["profile"]
    st.title(f"🏥 Welcome, {profile['full_name']}")
    st.caption(f"Role: {profile['role'].title()}")
    st.write("Use the sidebar to navigate to different modules: Patients, Doctors, Appointments, Billing, Pharmacy.")

    st.divider()
    st.subheader("📊 Quick Overview")

    col1, col2, col3, col4 = st.columns(4)
    try:
        with col1:
            r = supabase.table("patients").select("id", count="exact").execute()
            st.metric("Total Patients", r.count)
        with col2:
            r = supabase.table("doctors").select("id", count="exact").execute()
            st.metric("Total Doctors", r.count)
        with col3:
            r = supabase.table("appointments").select("id", count="exact").eq("status", "Scheduled").execute()
            st.metric("Upcoming Appointments", r.count)
        with col4:
            r = supabase.table("bills").select("id", count="exact").eq("payment_status", "Pending").execute()
            st.metric("Pending Bills", r.count)
    except Exception as e:
        st.warning(f"Could not load stats — check your Supabase connection. ({e})")

    st.sidebar.success(f"Logged in as {profile['full_name']}")
    if st.sidebar.button("🚪 Logout"):
        logout()
        st.rerun()
