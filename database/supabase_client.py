import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase():

    url = st.secrets["https://ezscscynbjknyxezzflp.supabase.co"]
    key = st.secrets["sb_publishable_sjiCkrhtL67GPlNC4loHFA_CPYkVeZb"]

    return create_client(url, key)


supabase = get_supabase()