import streamlit as st
import pandas as pd
from datetime import date
from utils.auth import require_role
from utils.db import supabase

st.set_page_config(page_title="Patients", page_icon="🧑‍🤝‍🧑", layout="wide")
require_role(["admin", "doctor", "receptionist"])

st.title("🧑‍🤝‍🧑 Patient Records")

tab1, tab2 = st.tabs(["📋 View / Search", "➕ Register New Patient"])

# ---------------- VIEW / SEARCH ----------------
with tab1:
    data = supabase.table("patients").select("*").order("created_at", desc=True).execute().data
    df = pd.DataFrame(data)

    search = st.text_input("🔍 Search by name or phone")
    if not df.empty and search:
        df = df[
            df["full_name"].str.contains(search, case=False, na=False)
            | df["phone"].fillna("").str.contains(search, case=False, na=False)
        ]

    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.subheader("Update Status / Discharge / Delete")
        selected_id = st.selectbox("Select Patient ID", df["id"].tolist())
        patient = df[df["id"] == selected_id].iloc[0]

        with st.form("edit_patient"):
            status_options = ["Outpatient", "Admitted", "Discharged"]
            status = st.selectbox("Status", status_options, index=status_options.index(patient["status"]))
            discharge_date = st.date_input("Discharge Date (if discharging)", value=date.today())
            update = st.form_submit_button("Update Patient")

            if update:
                payload = {"status": status}
                payload["discharge_date"] = str(discharge_date) if status == "Discharged" else None
                supabase.table("patients").update(payload).eq("id", int(selected_id)).execute()
                st.success("Patient record updated!")
                st.rerun()

        if st.button("🗑️ Delete This Patient Record", type="secondary"):
            supabase.table("patients").delete().eq("id", int(selected_id)).execute()
            st.success("Deleted.")
            st.rerun()

# ---------------- ADD NEW ----------------
with tab2:
    with st.form("add_patient", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name*")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            phone = st.text_input("Phone")
        with col2:
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", "Unknown"])
            emergency_contact = st.text_input("Emergency Contact")
            address = st.text_area("Address")
            status = st.selectbox("Status", ["Outpatient", "Admitted"])

        admission_date = st.date_input("Admission Date", value=date.today()) if status == "Admitted" else None
        submit = st.form_submit_button("Register Patient")

        if submit:
            if not full_name.strip():
                st.error("Full name is required.")
            else:
                supabase.table("patients").insert({
                    "full_name": full_name.strip(),
                    "age": int(age),
                    "gender": gender,
                    "phone": phone,
                    "blood_group": blood_group,
                    "emergency_contact": emergency_contact,
                    "address": address,
                    "status": status,
                    "admission_date": str(admission_date) if admission_date else None,
                }).execute()
                st.success(f"Patient '{full_name}' registered successfully!")
