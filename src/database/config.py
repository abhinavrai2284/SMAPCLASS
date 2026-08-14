import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") and "SUPABASE_URL" in st.secrets else os.getenv("SUPABASE_URL")
supabase_key = st.secrets.get("SUPABASE_KEY") if hasattr(st, "secrets") and "SUPABASE_KEY" in st.secrets else os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)