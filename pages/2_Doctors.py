import streamlit as st
import pandas as pd

from utils.auth import require_role
from utils.db import supabase


st.set_page_config(
    page_title="Doctors",
    page_icon="🩺",
    layout="wide"
)


require_role([
    "Admin",
    "receptionist"
])


st.title("🩺 Doctor Management")


tab1, tab2 = st.tabs(
    [
        "📋 View Doctors",
        "➕ Add New Doctor"
    ]
)


# ---------------- VIEW ----------------

with tab1:

    data = supabase.table(
        "doctors"
    ).select("*").order(
        "full_name"
    ).execute().data


    df = pd.DataFrame(data)


    search = st.text_input(
        "🔍 Search by name or specialization"
    )


    if not df.empty and search:

        df = df[
            df["full_name"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["specialization"].fillna("").str.contains(
                search,
                case=False
            )
        ]


    st.dataframe(
        df,
        use_container_width=True
    )


    if not df.empty:


        st.subheader(
            "Update / Delete Doctor"
        )


        selected_id = st.selectbox(
            "Select Doctor ID",
            df["id"].tolist()
        )


        if st.button(
            "🗑️ Delete Doctor",
            type="secondary"
        ):


            supabase.table(
                "doctors"
            ).delete().eq(
                "id",
                selected_id
            ).execute()


            st.success(
                "Doctor Deleted"
            )


            st.rerun()



# ---------------- ADD ----------------


with tab2:


    with st.form(
        "add_doctor",
        clear_on_submit=True
    ):


        col1, col2 = st.columns(2)


        with col1:


            full_name = st.text_input(
                "Full Name*"
            )


            specialization = st.text_input(
                "Specialization"
            )


            department = st.text_input(
                "Department"
            )


            qualification = st.text_input(
                "Qualification"
            )



        with col2:


            phone = st.text_input(
                "Phone"
            )


            email = st.text_input(
                "Email"
            )


            experience_years = st.number_input(
                "Experience (years)",
                min_value=0,
                max_value=60
            )


            consultation_fee = st.number_input(
                "Consultation Fee ₹",
                min_value=0.0
            )



        submit = st.form_submit_button(
            "Add Doctor"
        )


        if submit:


            if not full_name.strip():


                st.error(
                    "Doctor name required"
                )


            else:


                supabase.table(
                    "doctors"
                ).insert({


                    "full_name": full_name.strip(),

                    "specialization": specialization,

                    "department": department,

                    "qualification": qualification,

                    "phone": phone,

                    "email": email,

                    "experience_years": int(
                        experience_years
                    ),

                    "consultation_fee": float(
                        consultation_fee
                    )


                }).execute()


                st.success(
                    f"Dr. {full_name} added successfully!"
                )