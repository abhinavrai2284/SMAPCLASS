import streamlit as st
import textwrap

def subject_card(name, code, section, stats=None, footer_callback=None):
    stats_html = ""
    if stats:
        chips = "".join([f'<div style="background: rgba(235, 69, 158, 0.08); border: 1px solid rgba(235, 69, 158, 0.2); padding: 5px 12px; border-radius: 10px; font-size: 0.88rem; color: #1e293b;">{icon} <b>{value}</b> {label}</div>' for icon, label, value in stats])
        stats_html = f'<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;">{chips}</div>'

    html = textwrap.dedent(f"""
    <div style="background: white; border-left: 6px solid #EB459E; border: 1px solid #e2e8f0; border-left-width: 6px; border-left-color: #EB459E; padding: 20px 24px; border-radius: 16px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
        <h3 style="margin: 0; color: #1e293b; font-size: 1.3rem; font-weight: 700;">{name}</h3>
        <p style="color: #64748b; margin: 8px 0; font-size: 0.9rem;">
            Code: <span style="background: #eef2ff; color: #4f46e5; padding: 3px 8px; border-radius: 6px; font-weight: 600;">{code}</span>
            &nbsp;•&nbsp; Section: <b>{section}</b>
        </p>
        {stats_html}
    </div>
    """).strip()

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()