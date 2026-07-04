import streamlit as st
import pandas as pd

from utils.auth import require_role
from utils.db import supabase
from fpdf import FPDF


# ---------------- PDF FUNCTION ----------------

def create_bill_pdf(
    patient,
    service,
    amount,
    discount,
    total,
    method,
    status
):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=16
    )

    pdf.cell(
        200,
        10,
        "Hospital Management System",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font(
        "Arial",
        size=12
    )


    pdf.cell(
        200,
        10,
        f"Patient Name : {patient}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Service : {service}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Amount : Rs {amount}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Discount : Rs {discount}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Total Amount : Rs {total}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Payment Method : {method}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Payment Status : {status}",
        ln=True
    )


    file_name = "Hospital_Bill.pdf"

    pdf.output(
        file_name
    )

    return file_name



# ---------------- PAGE ----------------


st.set_page_config(
    page_title="Billing",
    page_icon="💳",
    layout="wide"
)


require_role(
    [
        "Admin",
        "receptionist"
    ]
)


st.title(
    "💳 Billing Management"
)


tab1, tab2 = st.tabs(
    [
        "📋 Billing Records",
        "➕ Create Bill"
    ]
)



# ---------------- VIEW ----------------


with tab1:

    data = supabase.table(
        "billing"
    ).select("*").execute().data


    df = pd.DataFrame(
        data
    )


    st.dataframe(
        df,
        use_container_width=True
    )



# ---------------- CREATE ----------------


with tab2:


    patients = supabase.table(
        "patients"
    ).select("*").execute().data


    patient_list = {

        p["full_name"]: p["id"]

        for p in patients

    }


    with st.form(
        "billing_form",
        clear_on_submit=True
    ):


        patient = st.selectbox(
            "Select Patient",
            list(patient_list.keys())
        )


        service_name = st.text_input(
            "Service Name"
        )


        amount = st.number_input(
            "Amount ₹",
            min_value=0.0
        )


        discount = st.number_input(
            "Discount ₹",
            min_value=0.0
        )


        total = amount - discount


        st.info(
            f"Total Amount ₹ {total}"
        )


        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "UPI",
                "Card"
            ]
        )


        payment_status = st.selectbox(
            "Payment Status",
            [
                "Paid",
                "Pending"
            ]
        )


        submit = st.form_submit_button(
            "Generate Bill"
        )


        if submit:


            supabase.table(
                "billing"
            ).insert(
                {

                    "patient_id": patient_list[patient],

                    "patient_name": patient,

                    "service_name": service_name,

                    "amount": amount,

                    "discount": discount,

                    "total_amount": total,

                    "payment_method": payment_method,

                    "payment_status": payment_status

                }
            ).execute()


            pdf_file = create_bill_pdf(

                patient,
                service_name,
                amount,
                discount,
                total,
                payment_method,
                payment_status

            )


            st.session_state[
                "bill_pdf"
            ] = pdf_file


            st.success(
                "Bill Created Successfully"
            )



# -------- PDF DOWNLOAD OUTSIDE FORM --------


if "bill_pdf" in st.session_state:


    with open(
        st.session_state["bill_pdf"],
        "rb"
    ) as file:


        st.download_button(

            label="📄 Download Bill PDF",

            data=file,

            file_name="Hospital_Bill.pdf",

            mime="application/pdf"

        )