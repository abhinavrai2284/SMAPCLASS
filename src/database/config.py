import os
import streamlit as st
from supabase import create_client, Client

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Check st.secrets safely without crashing if secrets are not configured yet
try:
    if hasattr(st, "secrets"):
        if not supabase_url and "SUPABASE_URL" in st.secrets:
            supabase_url = str(st.secrets["SUPABASE_URL"]).strip()
        if not supabase_key and "SUPABASE_KEY" in st.secrets:
            supabase_key = str(st.secrets["SUPABASE_KEY"]).strip()
except Exception:
    pass

supabase: Client = None

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")