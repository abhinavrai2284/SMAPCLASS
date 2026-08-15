import os
import streamlit as st

try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    Client = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Default project credentials (publishable client key)
DEFAULT_SUPABASE_URL = "https://lddkomsesyexjwdtskfh.supabase.co"
DEFAULT_SUPABASE_KEY = "sb_publishable_NDLEyZZYU6y574euWYlV3g_TcKzESSZ"

supabase_url = os.getenv("SUPABASE_URL") or os.getenv("supabase_url")
supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("supabase_key")

# Check st.secrets safely with flexible lookup
try:
    if hasattr(st, "secrets"):
        # 1. Top-level keys
        for k in st.secrets:
            k_lower = str(k).lower().replace("-", "_")
            if "url" in k_lower and not supabase_url:
                val = str(st.secrets[k]).strip().strip('"').strip("'")
                if val.startswith("http"):
                    supabase_url = val
            if ("key" in k_lower or "token" in k_lower) and not supabase_key:
                val = str(st.secrets[k]).strip().strip('"').strip("'")
                supabase_key = val

        # 2. Nested sections (e.g. [supabase] or [connections])
        for section in ["supabase", "connections", "db"]:
            if section in st.secrets and isinstance(st.secrets[section], dict):
                sec = st.secrets[section]
                for k, v in sec.items():
                    k_lower = str(k).lower()
                    v_str = str(v).strip().strip('"').strip("'")
                    if "url" in k_lower and v_str.startswith("http"):
                        supabase_url = v_str
                    if "key" in k_lower or "token" in k_lower:
                        supabase_key = v_str
except Exception as e:
    pass

# Fallback to project defaults if not provided in environment or secrets
if not supabase_url:
    supabase_url = DEFAULT_SUPABASE_URL
if not supabase_key:
    supabase_key = DEFAULT_SUPABASE_KEY

supabase = None

if create_client and supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")