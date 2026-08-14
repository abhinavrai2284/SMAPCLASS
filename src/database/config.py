import os
import streamlit as st
from supabase import create_client, Client

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

supabase_url = os.getenv("SUPABASE_URL") or os.getenv("supabase_url")
supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("supabase_key")

# Check st.secrets safely without crashing if secrets are not configured yet
try:
    if hasattr(st, "secrets"):
        for key in ["SUPABASE_URL", "supabase_url", "Supabase_Url"]:
            if key in st.secrets and not supabase_url:
                supabase_url = str(st.secrets[key]).strip()
        for key in ["SUPABASE_KEY", "supabase_key", "Supabase_Key"]:
            if key in st.secrets and not supabase_key:
                supabase_key = str(st.secrets[key]).strip()
except Exception as e:
    pass

supabase: Client = None

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")