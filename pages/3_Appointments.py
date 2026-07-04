import streamlit as st
import pandas as pd
from datetime import date, time
from utils.auth import require_role
from utils.db import supabase

st.set_page_config(page_title="Appointments", page_icon="📅", layout="wide")
require_role(["admin", "doctor", "receptionist"])

st.title("📅 Appointments & Scheduling")

patients = supabase.table("patients").select("id, full_name").order("full_name").execute().data
doctors = supabase.table("doctors").select("id, full_name, specialization").order("full_name").execute().data
patient_map = {p["full_name"]: p["id"] for p in patients}
doctor_map = {f'{d["full_name"]} ({d["specialization"] or "General"})': d["id"] for d in doctors}

tab1, tab2 = st.tabs(["📋 View / Manage", "➕ Book New Appointment"])

# ---------------- VIEW / MANAGE ----------------
with tab1:
    data = (
        supabase.table("appointments")
        .select("*, patients(full_name), doctors(full_name)")
        .order("appointment_date", desc=True)
        .execute()
        .data
    )

    rows = []
    for a in data:
        rows.append({
            "id": a["id"],
            "Patient": a["patients"]["full_name"] if a.get("patients") else "—",
            "Doctor": a["doctors"]["full_name"] if a.get("doctors") else "—",
            "Date": a["appointment_date"],
            "Time": a["appointment_time"],
            "Reason": a["reason"],
            "Status": a["status"],
        })
    df = pd.DataFrame(rows)

    status_filter = st.selectbox("Filter by status", ["All", "Scheduled", "Completed", "Cancelled"])
    if status_filter != "All" and not df.empty:
        df = df[df["Status"] == status_filter]

    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.subheader("Update Appointment")
        selected_id = st.selectbox("Select Appointment ID", df["id"].tolist())
        new_status = st.selectbox("New Status", ["Scheduled", "Completed", "Cancelled"])
        notes = st.text_area("Notes")
        if st.button("Update Appointment"):
            supabase.table("appointments").update({"status": new_status, "notes": notes}).eq(
                "id", int(selected_id)
            ).execute()
            st.success("Appointment updated!")
            st.rerun()

# ---------------- BOOK NEW ----------------
with tab2:
    if not patient_map or not doctor_map:
        st.warning("Add at least one patient and one doctor before booking appointments.")
    else:
        with st.form("book_appointment", clear_on_submit=True):
            patient_name = st.selectbox("Patient", list(patient_map.keys()))
            doctor_name = st.selectbox("Doctor", list(doctor_map.keys()))
            appt_date = st.date_input("Date", value=date.today())
            appt_time = st.time_input("Time", value=time(10, 0))
            reason = st.text_area("Reason for visit")
            submit = st.form_submit_button("Book Appointment")

            if submit:
                supabase.table("appointments").insert({
                    "patient_id": patient_map[patient_name],
                    "doctor_id": doctor_map[doctor_name],
                    "appointment_date": str(appt_date),
                    "appointment_time": str(appt_time),
                    "reason": reason,
                    "status": "Scheduled",
                }).execute()
                st.success("Appointment booked successfully!")
