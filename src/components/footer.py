import streamlit as st

def footer_home():
    st.markdown("""
        <div style="margin-top: 3.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 8px;">
            <p style="font-size: 0.88rem; color: #94a3b8; margin: 0;">
                ⚡ <b>SMAPCLASS</b> • Automated Face & Voice Biometric Attendance Platform
            </p>
            <p style="font-size: 0.78rem; color: #64748b; margin: 0;">
                Powered by dlib 128-d Vectorizer, Resemblyzer AI Speaker Recognition & Supabase Cloud
            </p>
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    st.markdown("""
        <div style="margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
            <p style="font-size: 0.82rem; color: #64748b; margin: 0;">
                <b>SMAPCLASS</b> • Enterprise Classroom AI Attendance
            </p>
            <p style="font-size: 0.82rem; color: #94a3b8; margin: 0;">
                Session Active 🟢
            </p>
        </div>
    """, unsafe_allow_html=True)