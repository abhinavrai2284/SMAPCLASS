import streamlit as st
import io

try:
    import segno
except ImportError:
    segno = None


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "smapclassapp.streamlit.app"
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    st.header("Scan to Join")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info('Copy this link to share on WhatsApp or Email')

    with col2:
        st.markdown('### Scan to Join')
        if segno:
            try:
                qr = segno.make(join_url)
                out = io.BytesIO()
                qr.save(out, kind='png', scale=10, border=1)
                st.image(out.getvalue(), caption='QR Code for class joining')
            except Exception:
                st.write(f"Class Code: **{subject_code}**")
        else:
            st.write(f"Class Code: **{subject_code}**")