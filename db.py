import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def init_supabase() -> Client:
    """Create (and cache) a single Supabase client for the whole app session."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase: Client = init_supabase()
