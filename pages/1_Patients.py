import streamlit as st
import pandas as pd

from datetime import date
from utils.auth import require_role
from utils.db import supabase


st.set_page_config(
    page_title="Patients",
    page_icon="🧑‍🤝‍🧑",
    layout="wide"
)


require_role([
    "Admin",
    "doctor",
    "receptionist"
])


st.title("🧑‍🤝‍🧑 Patient Records")


tab1, tab2 = st.tabs(
    [
        "📋 View / Search",
        "➕ Register New Patient"
    ]
)


# ---------------- VIEW ----------------

with tab1:

    data = supabase.table(
        "patients"
    ).select("*").order(
        "created_at",
        desc=True
    ).execute().data


    df = pd.DataFrame(data)


    search = st.text_input(
        "🔍 Search by name or phone"
    )


    if not df.empty and search:

        df = df[
            df["full_name"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["phone"].fillna("").str.contains(
                search,
                case=False
            )
        ]


    st.dataframe(
        df,
        use_container_width=True
    )


    if not df.empty:


        selected_id = st.selectbox(
            "Select Patient",
            df["id"].tolist()
        )


        patient = df[
            df["id"] == selected_id
        ].iloc[0]


        with st.form("update"):


            status = st.selectbox(
                "Status",
                [
                    "Outpatient",
                    "Admitted",
                    "Discharged"
                ]
            )


            update = st.form_submit_button(
                "Update Patient"
            )


            if update:


                supabase.table(
                    "patients"
                ).update({

                    "status": status

                }).eq(

                    "id",
                    selected_id

                ).execute()


                st.success(
                    "Patient Updated"
                )


                st.rerun()



# ---------------- ADD ----------------


with tab2:


    with st.form(
        "add_patient",
        clear_on_submit=True
    ):


        full_name = st.text_input(
            "Full Name"
        )


        age = st.number_input(
            "Age",
            0,
            120
        )


        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )


        phone = st.text_input(
            "Phone"
        )


        blood_group = st.selectbox(
            "Blood Group",
            [
                "A+",
                "A-",
                "B+",
                "B-",
                "O+",
                "O-",
                "AB+",
                "AB-",
                "Unknown"
            ]
        )


        emergency_contact = st.text_input(
            "Emergency Contact"
        )


        address = st.text_area(
            "Address"
        )


        status = st.selectbox(
            "Status",
            [
                "Outpatient",
                "Admitted"
            ]
        )


        submit = st.form_submit_button(
            "Register Patient"
        )


        if submit:


            supabase.table(
                "patients"
            ).insert({


                "full_name": full_name,

                "age": age,

                "gender": gender,

                "phone": phone,

                "blood_group": blood_group,

                "emergency_contact": emergency_contact,

                "address": address,

                "status": status


            }).execute()


            st.success(
                "Patient Added Successfully"
            )