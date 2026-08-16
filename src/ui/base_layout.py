import streamlit as st

def style_base_layout():
    """Applies universal base layout styling, Google fonts, button overrides, and custom UI components."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
        
        /* Universal Font Settings */
        html, body, [class*="css"], .stMarkdown, .stText, p, span, label, div {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        /* Hide Streamlit default footer and top header */
        #MainMenu, footer, header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1050px !important;
        }

        /* Typography */
        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2.5rem !important;
            line-height: 1.15 !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: -0.5px;
        }

        h2 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.7rem !important;
            line-height: 1.2 !important;
            margin-bottom: 0.5rem !important;
        }

        h3, h4 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
        }

        /* Streamlit Button Styling */
        div.stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: 0.6rem 1.4rem !important;
            border: 1px solid transparent !important;
            transition: all 0.2s ease-in-out !important;
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #5865F2 0%, #4752C4 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(88, 101, 242, 0.25) !important;
        }

        div.stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 18px rgba(88, 101, 242, 0.4) !important;
        }

        div.stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #EB459E 0%, #d42e88 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(235, 69, 158, 0.25) !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            box-shadow: 0 6px 18px rgba(235, 69, 158, 0.4) !important;
        }

        div.stButton > button[kind="tertiary"] {
            background: #ffffff !important;
            color: #334155 !important;
            border: 1.5px solid #cbd5e1 !important;
        }

        div.stButton > button[kind="tertiary"]:hover {
            background: #f1f5f9 !important;
            border-color: #94a3b8 !important;
            color: #0f172a !important;
        }

        /* Input Fields */
        .stTextInput > div > div > input {
            border-radius: 10px !important;
            font-size: 0.95rem !important;
            border: 1.5px solid #cbd5e1 !important;
            padding: 0.6rem 1rem !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #5865F2 !important;
            box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.15) !important;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #e2e8f0;
            padding: 6px;
            border-radius: 14px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 8px 18px;
            font-weight: 600;
            color: #475569;
        }

        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #5865F2 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)


def style_background_home():
    """Modern styling for the All-in-One Hero Landing Page."""
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(180deg, #0b0f19 0%, #111827 50%, #0f172a 100%) !important;
            color: #f8fafc !important;
        }

        .landing-portal-card {
            background: linear-gradient(145deg, #1e293b 0%, #172033 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 1.8rem;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .portal-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 100px;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .portal-badge.teacher {
            background: rgba(88, 101, 242, 0.15);
            color: #818cf8;
            border: 1px solid rgba(88, 101, 242, 0.3);
        }

        .portal-badge.student {
            background: rgba(235, 69, 158, 0.15);
            color: #f472b6;
            border: 1px solid rgba(235, 69, 158, 0.3);
        }

        .feature-chip {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #cbd5e1;
            font-size: 0.9rem;
            margin: 6px 0;
        }

        .feature-chip .check-icon {
            color: #4ade80;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    """Clean modern background styling for Teacher & Student Dashboards."""
    st.markdown("""
        <style>
        .stApp {
            background: #f8fafc !important;
            color: #0f172a !important;
        }

        .block-container {
            background: #f8fafc;
        }
        </style>
    """, unsafe_allow_html=True)