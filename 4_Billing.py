import streamlit as st
import pandas as pd
from utils.auth import require_role
from utils.db import supabase

st.set_page_config(page_title="Billing", page_icon="💰", layout="wide")
require_role(["admin", "receptionist"])

st.title("💰 Billing & Invoicing")

patients = supabase.table("patients").select("id, full_name").order("full_name").execute().data
patient_map = {p["full_name"]: p["id"] for p in patients}

tab1, tab2 = st.tabs(["📋 View Bills", "➕ Generate New Bill"])

# ---------------- VIEW ----------------
with tab1:
    data = (
        supabase.table("bills")
        .select("*, patients(full_name)")
        .order("created_at", desc=True)
        .execute()
        .data
    )

    rows = []
    for b in data:
        rows.append({
            "id": b["id"],
            "Patient": b["patients"]["full_name"] if b.get("patients") else "—",
            "Date": b["bill_date"],
            "Total (₹)": b["total_amount"],
            "Status": b["payment_status"],
        })
    df = pd.DataFrame(rows)

    status_filter = st.selectbox("Filter by payment status", ["All", "Pending", "Partial", "Paid"])
    if status_filter != "All" and not df.empty:
        df = df[df["Status"] == status_filter]

    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.subheader("Update Payment")
        selected_id = st.selectbox("Select Bill ID", df["id"].tolist())
        new_status = st.selectbox("Payment Status", ["Pending", "Partial", "Paid"])
        method = st.selectbox("Payment Method", ["Cash", "Card", "UPI", "Insurance"])
        if st.button("Update Payment Status"):
            supabase.table("bills").update({
                "payment_status": new_status,
                "payment_method": method,
            }).eq("id", int(selected_id)).execute()
            st.success("Payment status updated!")
            st.rerun()

# ---------------- GENERATE NEW ----------------
with tab2:
    if not patient_map:
        st.warning("Add at least one patient before generating a bill.")
    else:
        with st.form("generate_bill", clear_on_submit=True):
            patient_name = st.selectbox("Patient", list(patient_map.keys()))
            consultation_fee = st.number_input("Consultation Fee (₹)", min_value=0.0, step=100.0)
            room_charges = st.number_input("Room Charges (₹)", min_value=0.0, step=100.0)
            medicine_charges = st.number_input("Medicine Charges (₹)", min_value=0.0, step=50.0)
            other_charges = st.number_input("Other Charges (₹)", min_value=0.0, step=50.0)

            total = consultation_fee + room_charges + medicine_charges + other_charges
            st.metric("Total Amount", f"₹{total:,.2f}")

            submit = st.form_submit_button("Generate Bill")
            if submit:
                supabase.table("bills").insert({
                    "patient_id": patient_map[patient_name],
                    "consultation_fee": consultation_fee,
                    "room_charges": room_charges,
                    "medicine_charges": medicine_charges,
                    "other_charges": other_charges,
                    "total_amount": total,
                    "payment_status": "Pending",
                }).execute()
                st.success(f"Bill generated for {patient_name}: ₹{total:,.2f}")
