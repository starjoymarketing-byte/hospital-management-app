import streamlit as st
import pandas as pd

from datetime import date
from utils.auth import require_role
from utils.db import supabase


st.set_page_config(
    page_title="Appointments",
    page_icon="📅",
    layout="wide"
)


require_role([
    "Admin",
    "doctor",
    "receptionist"
])


st.title("📅 Appointment Management")


tab1, tab2 = st.tabs(
    [
        "📋 Appointments",
        "➕ New Appointment"
    ]
)


# ---------------- VIEW ----------------


with tab1:


    data = supabase.table(
        "appointments"
    ).select("*").execute().data


    df = pd.DataFrame(data)


    st.dataframe(
        df,
        use_container_width=True
    )


    if not df.empty:


        selected_id = st.selectbox(
            "Select Appointment",
            df["id"].tolist()
        )


        status = st.selectbox(
            "Update Status",
            [
                "Pending",
                "Completed",
                "Cancelled"
            ]
        )


        if st.button(
            "Update Appointment"
        ):


            supabase.table(
                "appointments"
            ).update({

                "status": status

            }).eq(

                "id",
                selected_id

            ).execute()


            st.success(
                "Appointment Updated"
            )


            st.rerun()



# ---------------- ADD ----------------


with tab2:


    patients = supabase.table(
        "patients"
    ).select("*").execute().data


    doctors = supabase.table(
        "doctors"
    ).select("*").execute().data


    patient_names = {
        p["full_name"]: p["id"]
        for p in patients
    }


    doctor_names = {
        d["full_name"]: d["id"]
        for d in doctors
    }


    with st.form(
        "appointment_form",
        clear_on_submit=True
    ):


        patient = st.selectbox(
            "Select Patient",
            list(patient_names.keys())
        )


        doctor = st.selectbox(
            "Select Doctor",
            list(doctor_names.keys())
        )


        appointment_date = st.date_input(
            "Appointment Date",
            date.today()
        )


        appointment_time = st.time_input(
    "Appointment Time"
        )


        reason = st.text_area(
            "Reason"
        )


        status = st.selectbox(
            "Status",
            [
                "Pending",
                "Completed",
                "Cancelled"
            ]
        )


        submit = st.form_submit_button(
            "Book Appointment"
        )


        if submit:


            supabase.table(
                "appointments"
            ).insert({


                "patient_id": patient_names[patient],

                "doctor_id": doctor_names[doctor],

                "patient_name": patient,

                "doctor_name": doctor,

                "appointment_date": str(
                    appointment_date
                ),

                "appointment_time": str(appointment_time),

                "reason": reason,

                "status": status


            }).execute()


            st.success(
                "Appointment Booked Successfully"
            )