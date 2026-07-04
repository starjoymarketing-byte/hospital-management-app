import streamlit as st
import pandas as pd
from datetime import date
from utils.auth import require_role
from utils.db import supabase

st.set_page_config(page_title="Pharmacy", page_icon="💊", layout="wide")
require_role(["admin", "pharmacist"])

st.title("💊 Pharmacy / Medicine Inventory")

tab1, tab2 = st.tabs(["📋 Inventory", "➕ Add Medicine"])

# ---------------- VIEW ----------------
with tab1:
    data = supabase.table("pharmacy_inventory").select("*").order("medicine_name").execute().data
    df = pd.DataFrame(data)

    search = st.text_input("🔍 Search medicine")
    if not df.empty and search:
        df = df[df["medicine_name"].str.contains(search, case=False, na=False)]

    if not df.empty:
        low_stock = df[df["quantity"] <= df["reorder_level"]]
        if not low_stock.empty:
            st.warning(f"⚠️ {len(low_stock)} medicine(s) at or below reorder level — restock soon!")

    st.dataframe(df, use_container_width=True)

    if not df.empty:
        st.subheader("Update Stock / Remove")
        selected_id = st.selectbox("Select Medicine ID", df["id"].tolist())
        med = df[df["id"] == selected_id].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            new_qty = st.number_input("New Quantity", min_value=0, value=int(med["quantity"]))
            if st.button("Update Stock"):
                supabase.table("pharmacy_inventory").update({"quantity": int(new_qty)}).eq(
                    "id", int(selected_id)
                ).execute()
                st.success("Stock updated!")
                st.rerun()
        with col2:
            if st.button("🗑️ Remove Medicine", type="secondary"):
                supabase.table("pharmacy_inventory").delete().eq("id", int(selected_id)).execute()
                st.success("Removed.")
                st.rerun()

# ---------------- ADD NEW ----------------
with tab2:
    with st.form("add_medicine", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Medicine Name*")
            category = st.text_input("Category")
            manufacturer = st.text_input("Manufacturer")
            batch_number = st.text_input("Batch Number")
        with col2:
            quantity = st.number_input("Quantity", min_value=0, step=1)
            unit_price = st.number_input("Unit Price (₹)", min_value=0.0, step=1.0)
            expiry_date = st.date_input("Expiry Date", value=date.today())
            reorder_level = st.number_input("Reorder Level", min_value=0, value=10, step=1)

        submit = st.form_submit_button("Add Medicine")
        if submit:
            if not name.strip():
                st.error("Medicine name is required.")
            else:
                supabase.table("pharmacy_inventory").insert({
                    "medicine_name": name.strip(),
                    "category": category,
                    "manufacturer": manufacturer,
                    "batch_number": batch_number,
                    "quantity": int(quantity),
                    "unit_price": float(unit_price),
                    "expiry_date": str(expiry_date),
                    "reorder_level": int(reorder_level),
                }).execute()
                st.success(f"{name} added to inventory!")
