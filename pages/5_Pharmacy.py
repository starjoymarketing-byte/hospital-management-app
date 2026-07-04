import streamlit as st
import pandas as pd

from datetime import date
from utils.auth import require_role
from utils.db import supabase


# ---------------- PAGE ----------------

st.set_page_config(
    page_title="Pharmacy",
    page_icon="💊",
    layout="wide"
)


require_role(
    [
        "Admin",
        "receptionist"
    ]
)


st.title(
    "💊 Pharmacy Management"
)


tab1, tab2 = st.tabs(
    [
        "📋 Medicine Stock",
        "➕ Add Medicine"
    ]
)


# ---------------- VIEW MEDICINE ----------------


with tab1:


    data = supabase.table(
        "pharmacy"
    ).select("*").execute().data


    df = pd.DataFrame(data)


    search = st.text_input(
        "🔍 Search Medicine"
    )


    if not df.empty and search:

        df = df[
            df["medicine_name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]


    st.dataframe(
        df,
        use_container_width=True
    )


    if not df.empty:


        st.subheader(
            "Update Stock"
        )


        selected_id = st.selectbox(
            "Select Medicine ID",
            df["id"].tolist()
        )


        qty = st.number_input(
            "New Quantity",
            min_value=0
        )


        if st.button(
            "Update Quantity"
        ):


            supabase.table(
                "pharmacy"
            ).update({

                "quantity": qty

            }).eq(

                "id",
                selected_id

            ).execute()


            st.success(
                "Stock Updated"
            )


            st.rerun()


        if st.button(
            "🗑️ Delete Medicine"
        ):


            supabase.table(
                "pharmacy"
            ).delete().eq(

                "id",
                selected_id

            ).execute()


            st.success(
                "Medicine Deleted"
            )


            st.rerun()



# ---------------- ADD MEDICINE ----------------


with tab2:


    with st.form(
        "medicine_form",
        clear_on_submit=True
    ):


        col1, col2 = st.columns(2)


        with col1:


            medicine_name = st.text_input(
                "Medicine Name"
            )


            category = st.text_input(
                "Category"
            )


            company = st.text_input(
                "Company"
            )


            quantity = st.number_input(
                "Quantity",
                min_value=0
            )


        with col2:


            price = st.number_input(
                "Price ₹",
                min_value=0.0
            )


            expiry_date = st.date_input(
                "Expiry Date",
                date.today()
            )


            supplier = st.text_input(
                "Supplier"
            )


            status = st.selectbox(
                "Status",
                [
                    "Available",
                    "Out of Stock"
                ]
            )


        submit = st.form_submit_button(
            "Add Medicine"
        )


        if submit:


            supabase.table(
                "pharmacy"
            ).insert({

                "medicine_name": medicine_name,

                "category": category,

                "company": company,

                "quantity": quantity,

                "price": price,

                "expiry_date": str(expiry_date),

                "supplier": supplier,

                "status": status


            }).execute()


            st.success(
                "Medicine Added Successfully"
            )