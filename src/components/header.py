import streamlit as st

def header_home():
    """Renders the top branding and hero header on the Home Landing Page."""
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; margin-bottom: 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <img src="{logo_url}" style="height: 48px; border-radius: 10px;" alt="SMAPCLASS Logo" />
                <div>
                    <div style="font-family: 'Climate Crisis', sans-serif; font-size: 1.6rem; color: #ffffff; line-height: 1;">SMAPCLASS</div>
                    <div style="font-size: 0.78rem; color: #94a3b8; font-weight: 500; letter-spacing: 0.5px;">NEXT-GEN AI ATTENDANCE</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.3); padding: 5px 14px; border-radius: 100px; display: flex; align-items: center; gap: 8px;">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #22c55e; display: inline-block; box-shadow: 0 0 8px #22c55e;"></span>
                    <span style="font-size: 0.8rem; font-weight: 700; color: #86efac;">AI Engine Active</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    """Renders dashboard header with brand and quick navigation back to home."""
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px;">
            <img src="{logo_url}" style="height: 44px; border-radius: 8px;" alt="Logo" />
            <div>
                <div style="font-family: 'Climate Crisis', sans-serif; font-size: 1.4rem; color: #5865F2; line-height: 1;">SMAPCLASS</div>
                <div style="font-size: 0.72rem; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">AI CLASSROOM PORTAL</div>
            </div>
        </div>
    """, unsafe_allow_html=True)