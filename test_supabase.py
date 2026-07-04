import streamlit as st
from supabase import create_client


url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)


st.title("Hospital Management System")

data = supabase.table("patients").select("*").execute()

st.write(data.data)

st.success("Supabase Connected Successfully")